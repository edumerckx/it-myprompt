from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session as SessionORM

from it_myprompt.database import get_session
from it_myprompt.models import User
from it_myprompt.schemas.user import UserResponse, UserSchema
from it_myprompt.security import get_hash, get_user

router = APIRouter(prefix='/users', tags=['users'])

Session = Annotated[SessionORM, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserResponse)
async def create_user(user: UserSchema, session: Session):
    new_user = User(
        name=user.name,
        email=user.email,
        password=get_hash(user.password),
    )

    try:
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Email already exists',
        )


@router.put('/me', status_code=HTTPStatus.OK, response_model=UserResponse)
async def update_user(
    user: UserSchema, session: Session, current_user: CurrentUser
):
    try:
        current_user.name = user.name
        current_user.email = user.email
        current_user.password = get_hash(user.password)

        await session.commit()
        await session.refresh(current_user)
        return current_user
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Email already exists',
        )
