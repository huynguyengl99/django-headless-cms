import json
import re
import time
from unittest.mock import patch

from django.conf import settings
from headless_cms.auto_translate.openai_translate import OpenAITranslate
from openai.types.chat import ChatCompletion, ChatCompletionMessage
from openai.types.chat.chat_completion import Choice

from helpers.base import BaseTestCase
from test_app.factories import PostFactory
from test_app.models import Post


class TestOpenAITranslate(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.instance: Post = PostFactory()
        self.translator = OpenAITranslate(self.instance)

        def batch_translate(raw):
            res = {}
            for language, obj_to_trans in raw.items():
                res[language] = {k: language + "-" + v for k, v in obj_to_trans.items()}
            return res

        self.batch_translate = batch_translate

    @patch("openai.resources.chat.completions.Completions.create")
    def test_openai_translate(self, mock_openai_create):
        translated_content = "Translated content"
        mock_openai_create.return_value = ChatCompletion(
            id="id",
            model="any-model",
            created=int(time.time()),
            object="chat.completion",
            choices=[
                Choice(
                    finish_reason="stop",
                    index=0,
                    message=ChatCompletionMessage(
                        content=translated_content, role="assistant"
                    ),
                )
            ],
        )

        result = self.translator.translate("en", "Raw content")
        assert result == translated_content

    @patch("openai.resources.chat.completions.Completions.create")
    def test_openai_batch_translate(self, mock_openai_create):
        translated_obj = {
            "title": "Translated title",
            "description": "Translated description",
            "body": "Translated body",
        }
        mock_openai_create.return_value = ChatCompletion(
            id="id",
            model="any-model",
            created=int(time.time()),
            object="chat.completion",
            choices=[
                Choice(
                    finish_reason="stop",
                    index=0,
                    message=ChatCompletionMessage(
                        content=json.dumps(translated_obj), role="assistant"
                    ),
                )
            ],
        )
        obj_to_translate = {
            "title": "title",
            "description": "description",
            "body": "body",
        }
        batches = {
            "ro": obj_to_translate,
            "vi": obj_to_translate,
        }
        result = self.translator.batch_translate(batches)
        assert result == {"vi": translated_obj, "ro": translated_obj}

    @patch("openai.resources.chat.completions.Completions.create")
    def test_process(self, mock_openai_create):
        def mock_open_ai_create_side_effect(**kwargs):
            messages = kwargs["messages"]
            trans_lang = re.search(r"into (.*) \(", messages[0]["content"]).group(1)
            obj_to_translate = json.loads(messages[1]["content"])
            translated_obj = {
                k: f"Translated {trans_lang}: {v}" for k, v in obj_to_translate.items()
            }
            return ChatCompletion(
                id="id",
                model="any-model",
                created=int(time.time()),
                object="chat.completion",
                choices=[
                    Choice(
                        finish_reason="stop",
                        index=0,
                        message=ChatCompletionMessage(
                            content=json.dumps(translated_obj), role="assistant"
                        ),
                    )
                ],
            )

        mock_openai_create.side_effect = mock_open_ai_create_side_effect

        self.translator.process()

        self.instance.refresh_from_db()
        base_lang = settings.LANGUAGE_CODE
        for lang, _code in settings.LANGUAGES:
            if lang == base_lang:
                continue
            assert (
                getattr(self.instance.title, lang)
                == f"Translated {lang}: {getattr(self.instance.title, base_lang)}"
            )
