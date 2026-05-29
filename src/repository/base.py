from typing import Type, Optional, Any, List, TypeVar
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")

class BaseRepo:
    def __init__(self, model: Type[ModelType], session: Session):
        self.model = model
        self.session = session

    def create(self, **kwargs) -> ModelType:
        """Создать новую запись"""
        instance = self.model(**kwargs)
        self.session.add(instance)
        self.session.commit()
        return instance


    def get(self, id: Any) -> Optional[ModelType]:
        """Получить по ID"""
        return self.session.get(self.model, id)


    def get_one(self, **filters) -> Optional[ModelType]:
        """Получить одну запись по фильтрам"""
        query = select(self.model).filter_by(**filters)
        result = self.session.execute(query)
        return result.scalar_one_or_none()


    def get_all(self, **filters) -> List[ModelType]:
        """Получить все записи по фильтрам"""
        query = select(self.model).filter_by(**filters)
        result = self.session.execute(query)
        return result.scalars().all()


    def update(self, id: Any, **values) -> Optional[ModelType]:
        """Обновить запись"""
        query = (
            update(self.model)
            .where(self.model.id == id)
            .values(**values)
            .returning(self.model)
        )
        result = self.session.execute(query)
        self.session.commit()
        return result.scalar_one_or_none()


    async def delete(self, id: Any) -> bool:
        """Удалить запись"""
        query = delete(self.model).where(self.model.id == id)
        result = await self.session.execute(query)
        await self.session.commit()
        return result.rowcount > 0


    async def exists(self, **filters) -> bool:
        """Проверить существование"""
        query = select(self.model).filter_by(**filters)
        result = await self.session.execute(query)
        return result.first() is not None


    async def count(self, **filters) -> int:
        """Подсчитать количество"""
        query = select(self.model).filter_by(**filters)
        result = await self.session.execute(query)
        return len(result.scalars().all())