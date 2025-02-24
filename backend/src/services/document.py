from sqlalchemy.orm import Session
from src.db.models import Document
from src.llm.charli_llm_client import CharliLLMClient
from src.db.models import User
from src.schemas.document import DocumentUpdate
from typing import Optional
from sqlalchemy.exc import NoResultFound
import requests
import urllib
from src.core.config import settings
from src.db.models import DocumentStatus

async def generate_document_title(db: Session, document_uuid: str,llm_client:CharliLLMClient)->Optional[Document]:
    system_prompt ="""
    Role: Financial Document Analyst

    Task:
    Generate a concise and relevant title for the given DOCUMENT based on its content.

    Instructions:
    Return only the short title.
    Do not include explanations, comments, or extra text.
    Do not introduce the title with phrases like "Here is the short title"—provide only the title itself.
    """
    document = db.query(Document).filter(Document.uuid == document_uuid).first()
    
    if not document:
        return None  # Document not found
    content = document.document_content
    if len(document.document_content) > 100:
        content = document.document_content[:100]
    user_prompt = f"DOCUMENT:\n{content}"
    payload = llm_client.format_input(system_prompt=system_prompt,user_prompt=user_prompt)
    generated_title = llm_client.call(payload)
    document.document_title = generated_title
    db.commit()
    db.refresh(document)
    return document


async def document_claim_extraction(db: Session, document_uuid: str)->Optional[Document]:
    """Trigger claim extraction for a document via external service."""
    document = db.query(Document).filter(Document.uuid == document_uuid).first()
    
    if not document:
        return None  # Document not found
    
    payload = {"answer": document.document_content}
    
    endpoint = urllib.parse.urljoin(settings.LLM_FACT_CHECKER_URL, settings.LLM_CLAIM_EXTRACTION_ENDPOINT)

    response = requests.post(endpoint, json=payload)
    
    if response.status_code == 200:
        extracted_claims = response.json()["results"]
        
        document.claims = extracted_claims
        document.status = DocumentStatus.CLAIM_VERIFICATION  
        db.commit()
        db.refresh(document)
    return document

async def document_claim_evaluation(db: Session, document_uuid: str)->Optional[Document]:
    """Trigger claim verification for a document via external service."""
    document = db.query(Document).filter(Document.uuid == document_uuid).first()
    
    if not document:
        return None  # Document not found
    
    payload = {"claims": document.claims,"truth_document":document.ground_truch}
    
    endpoint = urllib.parse.urljoin(settings.LLM_FACT_CHECKER_URL, settings.LLM_CLAIM_VERIFICATION_ENDPOINT)

    response = requests.post(endpoint, json=payload)
    
    if response.status_code == 200:
        extracted_claim_scores = response.json()["results"]
        
        document.claims = extracted_claim_scores
        document.status = DocumentStatus.DONE  
        db.commit()
        db.refresh(document)
    return document


def create_document(document_content:str, ground_truth:str ,current_user:User, db: Session) ->Optional[Document]:
    """Create a document and trigger claim extraction."""
    document = Document(
        document_title="",
        document_content=document_content,
        ground_truch=ground_truth,
        claims=[],  # Initially empty
        user_uuid=current_user.uuid,
        status="CLAIM_EXTRACTION"
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


def update_document(db: Session, document_id: str, update_data: DocumentUpdate) -> Optional[Document]:
    """Update a document's fields such as summary, status, etc."""
    document = db.query(Document).filter(Document.uuid == document_id).first()
    
    if not document:
        return None  # Document not found
    
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(document, key, value)  # Update only provided fields
    
    db.commit()
    db.refresh(document)
    return document


def get_document_by_uuid(db: Session, document_uuid: str) -> Optional[Document]:
    """Retrieve a document by its UUID."""
    try:
        
        document = db.query(Document).filter(Document.uuid == document_uuid).one()
        return document
    except NoResultFound:
        return None

async def get_document_list(db: Session, user: User):
    """Retrieve all documents uploaded by a specific user."""

    documents = db.query(Document.uuid, Document.document_title).filter(Document.user_uuid == user.uuid).all()
    return [{"document_id": str(doc.uuid), "title": doc.document_title} for doc in documents]
