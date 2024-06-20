import asyncio
import json
import logging
from functools import cache
from inspect import isclass

from django.conf import settings
from localized_fields.models import LocalizedModel

from headless_cms.auto_translate.base_translate import BaseTranslate
from headless_cms.settings import headless_cms_settings

_openai_client = headless_cms_settings.OPENAI_CLIENT
openai_client = _openai_client() if isclass(_openai_client) else _openai_client

system_prompt = f"""
You are a professional translator. Please translate and paraphrase (if needed) this content into {{lang}} language \
with friendly tone, concise and easy to understand. Just translate the content only, keep the HTML, markdown tag, link\
, the content between <getattr><getattr/> as it is, and keep the proper nouns as it is, too. You just response me with translated content only, do not \
add any additional comment or explanation.
Additionally, keep these term as it is: {str(headless_cms_settings.AUTO_TRANSLATE_IGNORES)}.
Here is your content:
"""

system_batch_translate_prompt = f"""
You are a professional translator. Please translate and paraphrase (if needed) this json object into {{lang}} language \
with friendly tone, concise and easy to understand. Just translate the content only, keep the HTML, markdown tag, link\
, the content between <getattr><getattr/> as it is, and keep the proper nouns as it is, too. You just response me with translated json object only, do not \
add any additional comment or explanation.
Additionally, keep these term as it is: {str(headless_cms_settings.AUTO_TRANSLATE_IGNORES)}.
Here is your json object:
"""

continue_prompt = "Continue the work for me. WRITE the next response as you are working, continue from the previous one."


@cache
def _get_language_map():
    return dict(settings.LANGUAGES)


logger = logging.getLogger("headless_cms")


class OpenAITranslate(BaseTranslate):
    """
    Translation class using OpenAI's chat model.

    This class extends the BaseTranslate class to provide translation functionality
    using OpenAI's chat model. It supports both single and batch translations.
    """

    can_batch_translate = True

    def __init__(self, instance: LocalizedModel):
        super().__init__(instance)

    def translate(self, language, text):
        """
        Translate text to a single language using OpenAI's chat model.

        Args:
            language (str): The target language code.
            text (str): The text to be translated.

        Returns:
            str: The translated text.
        """
        lang_name = _get_language_map().get(language)
        lang = language + f" ({lang_name})" if lang_name else ""
        prompts = [
            {"role": "system", "content": system_prompt.replace("{lang}", lang)},
            {"role": "user", "content": text},
        ]
        res = openai_client.chat.completions.create(
            model=headless_cms_settings.OPENAI_CHAT_MODEL,
            temperature=0.3,
            messages=prompts,
        )
        translated_content = res.choices[0].message.content
        return translated_content

    def chat_gpt_translate(self, prompts):
        prompts = list(prompts)
        res = openai_client.chat.completions.create(
            model=headless_cms_settings.OPENAI_CHAT_MODEL,
            temperature=0.7,
            messages=prompts,
            response_format={"type": "json_object"},
        )
        finish_reason = res.choices[0].finish_reason
        content = res.choices[0].message.content

        while finish_reason != "stop":
            prompts.extend(
                [
                    res.choices[0].message,
                    {"role": "user", "content": continue_prompt},
                ]
            )
            res = openai_client.chat.completions.create(
                model="gpt-4-turbo",
                temperature=0.3,
                messages=prompts,
            )
            content += res.choices[0].message.content
            finish_reason = res.choices[0].finish_reason

        try:
            return json.loads(content, strict=False)
        except json.decoder.JSONDecodeError as e:
            logger.error(e)
            return {}

    async def _async_translate(self, prompts_list):
        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(None, self.chat_gpt_translate, prompts)
            for prompts in prompts_list
        ]
        result = await asyncio.gather(*futures)
        return result

    def batch_translate(self, batches: dict[str, dict]):
        """
        Batch translate multiple fields to multiple languages using OpenAI's chat model.

        Args:
            batches (dict[str, dict]): A dictionary where keys are language codes and values
                are dictionaries mapping field names to text to be translated.

        Returns:
            dict[str, dict]: A dictionary where keys are language codes and values are
                dictionaries mapping field names to translated text.
        """
        langs = []
        prompt_list = []
        for language, obj_to_translate in batches.items():
            langs.append(language)
            lang_name = _get_language_map().get(language)
            lang = language + f" ({lang_name})" if lang_name else ""
            prompt_list.append(
                [
                    {
                        "role": "system",
                        "content": system_batch_translate_prompt.replace(
                            "{lang}", lang
                        ),
                    },
                    {"role": "user", "content": json.dumps(obj_to_translate)},
                ]
            )

        translated_objs = asyncio.run(self._async_translate(prompt_list))

        res = {lang: translated_objs[idx] for idx, lang in enumerate(langs)}

        return res
