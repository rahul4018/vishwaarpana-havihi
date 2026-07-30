from __future__ import annotations

from typing import Any

from google import genai

from app.core.config import settings


class AIChatService:
    """
    Google Gemini AI service.
    """

    def __init__(self) -> None:
        if not settings.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is missing."
            )

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
        )

        self.model_name = settings.GEMINI_MODEL

    def get_system_prompt(self) -> str:
        return """
You are Vishwaarpana Havihi AI Assistant.

You help devotees with:

- Temples
- Poojas
- Priests
- Bookings
- Catering
- Kundli
- Consultation
- Payments
- Invoices

You MUST always use the database information provided.

Never invent temples.

Never invent poojas.

Never invent priests.

If the answer is not available in the provided database information,
clearly say that it is unavailable.

Always answer politely.
"""

    def build_prompt(
        self,
        database_context: str,
        conversation_history: list[dict[str, str]],
        user_message: str,
    ) -> str:

        history = ""

        for message in conversation_history:
            history += (
                f"{message['role'].upper()}: "
                f"{message['content']}\n"
            )

        return f"""
{self.get_system_prompt()}

=================================================
DATABASE INFORMATION
=================================================

{database_context}

=================================================
CONVERSATION
=================================================

{history}

USER:
{user_message}

ASSISTANT:
"""

    def generate_response(
        self,
        database_context: str,
        conversation_history: list[dict[str, str]],
        user_message: str,
    ) -> dict[str, Any]:

        if not user_message.strip():
            raise ValueError(
                "User message cannot be empty."
            )

        prompt = self.build_prompt(
            database_context=database_context,
            conversation_history=conversation_history,
            user_message=user_message,
        )

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )

        text = (
            response.text.strip()
            if response.text
            else "No response generated."
        )

        return {
            "content": text,
            "model_name": self.model_name,
        }