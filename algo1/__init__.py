import logging
import logging.config
import os

# Create and configure top-level logger to be parent to other loggers
logging.getLogger(__name__)
logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(levelname)8s [%(asctime)s] %(name)s:%(funcName)s (%(lineno)d) %(message)s"}},
    "handlers": { 
        "default": { 
            "level": "DEBUG",
            "formatter": "default",
            "class": "logging.StreamHandler"}},
    "loggers": { 
        __name__: {
            "level": "DEBUG",
            "handlers": ["default"]}}})
