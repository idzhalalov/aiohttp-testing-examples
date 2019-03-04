from api.views import QuestionHandler

routes = [
    ('GET', '/api/v1/questions/{pk:\d+}', QuestionHandler, 'question_obj'),
    ('GET', '/api/v1/questions', QuestionHandler, 'question'),
    ('POST', '/api/v1/questions', QuestionHandler, 'question'),
]
