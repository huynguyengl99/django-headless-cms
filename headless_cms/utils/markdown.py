import re
from ast import literal_eval

from django.apps import apps
from django.utils.translation import gettext_lazy as _
from martor.utils import markdownify


def replace_placeholder(markdown_text, show_invalid=True):
    res = markdown_text
    pattern = re.compile(r"<getattr>(.*?)<getattr/>", re.DOTALL)
    groups = set(pattern.findall(markdown_text))
    for match in groups:
        try:
            app_model, id, attr = literal_eval(match)
            app_str, model_str = app_model.split(".")

            app = apps.get_app_config(app_str)
            model = app.get_model(model_str)
            obj = model.objects.get(pk=id)
            dt = getattr(obj, attr)
        except Exception:
            dt = str(_("Invalid placeholder")) if show_invalid else None
        res = res.replace(f"<getattr>{match}<getattr/>", dt) if dt else res

    return res


def custom_markdownify(markdown_text):
    markdown_text = replace_placeholder(markdown_text)
    return markdownify(markdown_text)
