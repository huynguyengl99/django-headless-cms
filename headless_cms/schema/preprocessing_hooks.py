from headless_cms.mixins import CMSSchemaMixin


def preprocessing_filter_spec(endpoints):
    filtered = []
    for path, path_regex, method, view in endpoints:
        if not issubclass(view.cls, CMSSchemaMixin):
            continue
        filtered.append((path, path_regex, method, view))
    return filtered
