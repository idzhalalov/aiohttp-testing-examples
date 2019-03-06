from aiohttp import web
from peewee_migrate import Router

import settings
from routes import routes
from api.models import database
from utils.helpers import get_logger

app = web.Application()
logger = get_logger()

# Routes
for route in routes:
    app.router.add_route(route[0], route[1], route[2], name=route[3])

# Database connection
database.init(
    host=settings.DB_HOST,
    database=settings.DB_NAME,
    user=settings.DB_USER,
    password=settings.DB_PASSWORD)

# Run migrations
router = Router(database)
router.run()

# Run app
logger.debug('Application is started')
web.run_app(app, host=settings.APP_HOST, port=settings.APP_PORT)
logger.debug('Application is stopped')
