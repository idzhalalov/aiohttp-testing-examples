from datetime import datetime

from peewee import *
from peewee import ForeignKeyField
from peewee_async import Manager, PostgresqlDatabase

database = PostgresqlDatabase(None)


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


class Question(BaseModel):
    question_text = CharField(max_length=200)
    pub_date = DateTimeField('date published')

    @classmethod
    async def add(cls, data):
        result = await Question.objects().create(
            Question,
            question_text=data.get('question_text'),
            pub_date=data.get('pub_date', datetime.now())
        )

        return result


class Choice(BaseModel):
    question = ForeignKeyField(
        Question,
        object_id_name='question_id',
        related_name='choice',
        db_column='question_id'
    )
    choice_text = CharField(max_length=200)
    votes = IntegerField(default=0)

    @classmethod
    async def add(cls, data, question_id):
        try:
            await Question.objects().get(Question, id=question_id)
        except Question.DoesNotExist:
            raise Question.DoesNotExist()

        result = await Choice.objects().create(
            Choice,
            question_id=question_id,
            choice_text=data.get('choice_text'),
            votes=data.get('votes', 0)
        )

        return result
