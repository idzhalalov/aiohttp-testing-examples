from aiohttp import web
from api.models import Question, Choice
import settings
from utils.helpers import get_logger
from json import JSONDecodeError


logger = get_logger(__name__)


class BaseHandler(web.View):
    def __init__(self, request):
        self.pk = request.match_info.get('pk')
        super(BaseHandler, self).__init__(request)


class QuestionHandler(BaseHandler):

    @staticmethod
    def _format_obj(question: Question):
        return {
            'id': question.id,
            'question_text': question.question_text,
            'pub_date': str(question.pub_date),
            'created_at': str(question.created_at),
            'updated_at': str(question.updated_at) if question.updated_at else None
        }

    async def get(self):
        code = 200
        page_num = int(self.request.query.get('page', '1'))

        logger.debug(f'Request: {self.request.url}')

        # A single object
        if self.pk:
            try:
                question = await Question.get_by(self.pk)
                result = self._format_obj(question)
            except Question.DoesNotExist:
                code = 404
                logger.debug(f'Object was not found by id {self.pk}')
                result = {
                    'id': self.pk,
                    'error_message': 'Object is not found by "id"'
                }
        # List of objects
        else:
            result = []

            questions = await Question.objects().execute(
                Question
                    .select()
                    .order_by(Question.pub_date.desc())
                    .paginate(page_num, settings.API_ITEMS_PER_PAGE)
            )

            for question in questions:
                result.append(self._format_obj(question))

        logger.debug(f'Result: {result}')

        return web.json_response(result, status=code)

    async def post(self):
        try:
            data = await self.request.json()
        except JSONDecodeError:
            result = {'error_message': 'Data is missing'}
            return web.json_response(
                result,
                status=web.HTTPBadRequest.status_code)

        question = await Question.add(data)
        result = self._format_obj(question)

        logger.debug(f'A new question added: {result}')

        return web.json_response(
            result,
            status=201
        )

    async def delete(self):
        logger.debug(f'Removing a question: id - {self.pk}')

        n = await Question.objects().execute(
            Question.delete().where(Question.id == self.pk)
        )

        if not n:
            logger.debug(f'Object was not found by id {self.pk}')
            result = {
                'id': self.pk,
                'error_message': 'Object is not found by "id"'
            }
            return web.json_response(result, status=404)

        return web.json_response(status=202)


class ChoiceHandler(BaseHandler):

    @staticmethod
    def _format_obj(choice: Choice):
        return {
            'id': choice.id,
            'question_id': choice.question_id,
            'choice_text': choice.choice_text,
            'votes': choice.votes,
            'created_at': str(choice.created_at) if choice.created_at else None,
            'updated_at': str(choice.updated_at) if choice.updated_at else None
        }

    async def get(self):
        result = []
        where_exp = None
        page_num = int(self.request.query.get('page', '1'))
        question_id = self.request.query.get('question_id')

        logger.debug(f'Request: {self.request.url}')

        # Filter by question_id
        if question_id:
            where_exp = (Choice.question_id == int(question_id))

        # List of objects
        choices = await Choice.objects().execute(
            Choice
                .select(Choice)
                .where(where_exp)
                .order_by(Choice.created_at.desc())
                .paginate(page_num, settings.API_ITEMS_PER_PAGE)
        )

        for choice in choices:
            result.append(self._format_obj(choice))

        logger.debug(f'Result: {result}')

        return web.json_response(result, status=web.HTTPOk.status_code)

    async def post(self):
        try:
            data = await self.request.json()
        except JSONDecodeError:
            result = {'error_message': 'Data is missing'}
            return web.json_response(
                result,
                status=web.HTTPBadRequest.status_code)

        question_id = data.get('question_id')

        # Data validation
        if not question_id:
            result = {
                'question_id': question_id,
                'error_message': 'Required field is missing of empty'
            }
            return web.json_response(
                result,
                status=web.HTTPNotFound.status_code)

        if not data.get('choice_text'):
            result = {
                'choice_text': None,
                'error_message': 'Required field is missing of empty'
            }
            return web.json_response(
                result,
                status=web.HTTPNotFound.status_code)

        # Save to DB
        try:
            choice = await Choice.add(data, question_id)
        except Question.DoesNotExist:
            error_message = (f'Error while adding a choice: '
                             f'question_id "{question_id}" is not found')

            logger.info(error_message)
            result = {
                'question_id': question_id,
                'error_message': error_message
            }

            return web.json_response(
                result,
                status=web.HTTPNotFound.status_code)

        result = self._format_obj(choice)
        logger.debug(f'A new choice added: {result}')

        return web.json_response(
            result,
            status=201
        )
