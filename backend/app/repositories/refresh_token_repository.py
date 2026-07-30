from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.refresh_token import RefreshToken


class RefreshTokenRepository:
    """
    Repository for refresh token database operations.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        refresh_token: RefreshToken,
    ) -> RefreshToken:
        self.db.add(refresh_token)
        self.db.commit()
        self.db.refresh(refresh_token)
        return refresh_token

    def get_by_jti(
        self,
        jti: str,
    ) -> RefreshToken | None:
        statement = select(RefreshToken).where(
            RefreshToken.jti == jti
        )
        return self.db.scalar(statement)

    def revoke(
        self,
        refresh_token: RefreshToken,
    ) -> RefreshToken:
        refresh_token.revoked_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(refresh_token)
        return refresh_token

    def delete_expired(
        self,
        now: datetime,
    ) -> int:
        expired_tokens = (
            self.db.query(RefreshToken)
            .filter(RefreshToken.expires_at < now)
            .all()
        )

        count = len(expired_tokens)

        for token in expired_tokens:
            self.db.delete(token)

        self.db.commit()

        return count