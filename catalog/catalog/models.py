import peewee
from typing import List

from catalog import database, db_manager


class Product(peewee.Model):
    """Продукт."""
    class Meta:
        database = database

    name = peewee.CharField(verbose_name='Наименование товара', max_length=256)
    price = peewee.IntegerField(verbose_name='Цена')

    def __str__(self):
        return f'{self.id}, {self.name}, {self.price}'

    @classmethod
    async def get_objects(cls):
        """Получение списка всех продуктов."""
        return await db_manager.execute(
            cls.select()
        )

    @classmethod
    async def get_objects_by_id(
        cls,
        ids: List[int]
    ):
        """Получение объектов по идентификаторам."""
        return await db_manager.execute(
            cls.select().where(cls.id.in_(ids))
        )
