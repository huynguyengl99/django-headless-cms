from django.db.models import Prefetch

from headless_cms.models import LocalizedPublicationModel, M2MSortedOrderThrough

calculated_models = {}


class CumulativePrefetch(Prefetch):
    def __radd__(self, other: str):
        self.add_prefix(other.replace("__", ""))
        return self


def calculate_prefetch_relation(
    model: type[LocalizedPublicationModel], fetched_models: set | None = None
):
    if fetched_models is None:
        fetched_models = {model}
    prefetch_relations = []
    select_relations = ["published_version"]
    fields = model._meta.get_fields()
    fetched_models = fetched_models | {model}
    for f in fields:
        rel_model = f.related_model
        if (
            not rel_model
            or rel_model in fetched_models
            or not issubclass(rel_model, LocalizedPublicationModel)
            or f.auto_created
        ):
            continue
        f_name = f.name
        if f.many_to_many or f.one_to_many:
            if f.many_to_many and issubclass(
                f.remote_field.through, M2MSortedOrderThrough
            ):
                thr = f.remote_field.through
                tfs = thr._meta.get_fields()
                rlt_field = next(
                    obj.remote_field
                    for obj in tfs
                    if obj.is_relation and obj.related_model != model
                )
                rlt_name = rlt_field.related_name or rlt_field.name
                queryset = rlt_field.model.objects.order_by(rlt_name + "__position")

                prefetch_relations.append(CumulativePrefetch(f_name, queryset))
            else:
                prefetch_relations.append(f_name)
            prefetches, selects = calculate_prefetch_relation(rel_model, fetched_models)
            prefetch_relations.extend(
                [
                    f_name + "__" + relation_name
                    for relation_name in prefetches + selects
                ]
            )
        else:
            select_relations.append(f_name)
            prefetches, selects = calculate_prefetch_relation(rel_model, fetched_models)
            prefetch_relations.extend(
                [f_name + "__" + relation_name for relation_name in prefetches]
            )
            select_relations.extend(
                [f_name + "__" + relation_name for relation_name in selects]
            )

    return prefetch_relations, select_relations
