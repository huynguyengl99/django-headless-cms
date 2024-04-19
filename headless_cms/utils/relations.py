from headless_cms.models import PublicationModel

calculated_models = {}


def calculate_prefetch_relation(
    model: PublicationModel, fetched_models: set | None = None
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
            or not issubclass(rel_model, PublicationModel)
            or f.auto_created
            and not f.related_name
        ):
            continue
        f_name = f.name
        if f.many_to_many or f.one_to_many:
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
