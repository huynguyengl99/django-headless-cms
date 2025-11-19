import asyncio
import functools
from functools import cached_property

import reversion
from django.contrib import admin
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.html import format_html
from localized_fields.fields import (
    LocalizedFileField,
    LocalizedTextField,
)
from localized_fields.models import LocalizedModel
from reversion.models import Version
from solo.models import SingletonModel

from headless_cms.fields import LocalizedUniqueNormalizedSlugField, LocalizedUrlField
from headless_cms.settings import headless_cms_settings
from headless_cms.utils.hash_utils import HashTracker


class PublishedQuerySet(models.QuerySet):
    """
    Custom QuerySet for handling published models.
    """

    @cached_property
    def prefetch_relation_list(self):
        from headless_cms.utils.relations import calculate_prefetch_relation  # noqa

        return calculate_prefetch_relation(self.model)

    def published(self, auto_prefetch=False):
        """
        Filter the QuerySet to only include published items.

        Args:
            auto_prefetch (bool): Whether to automatically prefetch related objects.

        Returns:
            QuerySet: A filtered QuerySet with only published items.
        """
        prefetches = []
        selects = []
        if auto_prefetch:
            prefetches, selects = self.prefetch_relation_list

        return (
            self.select_related(*selects)
            .prefetch_related(*prefetches)
            .filter(published_version__isnull=False)
        )


class PublishedManager(models.Manager):
    """
    Custom Manager for handling published models.
    """

    def get_queryset(self):
        return PublishedQuerySet(self.model, using=self._db)

    def published(self, auto_prefetch=False):
        """
        Filter the QuerySet to only include published items.

        Args:
            auto_prefetch (bool): Whether to automatically prefetch related objects.

        Returns:
            QuerySet: A filtered QuerySet with only published items.
        """
        return self.get_queryset().published(auto_prefetch)


