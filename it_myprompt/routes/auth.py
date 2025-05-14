from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession as AsyncSessionORM

from it_myprompt.database import get_session
from it_myprompt.models import User
from it_myprompt.schemas.auth import Token
from it_myprompt.security import create_token, get_user, verify

router = APIRouter(prefix='/auth', tags=['auth'])

AsyncSession = Annotated[AsyncSessionORM, Depends(get_session)]
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
CurrentUser = Annotated[User, Depends(get_user)]


@router.post('/token', response_model=Token, status_code=HTTPStatus.CREATED)
async def login_for_access_token(form_data: OAuth2Form, session: AsyncSession):
    user = await session.scalar(
        select(User).where(User.email == form_data.username)
    )

    bad_request = HTTPException(
        status_code=HTTPStatus.BAD_REQUEST, detail='Invalid credentials'
    )

    if not user:
        raise bad_request

    if not verify(form_data.password, user.password):
        raise bad_request

    access_token = create_token(data={'sub': user.email})
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post(
    '/refresh_token', response_model=Token, status_code=HTTPStatus.CREATED
)
def refresh_access_token(user: CurrentUser):
    access_token = create_token(data={'sub': user.email})
    return {'access_token': access_token, 'token_type': 'bearer'}
