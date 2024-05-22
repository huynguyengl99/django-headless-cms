import asyncio
import json
from inspect import isclass

from localized_fields.models import LocalizedModel

from headless_cms.auto_translate.base_translate import BaseTranslate
from headless_cms.settings import headless_cms_settings

_openai_client = headless_cms_settings.OPENAI_CLIENT
openai_client = _openai_client() if isclass(_openai_client) else _openai_client

system_prompt = f"""
You are a professional translator. Please translate and paraphrase (if needed) this content into {{lang}} language \
with friendly tone, concise and easy to understand. Just translate the content only, keep the HTML, markdown \
tag, the content between <getattr><getattr/> as it is, and keep the proper nouns as it is, too. You just response me with translated content only, do not \
add any additional comment or explanation.
Additionally, keep these term as it is: {str(headless_cms_settings.AUTO_TRANSLATE_IGNORES)}.
Here is your content:
"""

system_batch_translate_prompt = f"""
You are a professional translator. Please translate and paraphrase (if needed) this json object into {{lang}} language \
with friendly tone, concise and easy to understand. Just translate the content only, keep the HTML, markdown \
tag, the content between <getattr><getattr/> as it is, and keep the proper nouns as it is, too. You just response me with translated json object only, do not \
add any additional comment or explanation.
Additionally, keep these term as it is: {str(headless_cms_settings.AUTO_TRANSLATE_IGNORES)}.
Here is your json object:
"""


class OpenAITranslate(BaseTranslate):
    can_batch_translate = True

    def __init__(self, instance: LocalizedModel):
        super().__init__(instance)

    def translate(self, language, text):
        prompts = [
            {"role": "system", "content": system_prompt.replace("{lang}", language)},
            {"role": "user", "content": text},
        ]
        res = openai_client.chat.completions.create(
            model=headless_cms_settings.OPENAI_CHAT_MODEL,
            temperature=0.3,
            messages=prompts,
        )
        translated_content = res.choices[0].message.content
        return translated_content

    def chat_gpt_translate(self, prompt):
        res = openai_client.chat.completions.create(
            model=headless_cms_settings.OPENAI_CHAT_MODEL,
            temperature=0.7,
            messages=prompt,
            response_format={"type": "json_object"},
        )
        translated_content = res.choices[0].message.content
        return json.loads(translated_content)

    async def _async_translate(self, prompt_list):
        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(None, self.chat_gpt_translate, prompt)
            for prompt in prompt_list
        ]
        result = await asyncio.gather(*futures)
        return result

    def batch_translate(self, batches: dict[str, dict]):
        langs = []
        prompt_list = []
        for language, obj_to_translate in batches.items():
            langs.append(language)
            prompt_list.append(
                [
                    {
                        "role": "system",
                        "content": system_batch_translate_prompt.replace(
                            "{lang}", language
                        ),
                    },
                    {"role": "user", "content": json.dumps(obj_to_translate)},
                ]
            )

        translated_objs = asyncio.run(self._async_translate(prompt_list))

        res = {lang: translated_objs[idx] for idx, lang in enumerate(langs)}

        return res
