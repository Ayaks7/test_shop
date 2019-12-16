import peewee

from auth import database, db_manager


class ProfileUser(peewee.Model):
    """Пользователь."""
    class Meta:
        database = database

    username = peewee.CharField(
        verbose_name='Логин', max_length=32, unique=True
    )
    email = peewee.CharField(
        verbose_name='Почта', max_length=128, unique=True, null=True
    )
    password = peewee.CharField(
        verbose_name='Пароль', max_length=128, null=True
    )
    full_name = peewee.CharField(verbose_name='ФИО', max_length=128, null=True)
    phone = peewee.CharField(verbose_name='Телефон', max_length=32, null=True)
    address = peewee.CharField(verbose_name='Адрес', max_length=128, null=True)

    def __str__(self):
        return f'{self.username}, {self.full_name}'

    @classmethod
    async def get_objects_by_id(
        cls,
        object_id: int
    ):
        """Получение пользователя по идентификатору."""
        try:
            user = await db_manager.get(cls, id=object_id)
        except cls.DoesNotExist:
            return None
        return user

    @classmethod
    async def get_object_for_auth(
        cls,
        username: str
    ):
        """Получение пользователя по уникальному логину."""
        try:
            user = await db_manager.get(cls, username=username)
        except cls.DoesNotExist:
            return None
        return user
