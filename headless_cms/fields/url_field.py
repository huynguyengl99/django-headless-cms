from django.db.models import CharField


class AutoLanguageUrlField(CharField):
    """This field will automatically add language prefix path for relative url (/about => /en/about)
    but will keep the full url as it is."""

    pass
