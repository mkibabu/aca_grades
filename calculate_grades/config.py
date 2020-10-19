import logging
import os
import pathlib
from logging.config import dictConfig


log_conf = dict(
    version=1,
    formatters={
        "simple": {"format": "%(asctime)s %(name)s %(levelname)s: %(message)s"},
    },
    handlers={
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": logging.DEBUG,
        },
    },
    root={
        "handlers": ["console"],
        "level": logging.DEBUG,
    },
)

dictConfig(log_conf)

# location of input files. Defaults to top-level directory
# named "input".
INPUT_LOCATION = os.environ.get('INPUT_LOCATION', 'input')
INPUT_DIR = pathlib.Path(__file__).parents[1].joinpath(INPUT_LOCATION)
