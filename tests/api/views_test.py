import settings
from aiohttp import web
import pytest
from api.models import Question


async def test_get_question(cli, route_path, question_factory):
    question = await question_factory.get()

    resp = await cli.get(route_path('question_obj', str(question.id)))
    resp_json = await resp.json()

    print(resp_json)

    assert (question.id == resp_json.get('id')) is True


async def test_get_questions(cli, route_path, question_factory):
    for _ in range(settings.API_ITEMS_PER_PAGE):
        await question_factory.get()

    resp = await cli.get(route_path('questions'))
    resp_json = await resp.json()

    print(resp_json)

    assert (len(resp_json) == settings.API_ITEMS_PER_PAGE) is True


async def test_post_question(cli, route_path, question_factory):
    data = question_factory.initial_data()

    resp = await cli.post(route_path('questions'), json=data)
    resp_json = await resp.json()

    print(resp_json)

    assert (resp_json.get('id') > 0) is True


async def test_delete_question(cli, route_path, question):
    resp = await cli.delete(route_path('question_obj', str(question.id)))

    assert (resp.status == web.HTTPAccepted.status_code) is True
    with pytest.raises(Question.DoesNotExist):
        await Question.get_by(question.id)


async def test_get_choices(cli, route_path, choice_factory):
    for _ in range(settings.API_ITEMS_PER_PAGE):
        await choice_factory.get()

    resp = await cli.get(route_path('choices'))
    resp_json = await resp.json()

    print(resp_json)

    assert (len(resp_json) == settings.API_ITEMS_PER_PAGE) is True


async def test_get_choices_by_question_id(cli, route_path, question_factory,
                                          choice_factory):
    for _ in range(settings.API_ITEMS_PER_PAGE):
        question = await question_factory.get()

    choices_count = int(settings.API_ITEMS_PER_PAGE - 1)
    if choices_count <= 0:
        choices_count = 1

    for _ in range(choices_count):
        await choice_factory.get(question)

    choice_uri = route_path(f'choices')
    resp = await cli.get(f'{choice_uri}?question_id={question.id}')
    resp_json = await resp.json()

    print(resp_json)

    assert (len(resp_json) == choices_count) is True


async def test_post_choice(cli, route_path, question, choice_factory):
    data = choice_factory.initial_data(question.id)

    resp = await cli.post(route_path('choices'), json=data)
    resp_json = await resp.json()

    print(resp_json)

    assert (resp_json.get('id') > 0) is True
