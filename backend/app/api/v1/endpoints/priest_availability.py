from __future__ import annotations

from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies.auth import require_roles
from app.db.database import get_db
from app.schemas.priest_availability import (
    CreatePriestAvailabilityRequest,
    PriestAvailabilityResponse,
    UpdatePriestAvailabilityRequest,
)
from app.services.priest_availability_service import (
    PriestAvailabilityService,
)

router = APIRouter(
    prefix="/priest-availability",
    tags=["Priest Availability"],
)


@router.get(
    "",
    response_model=list[PriestAvailabilityResponse],
)
def get_all(
    db: Session = Depends(get_db),
):
    return PriestAvailabilityService(db).get_all()


@router.get(
    "/{availability_id}",
    response_model=PriestAvailabilityResponse,
)
def get_by_id(
    availability_id: UUID,
    db: Session = Depends(get_db),
):
    return PriestAvailabilityService(db).get_by_id(
        availability_id
    )


@router.get(
    "/priest/{priest_id}",
    response_model=list[PriestAvailabilityResponse],
)
def get_by_priest(
    priest_id: UUID,
    db: Session = Depends(get_db),
):
    return PriestAvailabilityService(db).get_by_priest(
        priest_id
    )


@router.get(
    "/date/{available_date}",
    response_model=list[PriestAvailabilityResponse],
)
def get_by_date(
    available_date: date,
    db: Session = Depends(get_db),
):
    return PriestAvailabilityService(db).get_by_date(
        available_date
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=PriestAvailabilityResponse,
)
def create(
    request: CreatePriestAvailabilityRequest,
    db: Session = Depends(get_db),
    _: dict = Depends(
        require_roles(
            "SUPER_ADMIN",
            "ADMIN",
            "TEMPLE_ADMIN",
        )
    ),
):
    return PriestAvailabilityService(db).create(
        request
    )


@router.put(
    "/{availability_id}",
    response_model=PriestAvailabilityResponse,
)
def update(
    availability_id: UUID,
    request: UpdatePriestAvailabilityRequest,
    db: Session = Depends(get_db),
    _: dict = Depends(
        require_roles(
            "SUPER_ADMIN",
            "ADMIN",
            "TEMPLE_ADMIN",
        )
    ),
):
    return PriestAvailabilityService(db).update(
        availability_id,
        request,
    )


@router.delete(
    "/{availability_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete(
    availability_id: UUID,
    db: Session = Depends(get_db),
    _: dict = Depends(
        require_roles(
            "SUPER_ADMIN",
            "ADMIN",
            "TEMPLE_ADMIN",
        )
    ),
):
    PriestAvailabilityService(db).delete(
        availability_id
    )