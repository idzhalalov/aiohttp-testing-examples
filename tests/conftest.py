import re
import asyncio
from datetime import datetime

import pytest
from faker import Faker
from aiohttp import web
from peewee_migrate import Router
from aiohttp.web_urldispatcher import DynamicResource

import settings
import api.models as models
from routes import routes

fake = Faker()
DB_NAME = settings.DB_NAME + '_test'


@pytest.fixture(scope='session', autouse=True)
def setup_db():
    # init db
    models.database.init(
        host=settings.DB_HOST,
        database=DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD)

    # run migrations
    router = Router(models.database)
    router.run()


@pytest.fixture(scope='session')
def faker():
    return fake


@pytest.fixture(scope='session')
def loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()

    yield loop
    loop.close()


@pytest.fixture
def cli(loop, aiohttp_client):

    app = web.Application()
    for route in routes:
        app.router.add_route(route[0], route[1], route[2], name=route[3])

    return loop.run_until_complete(aiohttp_client(app))


@pytest.fixture
async def route_path(cli):
    def _router_path(router_name, param=''):
        resource = cli.server.app.router[router_name]

        if isinstance(resource, DynamicResource):
            result = re.sub(r"{.+}", param, resource._formatter)
        else:
            result = resource._path

        return result

    return _router_path


@pytest.fixture
async def db_objects():
    return models.BaseModel.objects()


@pytest.fixture
async def question_factory(loop, request, db_objects):
    def cleanup_db():
        with db_objects.allow_sync():
            models.database.truncate_table(
                models.Question,
                restart_identity=True,
                cascade=True
            )

    class QuestionFactory:
        async def get(self):
            return await models.Question.add(self.initial_data())

        @staticmethod
        def initial_data():
            return {
                'question_text': fake.text(
                    max_nb_chars=models.Question.question_text.max_length),
                'pub_date': str(datetime.now())
            }

    request.addfinalizer(cleanup_db)

    return QuestionFactory()


@pytest.fixture
async def question(request, question_factory):
    if 'stop_question' not in request.keywords:
        return await question_factory.get()


@pytest.fixture
async def choice_factory(loop, question):

    class ChoiceFactory:
        async def get(self, question_obj=None):
            if not question_obj:
                question_obj = question

            return await models.Choice.add(self.initial_data(), question_obj.id)

        @staticmethod
        def initial_data(question_id=None):
            return {
                'question_id': question_id,
                'choice_text': fake.text(
                    max_nb_chars=models.Choice.choice_text.max_length),
                'votes': fake.random_number(3)
            }

    return ChoiceFactory()


@pytest.fixture
async def choice(request, choice_factory):
    if 'stop_choice' not in request.keywords:
        return await choice_factory.get()
