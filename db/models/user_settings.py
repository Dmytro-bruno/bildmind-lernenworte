import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from openapi.db.base import Base


class UserSettings(Base):
    __tablename__ = "user_settings"

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
        unique=True,
        nullable=False,
    )
    interface_language = Column(String(10), nullable=False, default="en")  # мова інтерфейсу
    native_language = Column(String(10), nullable=False, default="uk")  # мова, яку знає користувач
    target_language = Column(String(10), nullable=False, default="de")  # мова, яку він вивчає
    notifications_enabled = Column(Boolean, default=True)
    dark_mode = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="settings")

    __table_args__ = (UniqueConstraint("user_id", name="uq_user_settings_user_id"),)

    def __repr__(self):
        return (
            f"<UserSettings(id={self.id}, user_id={self.user_id}, "
            f"interface={self.interface_language}, native={self.native_language},"
            f" target={self.target_language})>"
        )
