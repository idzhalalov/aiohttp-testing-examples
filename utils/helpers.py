import logging
import settings


def get_logger(name: str='__main__', handler=None):
    if not handler:
        handler = logging.StreamHandler()

    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(settings.LOG_LEVEL)

    return logger
