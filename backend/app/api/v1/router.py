from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.booking import router as booking_router
from app.api.v1.endpoints.booking_quotation import (
    router as booking_quotation_router,
)
from app.api.v1.endpoints.booking_workflow import (
    router as booking_workflow_router,
)
from app.api.v1.endpoints.catering import router as catering_router
from app.api.v1.endpoints.category import router as category_router
from app.api.v1.endpoints.chat import router as chat_router
from app.api.v1.endpoints.contact import router as contact_router
from app.api.v1.endpoints.dashboard import router as dashboard_router
from app.api.v1.endpoints.gallery import router as gallery_router
from app.api.v1.endpoints.invoice import router as invoice_router
from app.api.v1.endpoints.kundli import router as kundli_router
from app.api.v1.endpoints.notification import router as notification_router
from app.api.v1.endpoints.payment import router as payment_router
from app.api.v1.endpoints.pooja import router as pooja_router
from app.api.v1.endpoints.priest import router as priest_router
from app.api.v1.endpoints.priest_assignment import (
    router as priest_assignment_router,
)
from app.api.v1.endpoints.priest_availability import (
    router as priest_availability_router,
)
from app.api.v1.endpoints.review import router as review_router
from app.api.v1.endpoints.role import router as role_router
from app.api.v1.endpoints.temple import router as temple_router
from app.api.v1.endpoints.users import router as users_router

api_router = APIRouter()

# Authentication
api_router.include_router(auth_router)

# Master Data
api_router.include_router(role_router)
api_router.include_router(temple_router)
api_router.include_router(category_router)
api_router.include_router(priest_router)
api_router.include_router(priest_availability_router)
api_router.include_router(priest_assignment_router)
api_router.include_router(pooja_router)

# Booking
api_router.include_router(booking_router)
api_router.include_router(booking_workflow_router)
api_router.include_router(booking_quotation_router)

# Payment & Invoice
api_router.include_router(payment_router)
api_router.include_router(invoice_router)

# Gallery
api_router.include_router(gallery_router)

# Notification
api_router.include_router(notification_router)

# Review
api_router.include_router(review_router)

# Contact
api_router.include_router(contact_router)

# Catering
api_router.include_router(catering_router)

# Kundli
api_router.include_router(kundli_router)

# AI Chat
api_router.include_router(chat_router)

# Dashboard
api_router.include_router(dashboard_router)

# Users
api_router.include_router(users_router)