from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
import os
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user
from app.core.config import settings
from app.schemas import MediaResponse
from app.repositories import MediaRepository
from app.models import MediaType

router = APIRouter(prefix="/api/v1/media", tags=["media"])


@router.post("/upload")
async def upload_media(
    incident_id: int = Form(...),
    file_type: str = Form(...),
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Upload media file for an incident."""
    
    # Validate file type
    valid_types = ["image", "video", "voice", "document"]
    if file_type not in valid_types:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type")
    
    # Validate file size
    file_content = await file.read()
    if len(file_content) > settings.MAX_FILE_SIZE:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File too large")
    
    # Create uploads directory if it doesn't exist
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # Generate unique filename
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"{incident_id}_{timestamp}_{file.filename}"
    file_path = os.path.join(settings.UPLOAD_DIR, filename)
    
    # Save file
    with open(file_path, "wb") as f:
        f.write(file_content)
    
    # Store in database
    media_repo = MediaRepository(db)
    media_type_enum = MediaType(file_type)
    media = await media_repo.create(incident_id, file_path, media_type_enum)
    await db.commit()
    
    return {
        "id": media.id,
        "incident_id": media.incident_id,
        "file_path": file_path,
        "file_type": file_type,
        "created_at": media.created_at
    }


@router.get("/incident/{incident_id}", response_model=list[MediaResponse])
async def get_incident_media(
    incident_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all media files for an incident."""
    media_repo = MediaRepository(db)
    media_files = await media_repo.get_by_incident(incident_id)
    
    return media_files


@router.delete("/{media_id}")
async def delete_media(
    media_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a media file."""
    media_repo = MediaRepository(db)
    media = await media_repo.get_by_id(media_id)
    
    if not media:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media not found")
    
    # Delete file from filesystem
    if os.path.exists(media.file_path):
        os.remove(media.file_path)
    
    # Delete from database
    await media_repo.delete(media_id)
    await db.commit()
    
    return {"message": "Media deleted successfully"}
