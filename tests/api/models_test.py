from peewee_async import Manager

from api.models import Question, BaseModel, database


async def test_objects():
    # objects is an instance of peewee_async.Manager
    objects = BaseModel.objects()
    assert str(type(objects)) == str(type(Manager(database=database)))

    # both objects are referring to the same Manager
    objects2 = BaseModel.objects()
    assert objects == objects2


async def test_updated_at(db_objects, question_factory, faker):
    question = await question_factory.get()
    updated_at = question.updated_at

    question.question_text = faker.word()
    await db_objects.update(question)
    updated_question = await Question.get_by(question.id)

    print(f'updated_at - {updated_at}')
    print(f'updated_at - {updated_question.updated_at}')

    assert (updated_at == updated_question.updated_at) is False


async def test_question_add(question_factory):
    data = question_factory.initial_data()
    question = await Question.add(data)

    assert isinstance(question.id, int)
    assert question.id > 0
