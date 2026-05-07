from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Ship, User
from app.schemas import UserCreate, UserLogin, UserOut, TokenOut
from app.auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=TokenOut, status_code=201)
def register(data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=409, detail="Email already registered")
    if data.role.value == "crew" and data.ship_id is None:
        raise HTTPException(status_code=422, detail="Crew members must be assigned to a ship")
    if data.role.value == "admin" and data.ship_id is not None:
        raise HTTPException(status_code=422, detail="Administrators cannot be assigned to a ship")
    if data.ship_id is not None and db.query(Ship).filter(Ship.id == data.ship_id).first() is None:
        raise HTTPException(status_code=404, detail="Selected ship was not found")

    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        name=data.name,
        role=data.role,
        ship_id=data.ship_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(str(user.id), user.role.value)
    return TokenOut(access_token=token, user=UserOut.model_validate(user))


@router.post("/login", response_model=TokenOut)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(str(user.id), user.role.value)
    return TokenOut(access_token=token, user=UserOut.model_validate(user))


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return UserOut.model_validate(current_user)


@router.get("/users", response_model=List[UserOut])
def list_users(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    query = db.query(User)
    if current_user.role.value == "crew" and current_user.ship_id:
        query = query.filter(User.ship_id == current_user.ship_id)
    return query.all()
