import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.base import Base


class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    jti = Column(
        String(128), unique=True, nullable=False, index=True
    )  # JWT ID (зазвичай це унікальний str)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expired_at = Column(
        DateTime(timezone=True), nullable=False
    )  # до якого моменту не можна приймати цей токен
    reason = Column(String(100), nullable=True)

    user = relationship("User", back_populates="token_blacklist")

    def __repr__(self):
        return (
            f"<TokenBlacklist(id={self.id}, "
            f"user_id={self.user_id}, jti={self.jti}, "
            f"reason={self.reason})>"
        )
