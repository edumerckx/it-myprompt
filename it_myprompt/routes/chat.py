from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from sqlalchemy.ext.asyncio import AsyncSession as AsyncSessionORM

from it_myprompt.database import get_session
from it_myprompt.models import Chat, User
from it_myprompt.schemas.chat import ChatResponse, ChatSchema
from it_myprompt.security import get_user
from it_myprompt.services.openrouter import get_llm

router = APIRouter(prefix='/chat', tags=['chat'])
AsyncSession = Annotated[AsyncSessionORM, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_user)]
LLM = Annotated[ChatOpenAI, Depends(get_llm)]


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=ChatResponse,
)
async def create_chat(
    chat: ChatSchema,
    session: AsyncSession,
    current_user: CurrentUser,
    llm: LLM,
):
    template = PromptTemplate.from_template(
        '{prompt}. Responda de forma direta'
    )
    chain = template | llm | StrOutputParser()

    try:
        response = await chain.ainvoke({'prompt': chat.prompt})
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
            detail=str(e),
        )

    new_chat = Chat(
        user_id=current_user.id,
        prompt=chat.prompt,
        response=response,
        model=llm.model_name,
    )

    session.add(new_chat)
    await session.commit()
    await session.refresh(new_chat)

    return new_chat