class LocalizedPublicationModel(LocalizedModel):
    """
    Abstract model for localized publication.

    This model extends the LocalizedModel to include versioning and publication
    functionality. It keeps track of the published version and allows for recursive
    actions on related objects.

    Attributes:
        published_version (ForeignKey): Reference to the published version.
        versions (GenericRelation): Relation to the versions of the model.
    """

    class AdminPublishedStateHtml:
        """
        HTML representations of the publication state.

        This nested class contains constants representing the HTML used to indicate
        the publication state of an object in the Django admin interface. It provides
        visual feedback on whether an object is unpublished, published but outdated,
        or published and up-to-date, using different colors for each state.

        Attributes:
            UNPUBLISHED (str): HTML for the unpublished state (red).
            PUBLISHED_OUTDATED (str): HTML for the published but outdated state (orange).
            PUBLISHED_LATEST (str): HTML for the published and up-to-date state (blue).
        """

        UNPUBLISHED = '<div style="color:red;">unpublished<div>'
        PUBLISHED_OUTDATED = '<div style="color:orange;">published (outdated)<div>'
        PUBLISHED_LATEST = '<div style="color:blue;">published (latest)<div>'

    published_version = models.ForeignKey(
        Version, editable=False, null=True, on_delete=models.SET_NULL
    )
    versions = GenericRelation(Version)
    skip_translation = models.BooleanField(default=False)

    objects = models.Manager()
    published_objects = PublishedManager()

    class Meta(LocalizedModel.Meta):
        abstract = True

    @property
    def published_data(self):
        """
        Get the data of the published version.

        Returns:
            dict: The field data of the published version, or None if not published.
        """
        if self.published_version_id:
            return self.published_version.field_dict

    def publish(self, user=None):
        """
        Publish the current version of the object.

        Args:
            user (User, optional): The user performing the publish action.
        """

        last_ver = Version.objects.get_for_object(self).first()

        if last_ver and last_ver.id == self.published_version_id:
            return

        with reversion.create_revision():
            reversion.set_comment("Publish")
            if user:
                reversion.set_user(user)

            self.save()

        with reversion.create_revision(manage_manually=True):
            last_ver = Version.objects.get_for_object(self).first()
            self.published_version = last_ver
            self.save()

    def build_actions(self, action, *args, tracker=None, **kwargs):
        """
        Perform an action recursively on the object and its related objects.

        Args:
            action (callable): The action to be performed.
            tracker: the list to track the object processed, not to do it again when being reference multiple times
        """
        action_list = []
        if tracker is None:
            tracker = set()

        track = (self._meta.object_name, self.id)
        if track in tracker:
            return action_list

        action_list.append((action, self, args, kwargs))
        tracker.add(track)

        for f in self._meta.get_fields():
            if (
                f.is_relation
                and not f.auto_created
                and f.related_model
                and issubclass(f.related_model, LocalizedPublicationModel)
            ):
                if f.many_to_one:
                    rel_obj = getattr(self, f.name)
                    if rel_obj:
                        action_list.extend(
                            rel_obj.build_actions(
                                action, *args, tracker=tracker, **kwargs
                            )
                        )
                elif f.many_to_many or f.one_to_many:
                    rel_objs = getattr(self, f.name).all()
                    for rel_obj in rel_objs:
                        action_list.extend(
                            rel_obj.build_actions(
                                action, *args, tracker=tracker, **kwargs
                            )
                        )
        return action_list

    def recursive_action(self, action, *args, **kwargs):
        action_list = self.build_actions(action, *args, **kwargs)

        async def run_actions(actions):
            loop = asyncio.get_event_loop()
            futures = []
            for act, _self, r_args, r_kwargs in actions:
                p_action = functools.partial(act, _self, *r_args, **r_kwargs)
                futures.append(loop.run_in_executor(None, p_action))

            result = await asyncio.gather(*futures)
            return result

        asyncio.run(run_actions(action_list))

    def recursively_publish(self, user=None):
        """
        Recursively publish the object and its related objects.

        Args:
            user (User, optional): The user performing the publish action.
        """
        self.recursive_action(self.__class__.publish, user=user)

    def unpublish(self, user=None):
        """
        Unpublish the current version of the object.

        Args:
            user (User, optional): The user performing the unpublish action.
        """
        with reversion.create_revision():
            reversion.set_comment("Unpublish")
            if user:
                reversion.set_user(user)

            self.save()

        with reversion.create_revision(manage_manually=True):
            self.published_version = None
            self.save()

    def translate(self, user=None, force=False):
        """
        Translate the object.

        Args:
            user (User, optional): The user performing the translation.
            force (bool, optional): Whether to force the translation.
        """
        if self.skip_translation:
            return

        with reversion.create_revision():
            reversion.set_comment(f"Object translated{' (forced)' if force else ''}.")

            if user:
                reversion.set_user(user)
            translator = headless_cms_settings.AUTO_TRANSLATE_CLASS(self)
            translator.process(force=force)

    def recursively_translate(self, user=None, force=False):
        """
        Recursively translate the object and its related objects.

        Args:
            user (User, optional): The user performing the translation.
            force (bool, optional): Whether to force the translation.
        """
        self.recursive_action(self.__class__.translate, user, force=force)

    def accumulate_hash(self, hash_tracker: HashTracker | None):
        """
        Accumulate the hash of the current object's published version ID into the hash tracker.

        This method is primarily used within a recursive hashing mechanism to roll up the hashes
        of an object and its dependencies or related items.

        Args:
            hash_tracker (HashTracker, optional): An instance of HashTracker that accumulates
            hashes.
        """
        hash_tracker.update_hash(self.published_version_id)

    def get_recursive_hash(self):
        """
        Generate and retrieve a composite hash representing the current object and its relations.

        This method initializes a new HashTracker and uses it to recursively accumulate hashes
        starting from the current object's published version ID. It leverages the accumulate_hash
        method to traverse and include related entities in the hash computation.

        Returns:
            str: The final calculated hash as a hexadecimal string, representing the state of
            this object and its recursively related entities.
        """
        hash_tracker = HashTracker()
        hash_tracker.update_hash(self.published_version_id)

        self.recursive_action(self.__class__.accumulate_hash, hash_tracker)

        return hash_tracker.current_hash

    @admin.display
    def published_state(self):
        """
        Get the published state of the object as HTML for the Django admin interface.

        This method provides a visual indicator of the publication state of an object
        in the Django admin interface. It returns an HTML representation indicating
        whether the object is unpublished, published (outdated), or published (latest).

        Returns:
            str: The HTML representation of the published state.
        """
        state = self.AdminPublishedStateHtml.UNPUBLISHED
        if self.published_version_id:
            last_ver = Version.objects.get_for_object(self).first()
            if last_ver.id == self.published_version_id:
                state = self.AdminPublishedStateHtml.PUBLISHED_LATEST
            else:
                state = self.AdminPublishedStateHtml.PUBLISHED_OUTDATED

        return format_html(state)

    published_state.allow_tags = True


class LocalizedSingletonModel(LocalizedPublicationModel, SingletonModel):
    """
    Abstract model for localized singleton.

    This model extends SingletonModel to include versioning and publication
    functionality for singleton instances.
    """

    @classmethod
    def get_solo(cls):
        obj = super().get_solo()
        if not obj.published_version_id:
            return None
        return obj

    class Meta:
        abstract = True


