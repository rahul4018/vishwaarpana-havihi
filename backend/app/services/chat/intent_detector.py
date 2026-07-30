from __future__ import annotations

from enum import Enum


class ChatIntent(str, Enum):
    TEMPLE = "TEMPLE"
    POOJA = "POOJA"
    PRIEST = "PRIEST"
    BOOKING = "BOOKING"
    PAYMENT = "PAYMENT"
    KUNDLI = "KUNDLI"
    CATERING = "CATERING"
    CONSULTATION = "CONSULTATION"
    GENERAL = "GENERAL"


class IntentDetector:
    """
    Simple keyword-based intent detector.
    """

    def detect(self, message: str) -> ChatIntent:
        text = message.lower()

        if any(word in text for word in [
            "temple", "mandir", "location", "address", "city"
        ]):
            return ChatIntent.TEMPLE

        if any(word in text for word in [
            "pooja", "puja", "ritual", "homa", "havan"
        ]):
            return ChatIntent.POOJA

        if any(word in text for word in [
            "priest", "pandit", "guru", "archaka"
        ]):
            return ChatIntent.PRIEST

        if any(word in text for word in [
            "booking", "book", "reserve"
        ]):
            return ChatIntent.BOOKING

        if any(word in text for word in [
            "payment", "pay", "invoice", "receipt"
        ]):
            return ChatIntent.PAYMENT

        if "kundli" in text:
            return ChatIntent.KUNDLI

        if any(word in text for word in [
            "food", "prasadam", "catering"
        ]):
            return ChatIntent.CATERING

        if any(word in text for word in [
            "consult", "consultation", "astrology"
        ]):
            return ChatIntent.CONSULTATION

        return ChatIntent.GENERAL