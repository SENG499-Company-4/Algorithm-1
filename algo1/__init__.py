import logging
import logging.config

# Create and configure top-level logger to be parent to other loggers
logger = logging.getLogger(__name__)
logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(levelname)8s [%(asctime)s] %(name)s:%(funcName)s (%(lineno)d) %(message)s"}},
    "handlers": { 
        "default": { 
            "formatter": "default",
            "class": "logging.StreamHandler"}},
    "loggers": { 
        __name__: {
            "handlers": ["default"]}}})
