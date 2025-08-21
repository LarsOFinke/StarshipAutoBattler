from ...config import (
    DEV_MODE,
    LOG_LEVEL,
    LOG_CONSOLE,
    LOG_FILE,
    LOG_FILE_NAME,
    LOG_FILE_TYPE,
)

from lars_logger import LoggerService

logger_service = LoggerService()

config = logger_service.get_logger_config(
    dev_mode=DEV_MODE,
    log_level=LOG_LEVEL,
    log_console=LOG_CONSOLE,
    log_file=LOG_FILE,
    log_file_name=LOG_FILE_NAME,
    log_file_type=LOG_FILE_TYPE,
)

logger = logger_service.get_custom_logger(name="Logger", config=config)
logger.log(logger, "dev-info")
log = logger.log
log_duration = logger.log_duration

test_logger = logger_service.get_test_logger()
