import reversion
from django.db import models
from django.db.models import DateTimeField, F
from django_jsonform.models.fields import ArrayField
from localized_fields.fields import LocalizedCharField, LocalizedTextField

from headless_cms.fields.martor_field import LocalizedMartorField
from headless_cms.models import LocalizedPublicationModel


@reversion.register(exclude=("published_version",))
class AWPostMetadata(LocalizedPublicationModel):
    title = LocalizedTextField(blank=True, null=True, required=False)
    description = LocalizedTextField(blank=True, null=True, required=False)
    canonical = LocalizedCharField(blank=True, null=True, required=False)


@reversion.register(exclude=("published_version",))
class AWPost(LocalizedPublicationModel):
    title = LocalizedTextField(blank=True, null=True, required=False)
    excerpt = LocalizedTextField(blank=True, null=True, required=False)
    image = LocalizedCharField(blank=True, null=True, required=False)
    draft = models.BooleanField(default=False)
    category = LocalizedCharField(blank=True, null=True, required=False)
    tags = ArrayField(models.CharField(max_length=50), blank=True, default=list)
    author = LocalizedCharField(blank=True, null=True, required=False)

    content = LocalizedMartorField(default=dict, blank=True, null=True, required=False)

    metadata = models.ForeignKey(
        AWPostMetadata, blank=True, null=True, on_delete=models.SET_NULL
    )

    published_date = DateTimeField(blank=True, null=True)
    updated_date = DateTimeField(auto_now=True)
    created_date = DateTimeField(auto_now_add=True)

    class Meta:
        ordering = [F("published_date").desc(nulls_first=True), "-created_date"]
        index_together = ["published_date", "created_date"]
