from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.user import User

from app.schemas.user import UserRegister
from app.schemas.user import UserLogin

from app.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register")
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):

    existing_user = (
        db.query(User)
        .filter(
            User.username == user.username
        )
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Usuario ya existe"
        )

    new_user = User(
    username=user.username,
    email=user.email,
    password=hash_password(
        user.password
    )
)

    db.add(new_user)
    db.commit()

    return {
        "message": "Usuario registrado"
    }


@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = (
        db.query(User)
        .filter(
            User.username == user.username
        )
        .first()
    )

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Credenciales inválidas"
        )

    if not verify_password(
        user.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Credenciales inválidas"
        )

    token = create_access_token(
        {
            "sub": str(
                db_user.id
            )
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }