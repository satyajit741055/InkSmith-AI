from app.schemas import UserCreate, UserResponse,UserLogin,Token
from fastapi import APIRouter,status,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from typing import Annotated
from app.models import User
from fastapi import HTTPException
from app.services.auth_service  import current_user, hash_password, verify_password, create_access_token
from app.config import settings
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func,select


router = APIRouter()


@router.post(
    "/sign-up",
    response_model = UserResponse,
    status_code = status.HTTP_201_CREATED
    )
async def sign_up(user: UserCreate, db : Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(User).where(User.email == user.email)
    )
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    result = await db.execute(
        select(User).where(User.username == user.username)
    )
    existing_username = result.scalar_one_or_none()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create New USer 

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

    

@router.post(
    "/token",
    response_model = Token,
    status_code = status.HTTP_200_OK
    )
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(
        select(User).where(
            func.lower(User.email) == form_data.username.lower(),
        ),
    )
    user = result.scalars().first()

    # Verify user exists and password is correct
    # Don't reveal which one failed (security best practice)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token with user id as subject
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post(
    "/sign-in",
    response_model = Token,
    status_code = status.HTTP_200_OK
    )
async def sign_in(
    credentials: UserLogin,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(
        select(User).where(
            func.lower(User.email) == credentials.email.lower(),
        ),
    )
    user = result.scalars().first()

    # Verify user exists and password is correct
    # Don't reveal which one failed (security best practice)
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )



    # Create access token with user id as subject
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")
    

@router.get(
    "/me",
    response_model = UserResponse,
    status_code = status.HTTP_200_OK
    )
async def get_current_user(current_user:current_user):
    return current_user
    