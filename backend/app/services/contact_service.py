from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions.http_exceptions import ResourceNotFoundError
from app.db.models.contact import Contact
from app.repositories import ContactRepository
from app.schemas import (
    CreateContactRequest,
    UpdateContactRequest,
)


class ContactService:
    def __init__(self, db: Session):
        self.repository = ContactRepository(db)

    def get_all(self) -> list[Contact]:
        return self.repository.get_all()

    def get_by_id(
        self,
        contact_id: str,
    ) -> Contact:
        contact = self.repository.get_by_id(
            UUID(contact_id)
        )

        if not contact:
            raise ResourceNotFoundError(
                "Contact enquiry not found"
            )

        return contact

    def get_by_status(
        self,
        enquiry_status: str,
    ) -> list[Contact]:
        return self.repository.get_by_status(
            enquiry_status.upper()
        )

    def create(
        self,
        request: CreateContactRequest,
    ) -> Contact:
        contact = Contact(
            name=request.name,
            email=str(request.email),
            phone=request.phone,
            subject=request.subject,
            message=request.message,
            enquiry_status="NEW",
        )

        return self.repository.create(contact)

    def update(
        self,
        contact_id: str,
        request: UpdateContactRequest,
    ) -> Contact:
        contact = self.get_by_id(contact_id)

        update_data = request.model_dump(
            exclude_unset=True
        )

        if "enquiry_status" in update_data:
            status_value = update_data[
                "enquiry_status"
            ]

            if status_value is not None:
                update_data[
                    "enquiry_status"
                ] = status_value.upper()

        for field, value in update_data.items():
            setattr(
                contact,
                field,
                value,
            )

        return self.repository.update(contact)

    def delete(
        self,
        contact_id: str,
    ) -> None:
        contact = self.get_by_id(contact_id)

        self.repository.delete(contact)