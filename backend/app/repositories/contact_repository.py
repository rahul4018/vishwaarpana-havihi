from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.contact import Contact


class ContactRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Contact]:
        return (
            self.db.query(Contact)
            .order_by(Contact.created_at.desc())
            .all()
        )

    def get_by_id(
        self,
        contact_id: UUID,
    ) -> Contact | None:
        return (
            self.db.query(Contact)
            .filter(Contact.id == contact_id)
            .first()
        )

    def get_by_status(
        self,
        enquiry_status: str,
    ) -> list[Contact]:
        return (
            self.db.query(Contact)
            .filter(
                Contact.enquiry_status == enquiry_status
            )
            .order_by(Contact.created_at.desc())
            .all()
        )

    def create(
        self,
        contact: Contact,
    ) -> Contact:
        self.db.add(contact)
        self.db.commit()
        self.db.refresh(contact)

        return contact

    def update(
        self,
        contact: Contact,
    ) -> Contact:
        self.db.commit()
        self.db.refresh(contact)

        return contact

    def delete(
        self,
        contact: Contact,
    ) -> None:
        self.db.delete(contact)
        self.db.commit()