from __future__ import annotations

from sqlalchemy.orm import Session

from app.db.models.pooja import Pooja
from app.db.models.priest import Priest
from app.db.models.temple import Temple


class ContextService:
    """
    Loads only the database information requested
    by the QueryRouter.
    """

    def __init__(self, db: Session):
        self.db = db

    def build_context(
        self,
        required: dict[str, bool],
    ) -> str:

        context: list[str] = []

        # -------------------------
        # Temples
        # -------------------------
        if required.get("temples"):
            temples = (
                self.db.query(Temple)
                .filter(Temple.is_active.is_(True))
                .all()
            )

            context.append("TEMPLES")

            if temples:
                for temple in temples:
                    context.append(
                        f"""
Temple Name: {temple.name}
City: {temple.city}
State: {temple.state}
Address: {temple.address}
Description: {temple.description or "N/A"}
"""
                    )
            else:
                context.append("No temples available.")

        # -------------------------
        # Poojas
        # -------------------------
        if required.get("poojas"):
            poojas = (
                self.db.query(Pooja)
                .filter(Pooja.is_active.is_(True))
                .all()
            )

            context.append("\nPOOJAS")

            if poojas:
                for pooja in poojas:
                    context.append(
                        f"""
Pooja: {pooja.name}
Temple: {pooja.temple.name}
Price: ₹{pooja.price}
Duration: {pooja.duration_minutes} minutes
Description: {pooja.description or "N/A"}
"""
                    )
            else:
                context.append("No poojas available.")

        # -------------------------
        # Priests
        # -------------------------
        if required.get("priests"):
            priests = (
                self.db.query(Priest)
                .filter(Priest.is_active.is_(True))
                .all()
            )

            context.append("\nPRIESTS")

            if priests:
                for priest in priests:
                    context.append(
                        f"""
Priest: {priest.full_name}
Temple: {priest.temple.name}
Experience: {priest.experience_years} years
Specialization: {priest.specialization or "General"}
"""
                    )
            else:
                context.append("No priests available.")

        return "\n".join(context)