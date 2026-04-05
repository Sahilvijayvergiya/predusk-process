from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from app.models.document import ProcessingJob, JobStatus, Document
from app.schemas.document import ProcessingJobUpdate
from typing import List, Optional
from datetime import datetime
from app.workers.document_processor import process_document
from app.core.redis_client import redis_client
import json


class JobService:
    def __init__(self, db: Session):
        self.db = db

    async def list_jobs(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        search: Optional[str] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> List[ProcessingJob]:
        """List processing jobs with filtering and sorting"""
        query = self.db.query(ProcessingJob).join(Document)
        
        # Filter by status
        if status:
            try:
                status_enum = JobStatus(status)
                query = query.filter(ProcessingJob.status == status_enum)
            except ValueError:
                pass  # Invalid status, ignore filter
        
        # Search by filename
        if search:
            query = query.filter(Document.original_filename.ilike(f"%{search}%"))
        
        # Sorting
        sort_column = getattr(ProcessingJob, sort_by, ProcessingJob.created_at)
        if sort_order.lower() == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))
        
        return query.offset(skip).limit(limit).all()

    async def get_job_by_id(self, job_id: int) -> Optional[ProcessingJob]:
        """Get job by ID"""
        return self.db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()

    async def update_job(self, job_id: int, job_update: ProcessingJobUpdate) -> Optional[ProcessingJob]:
        """Update a processing job"""
        job = await self.get_job_by_id(job_id)
        if not job:
            return None
        
        # Update fields
        update_data = job_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(job, field, value)
        
        self.db.commit()
        self.db.refresh(job)
        return job

    async def retry_job(self, job: ProcessingJob) -> ProcessingJob:
        """Retry a failed processing job"""
        # Reset job status
        job.status = JobStatus.QUEUED
        job.progress_percentage = 0.0
        job.current_stage = "queued"
        job.error_message = None
        job.started_at = None
        job.completed_at = None
        
        self.db.commit()
        
        # Queue new processing task
        task = process_document.delay(job.id)
        job.celery_task_id = task.id
        
        self.db.commit()
        self.db.refresh(job)
        
        # Publish retry event
        await self.publish_progress_event(
            job.id,
            JobStatus.QUEUED,
            0.0,
            "job_retried",
            "Job has been queued for retry"
        )
        
        return job

    async def publish_progress_event(
        self,
        job_id: int,
        status: JobStatus,
        progress_percentage: float,
        current_stage: str,
        message: Optional[str] = None
    ):
        """Publish progress event to Redis Pub/Sub"""
        event = {
            "job_id": job_id,
            "status": status.value,
            "progress_percentage": progress_percentage,
            "current_stage": current_stage,
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Publish to Redis
        redis_client.publish("job_progress", json.dumps(event))
        
        # Also store in Redis for current state retrieval
        redis_client.set(f"job_progress:{job_id}", json.dumps(event), ex=3600)  # 1 hour expiry
