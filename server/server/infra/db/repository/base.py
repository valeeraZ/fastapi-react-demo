from typing import Any, Generic, Sequence, Type, TypeVar

from server.infra.db.model.base import Base
from sqlalchemy import Row, RowMapping
from sqlalchemy.engine.result import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

T = TypeVar("T", bound=Base)
TEntity = TypeVar("TEntity", bound=Base)


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: AsyncSession):
        self.model = model
        self.session = session

    async def _query(self, *args: Any, **kwargs: Any) -> Result[tuple[Any]]:
        filters = [getattr(self.model, k) == v for k, v in kwargs.items()]
        filters.extend(iter(args))
        stmt = select(self.model).filter(*filters)
        return await self.session.execute(stmt)

    async def get(self, *args: Any, **kwargs: Any) -> T | None:
        result = await self._query(*args, **kwargs)
        return result.scalars().one_or_none()

    async def get_many(
        self, *args: Any, **kwargs: Any
    ) -> Sequence[Row[tuple[Any]] | RowMapping | Any]:
        result = await self._query(*args, **kwargs)
        return result.scalars().all()

    async def create(self, obj_in: dict[str, Any] | T) -> T:
        if isinstance(obj_in, dict):
            return await self._create_from_dict(obj_in)
        if isinstance(obj_in, self.model):
            return await self._create_from_model(obj_in)
        raise TypeError(
            f"obj_in must be of type {self.model} or dict, not {type(obj_in)}",
        )

    async def _create_from_model(self, obj_in: T) -> T:
        return await add_and_commit(self.session, obj_in)

    async def _create_from_dict(self, obj_in: dict[str, Any]) -> T:
        return await add_and_commit(self.session, self.model(**obj_in))

    async def get_by_id(self, id: int) -> T | None:
        return await self.get(id=id)

    async def update(self, obj_in: T) -> T:
        await self.session.commit()
        return obj_in

    async def update_with_dict(self, obj_in: T, updated_data: dict[str, Any]) -> T:
        for attr, value in updated_data.items():
            if obj_in.__table__.columns.keys().__contains__(attr):
                setattr(obj_in, attr, value)
        await self.session.commit()
        return obj_in

    async def delete(self, obj_in: T) -> None:
        await self.session.delete(obj_in)  # type: ignore
        await self.session.commit()

    async def delete_many(self, objs_in: list[T]) -> None:
        for obj in objs_in:
            await self.session.delete(obj)  # type: ignore
        await self.session.commit()


class RepositoryError(Exception):
    pass


async def add_and_commit(session: AsyncSession, obj: T) -> T:
    try:
        session.add(obj)  # type: ignore
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise RepositoryError(
            f"Error while adding {obj} to session: {str(e)}",
        ) from e
    return obj
