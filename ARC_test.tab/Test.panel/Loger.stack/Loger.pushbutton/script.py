from pyrevit import script

logger = script.get_logger()

logger.info('Test Info Log Level :OK_hand:')
logger.success('Test Success Log Level')
logger.debug('Test Debug Log Level')
logger.warning('Test Warning Log Level')
logger.error('Test Error Log Level')
logger.critical('Test Critical Log Level')
logger.deprecate('Test Deprecate Message')

