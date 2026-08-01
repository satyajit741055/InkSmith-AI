from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

import db.models as models
from db.database import get_db
from db.schemas import UserCreate
from auth import (
    create_access_token,
    hash_password,
    oauth2_scheme,
    verify_access_token,
    verify_password,
)

router = APIRouter()


@router.post("/register",status_code=status.HTTP_201_CREATED)
async def register(user:UserCreate,db:Annotated[AsyncSession,Depends(get_db)]):
    result = await db.execute(
        select(models.User).where(
            func.lower(models.User.username) == func.lower(user.username)
        )
    )
    
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    result = await db.execute(
        select(models.User).where(func.lower(models.User.email) == user.email.lower()),
    )
    existing_email = result.scalars().first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    hashed_password = hash_password(user.password)
    
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user

@router.post("/login")
async def login(user:UserCreate,db:Annotated[AsyncSession,Depends(get_db)]):
    result = await db.execute(
        select(models.User).where(
            func.lower(models.User.username) == func.lower(user.username)
        )
    )
    
    existing_user = result.scalar_one_or_none()
    
    if not existing_user or not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": existing_user.username},expires_delta=timedelta(minutes=30))
    
    return {"access_token": access_token, "token_type": "bearer"}


