from __future__ import annotations

from sqlalchemy.orm import Session

from app.db.models.temple import Temple
from app.db.models.pooja import Pooja
from app.db.models.priest import Priest


class ChatContextService:
    """
    Builds database context for Gemini.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_database_context(self) -> str:
        lines: list[str] = []

        # -------------------------
        # Temples
        # -------------------------

        temples = (
            self.db.query(Temple)
            .filter(Temple.is_active.is_(True))
            .all()
        )

        lines.append("TEMPLES")

        if temples:
            for temple in temples:
                lines.append(
                    f"""
Temple Name: {temple.name}
City: {temple.city}
State: {temple.state}
Address: {temple.address}
Description: {temple.description or "N/A"}
"""
                )
        else:
            lines.append("No temples available.")

        # -------------------------
        # Poojas
        # -------------------------

        poojas = (
            self.db.query(Pooja)
            .filter(Pooja.is_active.is_(True))
            .all()
        )

        lines.append("\nPOOJAS")

        if poojas:
            for pooja in poojas:
                lines.append(
                    f"""
Pooja: {pooja.name}
Temple: {pooja.temple.name}
Price: ₹{pooja.price}
Duration: {pooja.duration_minutes} minutes
Description: {pooja.description or "N/A"}
"""
                )
        else:
            lines.append("No poojas available.")

        # -------------------------
        # Priests
        # -------------------------

        priests = (
            self.db.query(Priest)
            .filter(Priest.is_active.is_(True))
            .all()
        )

        lines.append("\nPRIESTS")

        if priests:
            for priest in priests:
                lines.append(
                    f"""
Priest: {priest.full_name}
Temple: {priest.temple.name}
Experience: {priest.experience_years} years
Specialization: {priest.specialization or "General"}
"""
                )
        else:
            lines.append("No priests available.")

        return "\n".join(lines)