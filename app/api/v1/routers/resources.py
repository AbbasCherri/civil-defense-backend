from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas import ResourceResponse, ResourceCreate, ResourceUpdate
from app.repositories import ResourceRepository
from app.models import UserRole, ResourceStatus, ResourceType
from datetime import datetime

router = APIRouter(prefix="/api/v1/resources", tags=["resources"])


@router.post("/", response_model=ResourceResponse)
async def create_resource(
    resource: ResourceCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new resource (Admin only)."""
    if current_user["role"] != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    repo = ResourceRepository(db)
    resource_obj = await repo.create(resource.name, resource.type, resource.status)
    await db.commit()
    
    return resource_obj


@router.get("/{resource_id}", response_model=ResourceResponse)
async def get_resource(
    resource_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get resource details."""
    repo = ResourceRepository(db)
    resource = await repo.get_by_id(resource_id)
    
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    
    return resource


@router.get("/", response_model=List[ResourceResponse])
async def list_resources(
    skip: int = 0,
    limit: int = 100,
    status_filter: str = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all resources with optional filters."""
    repo = ResourceRepository(db)
    
    if status_filter:
        try:
            status_enum = ResourceStatus(status_filter)
            resources = await repo.get_by_status(status_enum)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status")
    else:
        resources = await repo.get_all(skip, limit)
    
    return resources


@router.patch("/{resource_id}", response_model=ResourceResponse)
async def update_resource(
    resource_id: int,
    resource: ResourceUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update resource details (Admin only)."""
    if current_user["role"] != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    repo = ResourceRepository(db)
    update_data = resource.dict(exclude_unset=True)
    resource_obj = await repo.update(resource_id, **update_data)
    
    if not resource_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    
    await db.commit()
    return resource_obj


@router.patch("/{resource_id}/status")
async def update_resource_status(
    resource_id: int,
    status_update: dict,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update resource maintenance status."""
    if current_user["role"] not in [UserRole.ADMIN, UserRole.DISPATCHER]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    repo = ResourceRepository(db)
    new_status = ResourceStatus(status_update.get("status"))
    resource = await repo.update_status(resource_id, new_status)
    
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    
    await db.commit()
    return {"id": resource.id, "status": resource.status}


@router.patch("/{resource_id}/fuel")
async def update_fuel_usage(
    resource_id: int,
    fuel_data: dict,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update fuel usage for a vehicle."""
    repo = ResourceRepository(db)
    resource = await repo.get_by_id(resource_id)
    
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    
    current_fuel = resource.fuel_usage or 0
    resource = await repo.update(resource_id, fuel_usage=current_fuel + fuel_data.get("fuel_amount", 0))
    await db.commit()
    
    return {"id": resource.id, "fuel_usage": resource.fuel_usage}


@router.patch("/{resource_id}/inspect")
async def mark_inspection(
    resource_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Mark resource as inspected."""
    repo = ResourceRepository(db)
    resource = await repo.update(resource_id, last_inspection=datetime.utcnow())
    
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    
    await db.commit()
    return {"id": resource.id, "last_inspection": resource.last_inspection}


@router.get("/by-status/{status_value}", response_model=List[ResourceResponse])
async def get_resources_by_status(
    status_value: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get resources by status."""
    try:
        status_enum = ResourceStatus(status_value)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status")
    
    repo = ResourceRepository(db)
    resources = await repo.get_by_status(status_enum)
    return resources


@router.delete("/{resource_id}")
async def delete_resource(
    resource_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a resource (Admin only)."""
    if current_user["role"] != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    repo = ResourceRepository(db)
    result = await repo.delete(resource_id)
    
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    
    await db.commit()
    return {"message": "Resource deleted successfully"}
