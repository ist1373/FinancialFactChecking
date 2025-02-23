"""
Auth API
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from src.db.session import get_db
from src.schemas.user import UserCreate, Token
from src.services.auth import signup_logic,signin_logic

router = APIRouter()

@router.post("/signup/", response_model=Token, status_code=201)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    return signup_logic(user, db)


@router.post("/signin/", response_model=Token)
def signin(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return signin_logic(form_data, db)

