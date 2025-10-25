"""OpenAI"""

# flake8: noqa=E501

from typing import Optional

from django.conf import settings
from openai import OpenAI
from openai.types.chat import ChatCompletion
from pydantic import BaseModel


class CompletionUsage(BaseModel):
    """Completion usage"""

    completion_tokens: int
    prompt_tokens: int
    total_tokens: int


def get_openapi_client():
    """Get OpenAPI client"""
    oa_client = OpenAI(api_key=settings.OPENAPI_API_KEY)
    return oa_client


def get_completion_usage(completion: ChatCompletion) -> Optional[CompletionUsage]:
    """Get completion usage"""

    if completion.usage:
        return CompletionUsage(
            completion_tokens=completion.usage.completion_tokens,
            prompt_tokens=completion.usage.prompt_tokens,
            total_tokens=completion.usage.total_tokens,
        )

    return None


def openai_completion(user_prompt: str, system_prompt: Optional[str] = None):
    """Chat completion"""
    oa_client = get_openapi_client()

    messages = []

    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    messages.append({"role": "user", "content": user_prompt})

    completion: ChatCompletion = oa_client.chat.completions.create(
        model="gpt-4o-mini", messages=messages
    )

    response = completion.choices[0].message.content

    return completion, response
