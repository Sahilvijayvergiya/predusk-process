from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List
import os
import uuid
import aiofiles
from datetime import datetime

from app.core.database import get_db
from app.models.document import Document, ProcessingJob
from app.schemas.document import DocumentResponse, ProcessingJobResponse
from app.core.config import settings
from app.services.document_service import DocumentService
from app.workers.document_processor import process_document

router = APIRouter()


@router.post("/upload", response_model=ProcessingJobResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload a document and create a processing job"""
    
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
    
    # Save file
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    # Create document record
    document = Document(
        filename=unique_filename,
        original_filename=file.filename,
        file_path=file_path,
        file_type=file.content_type or "unknown",
        file_size=len(content)
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    # Create processing job
    processing_job = ProcessingJob(
        document_id=document.id,
        status="queued"
    )
    
    db.add(processing_job)
    db.commit()
    db.refresh(processing_job)
    
    # Queue the processing task
    task = process_document.delay(processing_job.id)
    
    # Update job with task ID
    processing_job.celery_task_id = task.id
    db.commit()
    db.refresh(processing_job)
    
    return processing_job


@router.get("/", response_model=List[DocumentResponse])
async def list_documents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all documents"""
    documents = db.query(Document).offset(skip).limit(limit).all()
    return documents


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific document"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """Delete a document and its processing jobs"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Delete file from filesystem
    if os.path.exists(document.file_path):
        os.remove(document.file_path)
    
    # Delete database records (cascade will handle processing jobs)
    db.delete(document)
    db.commit()
    
    return {"message": "Document deleted successfully"}
