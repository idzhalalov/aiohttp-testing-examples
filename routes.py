from api.views import QuestionHandler, ChoiceHandler

routes = [
    ('GET', '/api/v1/questions/{pk:\d+}', QuestionHandler, 'question_obj'),
    ('GET', '/api/v1/questions', QuestionHandler, 'questions'),
    ('POST', '/api/v1/questions', QuestionHandler, 'questions'),
    ('DELETE', '/api/v1/questions/{pk:\d+}', QuestionHandler, 'questions_obj'),
    ('GET', '/api/v1/choices', ChoiceHandler, 'choices'),
    ('POST', '/api/v1/choices', ChoiceHandler, 'choices'),
]


