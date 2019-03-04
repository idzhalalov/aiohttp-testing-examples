import logging
import settings


def get_logger(name: str='__main__', handler=None, formatter=None):
    if not handler:
        handler = settings.LOG_HANDLER

    if not formatter:
        formatter = settings.LOF_FORMATTER

    if not handler.formatter:
        handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(settings.LOG_LEVEL)

    return logger
