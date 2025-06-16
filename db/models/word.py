import uuid

from sqlalchemy import Column, DateTime, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from openapi.db.base import Base


class Word(Base):
    __tablename__ = "words"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True,
    )
    base_form = Column(String(255), nullable=False)
    article = Column(String(10), nullable=True)
    base_and_article = Column(String(255), nullable=False)
    translation = Column(String(255), nullable=False)
    lang_from = Column(String(10), nullable=False)
    lang_to = Column(String(10), nullable=False)
    example = Column(String(512), nullable=True)
    level = Column(String(8), nullable=True, comment="CEFR рівень слова: A1, A2, B1...")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Взаємозв'язок з UserWord
    user_words = relationship("UserWord", back_populates="word", cascade="all, delete-orphan")
    gpt_logs = relationship("GPTLog", back_populates="word", cascade="all, delete-orphan")
    __table_args__ = (
        UniqueConstraint(
            "base_form",
            "translation",
            "lang_from",
            "lang_to",
            name="uq_word_baseform_translation_langs",
        ),
    )

    def __repr__(self):
        return (
            f"<Word(id={self.id}, base_form={self.base_form}, "
            f"translation={self.translation}, lang_from={self.lang_from}, "
            f"lang_to={self.lang_to})>"
        )
