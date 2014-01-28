import logging
import logging.handlers

logger = logging.getLogger('novalog')
logger.setLevel(logging.DEBUG)


http_handler = logging.handlers.HTTPHandler(
    'localhost:8000',
    '/remotelog/novalog/log/',
    method='POST',
)
logger.addHandler(http_handler)

logger.debug('Fuck')
logger.info('Fuck')
logger.warn('Fuck')
