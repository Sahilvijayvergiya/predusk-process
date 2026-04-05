from sqlalchemy.orm import Session
from app.models.document import Document, ProcessingJob
from app.schemas.document import DocumentCreate, ProcessingJobCreate
from typing import List, Optional
import os


class DocumentService:
    def __init__(self, db: Session):
        self.db = db

    async def create_document(self, document_data: DocumentCreate) -> Document:
        """Create a new document record"""
        document = Document(**document_data.dict())
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document

    async def get_document_by_id(self, document_id: int) -> Optional[Document]:
        """Get document by ID"""
        return self.db.query(Document).filter(Document.id == document_id).first()

    async def list_documents(self, skip: int = 0, limit: int = 100) -> List[Document]:
        """List all documents"""
        return self.db.query(Document).offset(skip).limit(limit).all()

    async def delete_document(self, document_id: int) -> bool:
        """Delete a document and its file"""
        document = await self.get_document_by_id(document_id)
        if not document:
            return False
        
        # Delete file from filesystem
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
        
        # Delete from database (cascade will handle processing jobs)
        self.db.delete(document)
        self.db.commit()
        return True
