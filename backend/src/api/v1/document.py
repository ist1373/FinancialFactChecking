from fastapi import APIRouter, Depends, HTTPException
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, File, UploadFile
from src.db.models import User
from sqlalchemy.orm import Session
from src.schemas.document import InitDocument, DocumentUUID
from src.core.security import get_current_user
from src.llm.charli_llm_client import CharliLLMClient,get_llm_client
from src.services.document import create_document,generate_document_title,document_claim_extraction,document_claim_evaluation,get_document_by_uuid
from src.db.session import get_db
import asyncio
import json

router = APIRouter()


@router.post("/document/create")
async def init_document(document: InitDocument,current_user: User = Depends(get_current_user), 
                    db: Session = Depends(get_db)):

    # document_title = generate_document_title(document_content=document.document_content,llm_client=llm_client)
    document = create_document(
                             document_content=document.document_content,
                             ground_truth=document.ground_truth,
                             current_user=current_user,db=db)
    return document

@router.post("/document/extract-claims")
async def extract_claims(doc: DocumentUUID,current_user: User = Depends(get_current_user), 
                    db: Session = Depends(get_db)):

    # document_title = generate_document_title(document_content=document.document_content,llm_client=llm_client)
    claims = await document_claim_extraction(db,doc.uuid)
    return claims

@router.post("/document/verify-claims")
async def verify_claims(doc: DocumentUUID,current_user: User = Depends(get_current_user), 
                    db: Session = Depends(get_db)):

    # document_title = generate_document_title(document_content=document.document_content,llm_client=llm_client)
    claims = await document_claim_evaluation(db,doc.uuid)
    return claims


active_connections = {}

@router.websocket("/ws/{document_uuid}")
async def websocket_connection(websocket: WebSocket, document_uuid: str, 
                               db: Session = Depends(get_db), 
                               llm_client: CharliLLMClient = Depends(get_llm_client)):
    """Handles WebSocket connections for document processing updates."""
    await websocket.accept()
    active_connections[document_uuid] = websocket

    try:
        await process_document(websocket, document_uuid, db, llm_client)
    finally:
        # Clean up connection after processing completes
        await websocket.close()
        del active_connections[document_uuid]



async def process_document(websocket: WebSocket, document_uuid: str, db: Session, llm_client: CharliLLMClient):
    try:
        await websocket.send_text(json.dumps({"status": "Processing started..."}))
        await asyncio.sleep(0.1)
        
        await websocket.send_text(json.dumps({"status": "Generating title..."}))
        await asyncio.sleep(0.1)

        document = await generate_document_title(db, document_uuid=document_uuid, llm_client=llm_client)
        await websocket.send_text(json.dumps({"status": "Title is generated!","data":document.document_title}))
        await asyncio.sleep(0.1)
        
        # Step 1: Extract Claims
        await websocket.send_text(json.dumps({"status": "Extracting Claims..."}))
        await asyncio.sleep(0.1)

        document = await document_claim_extraction(db, document_uuid=document_uuid)
        await websocket.send_text(json.dumps({"status": "Claim Extraction Complete!", "data": document.claims}))
        await asyncio.sleep(0.1)
        
        # Step 2: Evaluate Claims
        await websocket.send_text(json.dumps({"status": "Evaluating Claims..."}))
        await asyncio.sleep(0.1)

        document = await document_claim_evaluation(db, document_uuid=document_uuid)
        await websocket.send_text(json.dumps({"status": "Claim Evaluation Complete!", "data": document.claims}))
        await asyncio.sleep(0.1)
        
        await websocket.send_text(json.dumps({"status": "Processing Complete"}))
        
    except WebSocketDisconnect:
        print(f"Client for document {document_uuid} disconnected early.")

