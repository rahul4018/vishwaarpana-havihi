from enum import Enum


class QuotationStatus(str, Enum):
    DRAFT = "DRAFT"

    SENT = "SENT"

    VIEWED = "VIEWED"

    ACCEPTED = "ACCEPTED"

    REJECTED = "REJECTED"

    EXPIRED = "EXPIRED"

    CANCELLED = "CANCELLED"