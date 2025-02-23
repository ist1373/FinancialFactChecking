from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import List, Dict, Any, Optional

from typing import Optional
from pydantic import BaseModel, Field
from src.db.models import DocumentStatus

class InitDocument(BaseModel):
    document_content: str
    ground_truth: str

class DocumentUUID(BaseModel):
    uuid: str

class DocumentUpdate(BaseModel):
    """Schema for updating a document."""
    
    document_title: Optional[str] = Field(None, title="Document Title", description="Updated title of the document")
    document_summary: Optional[str] = Field(None, title="Document Summary", description="Updated summary of the document")
    document_content: Optional[str] = Field(None, title="Document Content", description="Updated document content")
    ground_truch_content: Optional[str] = Field(None, title="Ground Truth Content", description="Updated ground truth content")
    claims: Optional[list] = Field(None, title="Claims", description="Updated claims for the document")
    status: Optional[DocumentStatus] = Field(None, title="Document Status", description="Updated document status")

    class Config:
        orm_mode = True  # Enables compatibility with SQLAlchemy models

