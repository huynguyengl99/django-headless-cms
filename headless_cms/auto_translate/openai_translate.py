import json

from localized_fields.models import LocalizedModel
from openai import OpenAI

from headless_cms.auto_translate.base_translate import BaseTranslate
from headless_cms.settings import headless_cms_settings

client = OpenAI()

system_prompt = f"""
You are a professional translator. Please translate and paraphrase (if needed) this content into {{lang}} language \
with friendly tone, concise and easy to understand. Just translate the content only, keep the HTML or markdown \
tag as it is. You just response me with translated content only, do not add any additional comment or explanation.
Additionally, keep these term as it is: {str(headless_cms_settings.AUTO_TRANSLATE_IGNORES)}.
Here is your content:
"""

system_batch_translate_prompt = f"""
You are a professional translator. Please translate and paraphrase (if needed) this json object into {{lang}} language \
with friendly tone, concise and easy to understand. Just translate the content only, keep the HTML or markdown \
tag as it is. You just response me with translated json object only, do not add any additional comment or explanation.
Additionally, keep these term as it is: {str(headless_cms_settings.AUTO_TRANSLATE_IGNORES)}.
Here is your json object:
"""


class OpenAITranslate(BaseTranslate):
    can_translate_object = True

    def __init__(self, instance: LocalizedModel, openai_client=client):
        super().__init__(instance)
        self.openai_client = openai_client

    def translate(self, language, text):
        prompts = [
            {"role": "system", "content": system_prompt.replace("{lang}", language)},
            {"role": "user", "content": text},
        ]
        res = self.openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            temperature=0.3,
            messages=prompts,
        )
        translated_content = res.choices[0].message.content
        return translated_content

    def batch_translate(self, language: str, obj_to_translate: dict):
        prompts = [
            {
                "role": "system",
                "content": system_batch_translate_prompt.replace("{lang}", language),
            },
            {"role": "user", "content": json.dumps(obj_to_translate)},
        ]

        res = self.openai_client.chat.completions.create(
            model="gpt-4-turbo",
            temperature=0.7,
            messages=prompts,
            response_format={"type": "json_object"},
        )
        translated_content = res.choices[0].message.content
        return json.loads(translated_content)
