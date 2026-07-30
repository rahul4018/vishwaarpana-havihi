from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions.http_exceptions import (
    BadRequestError,
    DuplicateCategoryNameError,
    DuplicateCategorySlugError,
    DuplicateEmailError,
    DuplicateTempleNameError,
    DuplicateTempleSlugError,
    InvalidCredentialsError,
    InvalidTokenError,
    ResourceNotFoundError,
    RoleNotFoundError,
)


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(ResourceNotFoundError)
    async def resource_not_found_handler(
        request: Request,
        exc: ResourceNotFoundError,
    ):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )

    @app.exception_handler(BadRequestError)
    async def bad_request_handler(
        request: Request,
        exc: BadRequestError,
    ):
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)},
        )

    @app.exception_handler(DuplicateEmailError)
    async def duplicate_email_handler(
        request: Request,
        exc: DuplicateEmailError,
    ):
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc)},
        )

    @app.exception_handler(DuplicateTempleNameError)
    async def duplicate_temple_name_handler(
        request: Request,
        exc: DuplicateTempleNameError,
    ):
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc)},
        )

    @app.exception_handler(DuplicateTempleSlugError)
    async def duplicate_temple_slug_handler(
        request: Request,
        exc: DuplicateTempleSlugError,
    ):
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc)},
        )

    @app.exception_handler(DuplicateCategoryNameError)
    async def duplicate_category_name_handler(
        request: Request,
        exc: DuplicateCategoryNameError,
    ):
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc)},
        )

    @app.exception_handler(DuplicateCategorySlugError)
    async def duplicate_category_slug_handler(
        request: Request,
        exc: DuplicateCategorySlugError,
    ):
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc)},
        )

    @app.exception_handler(InvalidCredentialsError)
    async def invalid_credentials_handler(
        request: Request,
        exc: InvalidCredentialsError,
    ):
        return JSONResponse(
            status_code=401,
            content={"detail": str(exc)},
        )

    @app.exception_handler(InvalidTokenError)
    async def invalid_token_handler(
        request: Request,
        exc: InvalidTokenError,
    ):
        return JSONResponse(
            status_code=401,
            content={"detail": str(exc)},
        )

    @app.exception_handler(RoleNotFoundError)
    async def role_not_found_handler(
        request: Request,
        exc: RoleNotFoundError,
    ):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )