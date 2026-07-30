from __future__ import annotations

from app.services.chat.intent_detector import ChatIntent


class QueryRouter:
    """
    Determines which database entities should be loaded
    based on the detected chat intent.
    """

    def get_required_context(self, intent: ChatIntent) -> dict[str, bool]:
        return {
            "temples": intent == ChatIntent.TEMPLE,
            "poojas": intent == ChatIntent.POOJA,
            "priests": intent == ChatIntent.PRIEST,
            "bookings": intent == ChatIntent.BOOKING,
            "payments": intent == ChatIntent.PAYMENT,
            "kundli": intent == ChatIntent.KUNDLI,
            "catering": intent == ChatIntent.CATERING,
            "consultation": intent == ChatIntent.CONSULTATION,
            "general": intent == ChatIntent.GENERAL,
        }