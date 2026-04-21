from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token
from app.db import get_db
from app.models.schemas import UserCreate, UserResponse, Token

router = APIRouter(prefix="/auth", tags=["authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    from app.core.security import decode_access_token

    username = decode_access_token(token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return username


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    from supabase import create_client

    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Supabase not configured",
        )

    supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

    try:
        auth_response = supabase.auth.sign_up(
            {"email": user.email, "password": user.password}
        )
        if auth_response.user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Registration failed",
            )
        return UserResponse(
            id=auth_response.user.id,
            email=auth_response.user.email,
            full_name=user.full_name,
            created_at=auth_response.user.created_at,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    from supabase import create_client

    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Supabase not configured",
        )

    supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

    try:
        auth_response = supabase.auth.sign_in_with_password(
            {"email": form_data.username, "password": form_data.password}
        )
        if auth_response.user is None or auth_response.session is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(data={"sub": auth_response.user.id})
        return Token(access_token=access_token, token_type="bearer")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/me", response_model=UserResponse)
async def get_me(token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(token)
    return UserResponse(
        id=current_user,
        email="user@example.com",
        full_name="User",
        created_at="2024-01-01T00:00:00Z",
    )
