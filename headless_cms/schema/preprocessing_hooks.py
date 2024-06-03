from headless_cms.mixins import CMSSchemaMixin


def preprocessing_filter_spec(endpoints):
    """
    Preprocessing hook to filter endpoints for the OpenAPI schema.

    This function filters the endpoints to include only those views that extend the
    `CMSSchemaMixin`. It is used as a preprocessing hook for DRF Spectacular to
    dynamically generate the OpenAPI schema for CMS views.

    Args:
        endpoints (list): A list of endpoints to be processed.

    Returns:
        list: A filtered list of endpoints that include only CMS views.
    """
    filtered = []
    for path, path_regex, method, view in endpoints:
        if not issubclass(view.cls, CMSSchemaMixin):
            continue
        filtered.append((path, path_regex, method, view))
    return filtered
