from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
)

from app.schemas.booking import (
    BookingResponse,
    CreateBookingRequest,
    UpdateBookingRequest,
)

from app.schemas.booking_quotation import (
    BookingQuotationResponse,
    CreateBookingQuotationRequest,
    UpdateBookingQuotationRequest,
)

from app.schemas.catering import (
    CateringResponse,
    CreateCateringRequest,
    UpdateCateringRequest,
)

from app.schemas.category import (
    CategoryResponse,
    CreateCategoryRequest,
    UpdateCategoryRequest,
)

from app.schemas.chat import (
    ChatAskResponse,
    ChatConversationResponse,
    ChatMessageResponse,
    CreateConversationRequest,
    SendMessageRequest,
)

from app.schemas.consultation import (
    ConsultationResponse,
    CreateConsultationRequest,
    ManageConsultationRequest,
    UpdateConsultationRequest,
)

from app.schemas.contact import (
    ContactResponse,
    CreateContactRequest,
    UpdateContactRequest,
)

from app.schemas.gallery import (
    CreateGalleryRequest,
    GalleryResponse,
    UpdateGalleryRequest,
)

from app.schemas.invoice import (
    CreateInvoiceRequest,
    InvoiceResponse,
    UpdateInvoiceRequest,
)

from app.schemas.kundli import (
    CreateKundliRequest,
    KundliResponse,
    ManageKundliRequest,
    UpdateKundliRequest,
)

from app.schemas.notification import (
    CreateNotificationRequest,
    NotificationResponse,
    UpdateNotificationRequest,
)

from app.schemas.payment import (
    CreatePaymentRequest,
    PaymentResponse,
    UpdatePaymentRequest,
)

from app.schemas.pooja import (
    CreatePoojaRequest,
    PoojaResponse,
    UpdatePoojaRequest,
)

from app.schemas.priest import (
    CreatePriestRequest,
    PriestResponse,
    UpdatePriestRequest,
)

from app.schemas.priest_assignment import (
    CreatePriestAssignmentRequest,
    PriestAssignmentResponse,
    UpdatePriestAssignmentRequest,
)

from app.schemas.priest_availability import (
    CreatePriestAvailabilityRequest,
    PriestAvailabilityResponse,
    UpdatePriestAvailabilityRequest,
)

from app.schemas.review import (
    CreateReviewRequest,
    ModerateReviewRequest,
    ReviewResponse,
    UpdateReviewRequest,
)

from app.schemas.role import (
    RoleResponse,
)

from app.schemas.temple import (
    CreateTempleRequest,
    TempleResponse,
    UpdateTempleRequest,
)

from app.schemas.user import (
    CreateUserRequest,
    UpdateUserRequest,
    UserResponse,
)

__all__ = [
    # Authentication
    "LoginRequest",
    "LoginResponse",
    "RefreshTokenRequest",
    "RefreshTokenResponse",
    "RegisterRequest",
    "RegisterResponse",
    "TokenResponse",

    # Temple
    "CreateTempleRequest",
    "TempleResponse",
    "UpdateTempleRequest",

    # Category
    "CategoryResponse",
    "CreateCategoryRequest",
    "UpdateCategoryRequest",

    # Role
    "RoleResponse",

    # Priest
    "CreatePriestRequest",
    "PriestResponse",
    "UpdatePriestRequest",

    # Priest Assignment
    "CreatePriestAssignmentRequest",
    "UpdatePriestAssignmentRequest",
    "PriestAssignmentResponse",

    # Priest Availability
    "CreatePriestAvailabilityRequest",
    "UpdatePriestAvailabilityRequest",
    "PriestAvailabilityResponse",

    # Pooja
    "CreatePoojaRequest",
    "PoojaResponse",
    "UpdatePoojaRequest",

    # Booking
    "BookingResponse",
    "CreateBookingRequest",
    "UpdateBookingRequest",

    # Booking Quotation
    "CreateBookingQuotationRequest",
    "UpdateBookingQuotationRequest",
    "BookingQuotationResponse",

    # Payment
    "CreatePaymentRequest",
    "PaymentResponse",
    "UpdatePaymentRequest",

    # Invoice
    "CreateInvoiceRequest",
    "InvoiceResponse",
    "UpdateInvoiceRequest",

    # Gallery
    "CreateGalleryRequest",
    "GalleryResponse",
    "UpdateGalleryRequest",

    # Notification
    "CreateNotificationRequest",
    "NotificationResponse",
    "UpdateNotificationRequest",

    # Review
    "CreateReviewRequest",
    "ModerateReviewRequest",
    "ReviewResponse",
    "UpdateReviewRequest",

    # Contact
    "ContactResponse",
    "CreateContactRequest",
    "UpdateContactRequest",

    # Catering
    "CateringResponse",
    "CreateCateringRequest",
    "UpdateCateringRequest",

    # Kundli
    "CreateKundliRequest",
    "KundliResponse",
    "ManageKundliRequest",
    "UpdateKundliRequest",

    # Consultation
    "ConsultationResponse",
    "CreateConsultationRequest",
    "ManageConsultationRequest",
    "UpdateConsultationRequest",

    # Chat
    "ChatAskResponse",
    "ChatConversationResponse",
    "ChatMessageResponse",
    "CreateConversationRequest",
    "SendMessageRequest",

    # User
    "CreateUserRequest",
    "UpdateUserRequest",
    "UserResponse",
]