class LocalizedTitleSlugModel(LocalizedPublicationModel):
    """
    Abstract model for localized title and slug.

    This model extends LocalizedPublicationModel to include title and slug fields
    that are automatically populated and unique per language.

    Attributes:
        title (LocalizedTextField): The title of the object.
        slug (LocalizedUniqueNormalizedSlugField): The slug of the object.
    """

    title = LocalizedTextField(blank=True, null=True, required=False)
    slug = LocalizedUniqueNormalizedSlugField(
        populate_from="title", blank=True, null=True, required=False
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        abstract = True


class LocalizedDynamicFileModel(LocalizedPublicationModel):
    """
    Abstract model for localized dynamic file.

    This model extends LocalizedPublicationModel to include fields for either
    uploading files or specifying URLs, along with alternative text. When both
    a file and a URL are provided, the file takes precedence.

    Attributes:
        src_file (LocalizedFileField): The source file.
        src_url (LocalizedCharField): The source URL.
        alt (LocalizedTextField): The alternative text for the file.
    """

    src_file = LocalizedFileField(default=dict, blank=True, null=True, required=False)
    src_url = LocalizedUrlField(default=dict, blank=True, null=True, required=False)
    alt = LocalizedTextField(blank=True, null=True, required=False)

    class Meta:
        abstract = True

    @property
    def src_link(self):
        """
        Get the source link.

        This property returns the absolute URL of the source file if it exists.
        If the source file does not exist, it returns the translated URL.

        Returns:
            str: The absolute URL of the source file or the translated URL.
        """
        src_file = self.src_file.translate()
        if src_file:
            src_url = src_file.url
            if src_url.startswith("/"):
                src_url = f"{headless_cms_settings.CMS_HOST}{src_url}"
            return src_url
        elif self.src_url:
            return self.src_url.translate()


class M2MSortedOrderThrough(models.Model):
    """
    Abstract model for many-to-many relationships with a position field for sorting.

    This model is designed to be used as a through table for many-to-many relationships
    where the order of the related objects is important. It includes a `position` field
    that is used by the `sortableadmin` library to specify the order of the related objects.

    Attributes:
        fk_name (str): The name of the foreign key field that points to the parent model.
            This is used to detect the parent model in self-referencing many-to-many
            relationships. For normal many-to-many relationships, this attribute is not
            needed.

        position (PositiveIntegerField): The position field for sorting the related objects.

    Usage:
        The `fk_name` attribute is specifically used in self-referencing many-to-many
        relationships to detect the parent object. This allows the detection of child
        objects and the ability to get the status of the child objects for visualization
        in the Django admin interface.

    Example:
        In a self-referencing many-to-many relationship, set `fk_name` to the name of
        the foreign key field that points to the parent model.

        .. code-block:: python

            class MyModel(LocalizedPublicationModel):
                related_objects = models.ManyToManyField(
                    'self',
                    through='MyModelThrough'
                )

            class MyModelThrough(M2MSortedOrderThrough):
                fk_name = 'parent_model'
                parent_model = models.ForeignKey(MyModel, on_delete=models.CASCADE)
                child_model = models.ForeignKey(MyModel, related_name='child_set', on_delete=models.CASCADE)
    """

    fk_name = None
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["position"]
        abstract = True


class SortableGenericBaseModel(LocalizedPublicationModel):
    """
    Abstract model for sortable generic base.

    This model extends LocalizedPublicationModel to include fields for generic
    relations and sorting.

    Attributes:
        content_type (ForeignKey): The content type of the related object.
        object (GenericForeignKey): The related object.
        object_id (PositiveIntegerField): The ID of the related object.
        position (PositiveIntegerField): The position for sorting.
    """

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    object = GenericForeignKey(
        ct_field="content_type",
        fk_field="object_id",
    )

    object_id = models.PositiveIntegerField(blank=True, null=True)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["position"]
        abstract = True

    def __str__(self):
        return f"{self._meta.object_name} - {self.id} for {self.object}"

    @property
    def _content_type(self):
        """
        Get the content type of the related object.

        Returns:
            ContentType: The content type of the related object.
        """
        return ContentType.objects.db_manager(self._state.db).get_for_id(
            self.content_type_id
        )

    @property
    def _model(self):
        """
        Get the model class of the related object.

        Returns:
            Model: The model class of the related object.
        """
        return self._content_type.model_class()
