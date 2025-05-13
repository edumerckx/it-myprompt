from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=func.gen_random_uuid(),
        init=False,
    )
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
    chats: Mapped[list['Chat']] = relationship(
        back_populates='user', init=False
    )


@table_registry.mapped_as_dataclass
class Chat:
    __tablename__ = 'chats'
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=func.gen_random_uuid(),
        init=False,
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    prompt: Mapped[str]
    response: Mapped[str]
    model: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    user: Mapped[User] = relationship(back_populates='chats', init=False)
