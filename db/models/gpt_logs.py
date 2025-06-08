import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from openapi.db.base import Base


class GPTLog(Base):
    __tablename__ = "gpt_logs"

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
    word_id = Column(
        UUID(as_uuid=True),
        ForeignKey("words.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    token_usage = Column(Integer, nullable=False, default=0)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Взаємозв’язки
    user = relationship("User", back_populates="gpt_logs")
    word = relationship("Word", back_populates="gpt_logs")

    def __repr__(self):
        return (
            f"<GPTLog(id={self.id}, user_id={self.user_id}, word_id={self.word_id}, "
            f"token_usage={self.token_usage}, timestamp={self.timestamp})>"
        )
