
from datetime import datetime, timezone
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, JSON, CHAR, Enum
from src.db.base import Base
from sqlalchemy.orm import relationship
import uuid
import enum

class DocumentStatus(enum.Enum):
    CLAIM_EXTRACTION = "claim_extraction"
    CLAIM_VERIFICATION = "claim_verification"
    DONE = "done"

class User(Base):
    __tablename__ = "User"

    uuid = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(128), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    creation_date = Column(DateTime, default=datetime.now(timezone.utc))

    # Relationship to Document
    documents = relationship("Document", back_populates="user", cascade="all, delete-orphan")


class Document(Base):
    __tablename__ = "Document"

    uuid = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_title = Column(Text, nullable=False)
    document_content = Column(Text, nullable=False)
    ground_truch = Column(Text, nullable=False)
    claims = Column(JSON, nullable=False)  # Storing claims as JSON
    creation_date = Column(DateTime, default=datetime.now(timezone.utc))
    user_uuid = Column(CHAR(36), ForeignKey("User.uuid", ondelete="CASCADE"), nullable=True)
    status = Column(Enum(DocumentStatus), default=DocumentStatus.CLAIM_EXTRACTION, nullable=False)
    # Relationship to User
    user = relationship("User", back_populates="documents")
