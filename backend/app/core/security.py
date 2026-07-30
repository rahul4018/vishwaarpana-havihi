from __future__ import annotations

import hashlib
import hmac

from pwdlib import PasswordHash

from app.core.config import settings

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """
    Hash a plain text password using Argon2.
    """
    return password_hash.hash(password)


def verify_password(
    password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a plain text password against its hash.
    """
    return password_hash.verify(
        password,
        hashed_password,
    )


def hash_refresh_token(token: str) -> str:
    """
    Hash a refresh token using HMAC-SHA256.

    The application's SECRET_KEY is used as the HMAC key so the
    original token is never stored in the database.
    """
    return hmac.new(
        settings.SECRET_KEY.encode("utf-8"),
        token.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def verify_refresh_token(
    token: str,
    stored_hash: str,
) -> bool:
    """
    Verify a refresh token against the stored hash.
    """
    computed_hash = hash_refresh_token(token)

    return hmac.compare_digest(
        computed_hash,
        stored_hash,
    )