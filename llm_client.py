# llm_client.py (new SDK version)
from __future__ import annotations

import logging
import os
from typing import Dict, List, Optional

from pydantic import BaseModel, Field
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

# New OpenAI SDK import
from openai import OpenAI

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class LLMConfig(BaseModel):
    provider: str = Field("openai")
    model: str = Field("gpt-4o-mini")
    temperature: float = Field(0.2, ge=0.0, le=1.0)
    max_tokens: int = Field(512, ge=1, le=4096)
    system_prompt: str = Field(
        "You are a helpful, concise customer support assistant. "
        "Answer as a professional support agent using clear, actionable language."
    )


class LLMClient:
    def __init__(self, config: LLMConfig, api_key: Optional[str]):
        self.config = config
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is required but not provided.")
        # instantiate new SDK client
        self.client = OpenAI(api_key=self.api_key)

    def _build_messages(
        self,
        user_query: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        extra_context: Optional[str] = None,
    ) -> List[Dict[str, str]]:
        messages: List[Dict[str, str]] = []
        messages.append({"role": "system", "content": self.config.system_prompt})
        if extra_context:
            messages.append({"role": "system", "content": f"Context: {extra_context}"})
        if conversation_history:
            messages.extend(conversation_history)
        messages.append({"role": "user", "content": user_query})
        return messages

    @retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type(Exception),
    )
    def _call_openai(self, messages: List[Dict[str, str]]) -> str:
        """
        New SDK call pattern: client.chat.completions.create(...)
        """
        try:
            resp = self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
            )
            # New SDK returns choices[0].message.content
            return resp.choices[0].message.content.strip()
        except Exception:
            logger.exception("LLM call failed")
            raise

    def generate_response(
        self,
        user_query: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        extra_context: Optional[str] = None,
    ) -> str:
        try:
            messages = self._build_messages(user_query, conversation_history, extra_context)
            return self._call_openai(messages)
        except Exception as exc:
            logger.exception("Error generating LLM response")
            return (
                "⚠️ An error occurred while contacting the LLM backend. "
                f"Error: {type(exc).__name__}: {str(exc)[:200]}"
            )
