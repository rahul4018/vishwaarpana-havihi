from pathlib import Path
from uuid import uuid4

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from app.core.dependencies.permissions import require_roles
from app.core.exceptions.http_exceptions import ResourceNotFoundError
from app.db.database import get_db
from app.db.models.user import User
from app.schemas import (
    CreateGalleryRequest,
    GalleryResponse,
    UpdateGalleryRequest,
)
from app.services import GalleryService


router = APIRouter(
    prefix="/gallery",
    tags=["Gallery"],
)


# Gallery image upload configuration
ALLOWED_IMAGE_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB

BASE_DIR = Path(__file__).resolve().parents[4]

GALLERY_UPLOAD_DIR = (
    BASE_DIR
    / "uploads"
    / "gallery"
)

GALLERY_UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


@router.get(
    "",
    response_model=list[GalleryResponse],
    summary="Get all gallery items",
)
def get_all_gallery_items(
    db: Session = Depends(get_db),
):
    """
    Get all gallery items.
    """

    service = GalleryService(db)

    return service.get_all()


@router.get(
    "/temple/{temple_id}",
    response_model=list[GalleryResponse],
    summary="Get gallery items by temple ID",
)
def get_gallery_by_temple(
    temple_id: str,
    db: Session = Depends(get_db),
):
    """
    Get gallery items associated with a temple.
    """

    service = GalleryService(db)

    try:
        return service.get_by_temple_id(
            temple_id
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/pooja/{pooja_id}",
    response_model=list[GalleryResponse],
    summary="Get gallery items by pooja ID",
)
def get_gallery_by_pooja(
    pooja_id: str,
    db: Session = Depends(get_db),
):
    """
    Get gallery items associated with a pooja.
    """

    service = GalleryService(db)

    try:
        return service.get_by_pooja_id(
            pooja_id
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
    summary="Upload gallery image",
)
async def upload_gallery_image(
    file: UploadFile = File(...),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
) -> dict[str, str]:
    """
    Upload a JPG, PNG, or WebP image for the gallery.

    Accessible only to ADMIN and SUPER_ADMIN.
    """

    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Only JPG, PNG, and WebP "
                "images are allowed."
            ),
        )

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded image is empty.",
        )

    if len(content) > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Image size must not exceed 5 MB.",
        )

    extension = ALLOWED_IMAGE_TYPES[
        file.content_type
    ]

    filename = (
        f"{uuid4()}{extension}"
    )

    file_path = (
        GALLERY_UPLOAD_DIR
        / filename
    )

    try:
        file_path.write_bytes(
            content
        )

    except OSError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save uploaded image.",
        ) from exc

    return {
        "filename": filename,
        "image_url": (
            f"/uploads/gallery/{filename}"
        ),
    }


@router.get(
    "/{gallery_id}",
    response_model=GalleryResponse,
    summary="Get gallery item by ID",
)
def get_gallery_item(
    gallery_id: str,
    db: Session = Depends(get_db),
):
    """
    Get a gallery item by ID.
    """

    service = GalleryService(db)

    try:
        return service.get_by_id(
            gallery_id
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.post(
    "",
    response_model=GalleryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create gallery item",
)
def create_gallery_item(
    request: CreateGalleryRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    """
    Create a new gallery item.

    Accessible only to ADMIN and SUPER_ADMIN.
    """

    service = GalleryService(db)

    try:
        return service.create(
            request
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.put(
    "/{gallery_id}",
    response_model=GalleryResponse,
    summary="Update gallery item",
)
def update_gallery_item(
    gallery_id: str,
    request: UpdateGalleryRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "SUPER_ADMIN"),
    ),
):
    """
    Update a gallery item.

    Accessible only to ADMIN and SUPER_ADMIN.
    """

    service = GalleryService(db)

    try:
        return service.update(
            gallery_id,
            request,
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{gallery_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete gallery item",
)
def delete_gallery_item(
    gallery_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("SUPER_ADMIN", "ADMIN"),
    ),
):
    """
    Delete a gallery item.

    Accessible only to SUPER_ADMIN.
    """

    service = GalleryService(db)

    try:
        service.delete(
            gallery_id
        )

    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc