from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.core.security import get_password_hash, create_access_token, verify_password
from src.db.models import User
from src.schemas.user import UserCreate
from datetime import timedelta
from src.core.config import settings
from fastapi.security import OAuth2PasswordRequestForm


def signup_logic(user: UserCreate, db: Session):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    hashed_password = get_password_hash(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    access_token = create_access_token(
        data={"sub": new_user.uuid},
        expires_delta=timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS),
    )
    return {"access_token": access_token, "token_type": "bearer"}


def signin_logic(form_data: OAuth2PasswordRequestForm, db: Session):
    """
    Handle user sign-in logic.

    Args:
        form_data: OAuth2PasswordRequestForm containing username (email) and password.
        db: SQLAlchemy database session.

    Returns:
        A dictionary with an access token and token type.

    Raises:
        HTTPException: If the email does not exist or the password is invalid.
    """
    # Query the database for the user
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Verify the provided password
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Generate a JWT token for the user
    access_token = create_access_token(
        data={"sub": user.uuid},  # Use the UUID as the subject (sub)
        expires_delta=timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS),
    )

    return {"access_token": access_token, "token_type": "bearer"}
