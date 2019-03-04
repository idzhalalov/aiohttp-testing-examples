from aiohttp import web
from api.models import Question
import settings
from utils.helpers import get_logger


logger = get_logger(__name__)


def question_obj(data):
    return {
        'id': data.id,
        'question_text': data.question_text,
        'pub_date': str(data.pub_date),
        'created_at': str(data.created_at),
        'updated_at': str(data.updated_at) if data.updated_at else None
    }


class QuestionHandler(web.View):
    def __init__(self, request):
        self.pk = request.match_info.get('pk')
        super(QuestionHandler, self).__init__(request)

    async def get(self):
        code = 200
        page_num = int(self.request.query.get('page', '1'))

        logger.debug(f'Request: {self.request.url}')

        # A single object
        if self.pk:
            try:
                question = await Question.get_by(pk)
                result = question_obj(question)
            except Question.DoesNotExist:
                code = 404
                logger.debug(f'Object was not found by id {self.pk}')
                result = {
                    'id': self.pk,
                    'error_message': 'Object is not found by id'
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
                result.append(question_obj(question))

        logger.debug(f'Result: {result}')

        return web.json_response(result, status=code)

    async def post(self):
        data = await self.request.json()

        question = await Question.add(data)
        result = question_obj(question)

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
                'error_message': 'Object is not found by id'
            }
            return web.json_response(result, status=404)

        return web.json_response(status=202)
