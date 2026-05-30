"""Document model."""
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.database import Base


class Document(Base):
    """Document model for uploaded study materials."""

    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    file_type = Column(String(20), nullable=False)  # pdf, docx, pptx, txt
    file_size = Column(Integer, nullable=False)  # in bytes
    file_path = Column(String(500), nullable=False)
    subject = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    upload_date = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_processed = Column(Integer, default=0)  # 0: pending, 1: processing, 2: completed, 3: failed
    embedding_chunks = Column(Integer, default=0)  # number of text chunks with embeddings

    def __repr__(self):
        return f"<Document {self.title}>"
