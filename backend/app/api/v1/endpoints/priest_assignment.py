from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies.auth import require_roles
from app.db.database import get_db
from app.schemas.priest_assignment import (
    CreatePriestAssignmentRequest,
    PriestAssignmentResponse,
    UpdatePriestAssignmentRequest,
)
from app.services.priest_assignment_service import (
    PriestAssignmentService,
)

router = APIRouter(
    prefix="/priest-assignments",
    tags=["Priest Assignment"],
)


@router.get(
    "",
    response_model=list[PriestAssignmentResponse],
)
def get_all_assignments(
    db: Session = Depends(get_db),
):
    return PriestAssignmentService(db).get_all()


@router.get(
    "/{assignment_id}",
    response_model=PriestAssignmentResponse,
)
def get_assignment(
    assignment_id: UUID,
    db: Session = Depends(get_db),
):
    return PriestAssignmentService(db).get_by_id(
        assignment_id
    )


@router.get(
    "/booking/{booking_id}",
    response_model=PriestAssignmentResponse,
)
def get_booking_assignment(
    booking_id: UUID,
    db: Session = Depends(get_db),
):
    return PriestAssignmentService(db).get_by_booking(
        booking_id
    )


@router.get(
    "/priest/{priest_id}",
    response_model=list[PriestAssignmentResponse],
)
def get_priest_assignments(
    priest_id: UUID,
    db: Session = Depends(get_db),
):
    return PriestAssignmentService(db).get_by_priest(
        priest_id
    )


@router.post(
    "",
    response_model=PriestAssignmentResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(
            require_roles(
                "ADMIN",
                "SUPER_ADMIN",
            )
        )
    ],
)
def create_assignment(
    request: CreatePriestAssignmentRequest,
    db: Session = Depends(get_db),
):
    return PriestAssignmentService(db).create(
        request
    )


@router.put(
    "/{assignment_id}",
    response_model=PriestAssignmentResponse,
    dependencies=[
        Depends(
            require_roles(
                "ADMIN",
                "SUPER_ADMIN",
            )
        )
    ],
)
def update_assignment(
    assignment_id: UUID,
    request: UpdatePriestAssignmentRequest,
    db: Session = Depends(get_db),
):
    return PriestAssignmentService(db).update(
        assignment_id,
        request,
    )


@router.delete(
    "/{assignment_id}",
    dependencies=[
        Depends(
            require_roles(
                "ADMIN",
                "SUPER_ADMIN",
            )
        )
    ],
)
def delete_assignment(
    assignment_id: UUID,
    db: Session = Depends(get_db),
):
    return PriestAssignmentService(db).delete(
        assignment_id
    )