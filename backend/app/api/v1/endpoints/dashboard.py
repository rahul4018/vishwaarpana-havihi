from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.dependencies.auth import get_current_user
from app.db.database import get_db
from app.db.models.booking import Booking
from app.db.models.pooja import Pooja
from app.db.models.priest import Priest
from app.db.models.temple import Temple
from app.db.models.user import User

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/stats",
    summary="Dashboard statistics",
)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    total_temples = db.query(func.count(Temple.id)).scalar() or 0
    total_priests = db.query(func.count(Priest.id)).scalar() or 0
    total_poojas = db.query(func.count(Pooja.id)).scalar() or 0
    total_bookings = db.query(func.count(Booking.id)).scalar() or 0

    return {
        "success": True,
        "data": {
            "total_temples": total_temples,
            "total_priests": total_priests,
            "total_poojas": total_poojas,
            "total_bookings": total_bookings,
            "total_revenue": 0,
        },
    }