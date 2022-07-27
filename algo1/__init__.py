"""SENG 499 Company 4 Algorithm 1

Algorithm 1 generates a schedule given course, professor, preference, and
capacity data.

A top level logger is defined here as the parent to all other loggers. This
saves reconfiguring loggers for each module.
"""

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
