from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_session, verify_token
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UserSchema, LoginSchema, UserAdmin
from http import HTTPStatus
from jose import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm


auth_router = APIRouter(prefix='/auth', tags=['auth'])


def create_token(user_id, token_duration=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    expiration_date = datetime.now(timezone.utc) + token_duration
    token_data = {
        "sub": str(user_id),
        "exp": expiration_date
    }
    encoded_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_token


def authenticate_user(email, password, session):
    user = session.query(User).filter(User.email == email).first()

    if not user:
        return False
    
    if not bcrypt_context.verify(password, user.password):
        return False
    
    return user


@auth_router.post('/create_admin')
async def create_admin(user_admin: UserAdmin, session=Depends(get_session)):

    existing_user = session.query(User).filter(User.email == user_admin.email).first()

    if existing_user:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="EMAIL_ALREADY_EXISTS"
        )

    hashed_password = bcrypt_context.hash(user_admin.password)

    new_admin = User(
        name=user_admin.name,
        email=user_admin.email,
        password=hashed_password,
        is_admin=True
    )

    session.add(new_admin)
    session.commit()

    return {
        "message": "ADMIN_CREATED"
    }


@auth_router.post('/create_account')
async def create_account(user: UserSchema, session=Depends(get_session)):

    existing_user = session.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="EMAIL_ALREADY_EXISTS"
        )

    hashed_password = bcrypt_context.hash(user.password)

    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
    )

    session.add(new_user)
    session.commit()

    return {
        "message": "USER_CREATED"
    }


@auth_router.post('/login')
async def login(login_data: LoginSchema, session=Depends(get_session)):

    user = authenticate_user(login_data.email, login_data.password, session)

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="INVALID_CREDENTIALS"
        )

    access_token = create_token(user.id)
    refresh_token = create_token(user.id, token_duration=timedelta(days=7))

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@auth_router.post('/login-form')
async def login_form(form_data: OAuth2PasswordRequestForm = Depends(), session=Depends(get_session)):

    user = authenticate_user(form_data.username, form_data.password, session)

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="INVALID_CREDENTIALS"
        )

    access_token = create_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@auth_router.get('/refresh')
async def use_refresh_token(user: User = Depends(verify_token)):

    access_token = create_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
