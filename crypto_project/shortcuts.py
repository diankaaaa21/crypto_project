import logging
import os
from logging.handlers import RotatingFileHandler

from django.conf import settings


def file_logger(name, _handler=None):
    log_dir = os.path.join(settings.DJANGO_ROOT, "var", "log")
    os.makedirs(log_dir, exist_ok=True)

    filename = os.path.join(log_dir, f"{name}.log")
    log = logging.getLogger(name)
    if log.handlers:
        return log

    _handler = _handler or RotatingFileHandler(
        filename,
        maxBytes=10 * 1024 * 1024,
        backupCount=4,
    )
    _formatter = logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    _handler.setFormatter(_formatter)
    _handler.setLevel(logging.INFO)
    log.setLevel(logging.INFO)
    log.addHandler(_handler)
    return log