# -*- coding: utf-8 -*-
"""
    pysimplebgc.logger
    ------------------

    Logging setup.

    :copyright: Copyright 2015 Lionel Darras and contributors, see AUTHORS.
    :license: GNU GPL v3.

"""
from __future__ import unicode_literals
import logging
from .compat import NullHandler
from logging import NullHandler


LOGGER = logging.getLogger('blasterGimbal')
LOGGER.addHandler(NullHandler())


def active_logger():
    '''Initialize a speaking logger with stream handler (stderr).'''
    LOGGER = logging.getLogger('blasterGimbal')

    LOGGER.setLevel(logging.INFO)
    logging.getLogger('pylink').setLevel(logging.INFO)

    # Default to logging to stderr.
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s ')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    LOGGER.addHandler(stream_handler)
    logging.getLogger('pylink').addHandler(stream_handler)
