from celery import Task
from app.workers.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.document import ProcessingJob, JobStatus
from datetime import datetime
import os
import mimetypes
import json
import random
from typing import Dict, Any


class DatabaseTask(Task):
    """Base task that handles database sessions"""
    def __call__(self, *args, **kwargs):
        with SessionLocal() as db:
            self.db = db
            try:
                return super().__call__(*args, **kwargs)
            finally:
                self.db.close()


@celery_app.task(bind=True, base=DatabaseTask)
def process_document(self, job_id: int):
    """Process a document asynchronously with progress tracking"""
    from app.services.job_service import JobService
    job_service = JobService(self.db)
    
    try:
        # Get the job
        job = self.db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()
        if not job:
            raise Exception(f"Job {job_id} not found")
        
        # Update job status to processing
        job.status = JobStatus.PROCESSING
        job.started_at = datetime.utcnow()
        job.current_stage = "document_received"
        job.progress_percentage = 10.0
        self.db.commit()
        
        # Publish progress event
        import asyncio
        asyncio.run(job_service.publish_progress_event(
            job_id, JobStatus.PROCESSING, 10.0, "document_received", "Document received for processing"
        ))
        
        # Simulate document parsing (20% progress)
        _simulate_processing_step(job, job_service, "parsing_started", "Parsing document content", 20.0)
        parsed_content = _parse_document(job.document.file_path)
        _simulate_processing_step(job, job_service, "parsing_completed", "Document parsing completed", 40.0)
        
        # Simulate field extraction (60% progress)
        _simulate_processing_step(job, job_service, "extraction_started", "Extracting structured fields", 50.0)
        extracted_data = _extract_fields(parsed_content, job.document.original_filename)
        _simulate_processing_step(job, job_service, "extraction_completed", "Field extraction completed", 70.0)
        
        # Store results (80% progress)
        _simulate_processing_step(job, job_service, "storing_results", "Storing processed results", 80.0)
        
        job.extracted_title = extracted_data.get("title")
        job.extracted_category = extracted_data.get("category")
        job.extracted_summary = extracted_data.get("summary")
        job.extracted_keywords = extracted_data.get("keywords", [])
        job.processed_content = parsed_content[:1000] + "..." if len(parsed_content) > 1000 else parsed_content
        job.final_result = extracted_data
        job.progress_percentage = 90.0
        
        self.db.commit()
        
        # Complete job (100% progress)
        _simulate_processing_step(job, job_service, "job_completed", "Processing completed successfully", 100.0)
        
        job.status = JobStatus.COMPLETED
        job.completed_at = datetime.utcnow()
        job.current_stage = "completed"
        job.progress_percentage = 100.0
        
        self.db.commit()
        
        return {
            "status": "completed",
            "job_id": job_id,
            "extracted_data": extracted_data
        }
        
    except Exception as e:
        # Handle job failure
        job = self.db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()
        if job:
            job.status = JobStatus.FAILED
            job.error_message = str(e)
            job.completed_at = datetime.utcnow()
            job.current_stage = "failed"
            self.db.commit()
            
            # Publish failure event
            import asyncio
            asyncio.run(job_service.publish_progress_event(
                job_id, JobStatus.FAILED, job.progress_percentage, "job_failed", f"Processing failed: {str(e)}"
            ))
        
        raise


def _simulate_processing_step(job, job_service, stage_name: str, message: str, progress: float):
    """Simulate a processing step with delay and progress update"""
    import time
    import asyncio
    
    # Simulate processing time
    time.sleep(random.uniform(0.5, 2.0))
    
    # Update job
    job.current_stage = stage_name
    job.progress_percentage = progress
    
    # Publish progress event
    asyncio.run(job_service.publish_progress_event(
        job.id, JobStatus.PROCESSING, progress, stage_name, message
    ))


def _parse_document(file_path: str) -> str:
    """Parse document content (simulated)"""
    # In a real implementation, this would use appropriate parsers
    # For PDF: PyPDF2, pdfplumber
    # For DOCX: python-docx
    # For TXT: simple file read
    
    try:
        file_type = mimetypes.guess_type(file_path)[0]
        
        if file_type and file_type.startswith('text/'):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            # For binary files, simulate content extraction
            return f"Simulated extracted content from {os.path.basename(file_path)}. " * 50
            
    except Exception as e:
        return f"Error parsing document: {str(e)}"


def _extract_fields(content: str, filename: str) -> Dict[str, Any]:
    """Extract structured fields from document content (simulated)"""
    # In a real implementation, this would use NLP/AI techniques
    # For now, simulate extraction based on content and filename
    
    words = content.split() if content else []
    word_count = len(words)
    
    # Simulate title extraction
    title = os.path.splitext(filename)[0].replace('_', ' ').replace('-', ' ').title()
    
    # Simulate category extraction
    categories = ["Business", "Technical", "Legal", "Financial", "Marketing", "Research"]
    category = random.choice(categories)
    
    # Simulate summary
    summary = f"This document contains approximately {word_count} words and appears to be related to {category.lower()} topics."
    
    # Simulate keyword extraction
    common_words = ["analysis", "report", "data", "system", "process", "management", "development", "research"]
    keywords = random.sample(common_words, min(5, len(common_words)))
    
    return {
        "title": title,
        "category": category,
        "summary": summary,
        "keywords": keywords,
        "word_count": word_count,
        "processing_metadata": {
            "extraction_method": "simulated",
            "confidence_score": random.uniform(0.7, 0.95)
        }
    }
