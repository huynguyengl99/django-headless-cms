def preprocessing_filter_spec(endpoints):
    filtered = []
    for path, path_regex, method, view in endpoints:
        if "CMS" not in str(view.cls):
            continue
        filtered.append((path, path_regex, method, view))
    return filtered
