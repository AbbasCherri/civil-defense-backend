from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.core.security import create_access_token
from app.schemas import UserCreate, UserLogin, UserResponse, Token
from app.services import UserService
from app.models import UserRole

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user."""
    service = UserService(db)
    result = await service.register_user(user.name, user.email, user.password, user.role)
    
    if "error" in result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])
    
    return result


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """Login user and return JWT token. Accepts form data (username/password) for OAuth2 compatibility."""
    service = UserService(db)
    # Use username field as email (standard OAuth2 convention)
    user = await service.authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user["id"]), "email": user["email"], "role": user["role"]},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login/json", response_model=Token)
async def login_json(user_login: UserLogin, db: AsyncSession = Depends(get_db)):
    """Login user with JSON body (alternative to form data). Returns JWT token."""
    service = UserService(db)
    user = await service.authenticate_user(user_login.email, user_login.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user["id"]), "email": user["email"], "role": user["role"]},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/verify-token")
async def verify_token(current_user: dict = Depends(lambda token: token)):
    """Verify JWT token."""
    return {"valid": True, "user": current_user}


@router.get("/all_users", response_model=List[UserResponse])
async def read_all_users(db: AsyncSession = Depends(get_db)):
    """Read all users."""
    service = UserService(db)
    users = await service.get_all_users()
    return users 