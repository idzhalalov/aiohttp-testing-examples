from os.path import isfile
from envparse import env
import logging

ENV = env.str('ENV', default='.env')
if isfile(ENV):
    env.read_envfile(ENV)

# Define settings
DB_HOST = env.str('DB_HOST')
DB_PORT = env.int('DB_PORT')
DB_NAME = env.str('DB_NAME')
DB_USER = env.str('DB_USER')
DB_PASSWORD = env.str('DB_PASSWORD')

# logging
LOG_LEVEL = env.str('LOG_LEVEL', default='ERROR')
LOG_HANDLER = logging.StreamHandler()
LOF_FORMATTER = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

APP_HOST = env.str('APP_HOST', default='127.0.0.1')
APP_PORT = env.str('APP_PORT', default='8000')
API_ITEMS_PER_PAGE = env.int('API_ITEMS_PER_PAGE', default=10)
