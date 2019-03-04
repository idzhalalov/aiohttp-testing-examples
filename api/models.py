from datetime import datetime

from peewee import *
from peewee_async import Manager
from peewee_asyncext import PostgresqlExtDatabase

database = PostgresqlExtDatabase(None)


class BaseModel(Model):
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(null=True)

    def update(self, *args, **update):
        update['updated_at'] = datetime.now()

        return super(BaseModel, self).update(*args, **update)

    @classmethod
    def objects(cls):
        try:
            if cls.manager:
                pass
        except AttributeError:
            cls.manager = Manager(cls._meta.database)
        return cls.manager

    @classmethod
    async def get_by(cls, pk: int=None, expression: 'peewee.Expression'=None):
        if not expression:
            expression = (cls.id == pk)

        if not expression and not pk:
            raise ValueError('Either pk or expression should be passed')

        return await cls.objects().get(cls, expression)

    class Meta:
        database = database
        legacy_table_names = False
