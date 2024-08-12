# *****************************************************************************
# Author: Haley Kong
# Date Created: Sat Aug  3 10:51:24 2024
# Project: Heirloom Machine Interface
#
# Version History
# ---------------
# <DD-MM-YYYY> Initial Version
#
# *****************************************************************************
""" One-line Description:

"""
# Standard imports
import logging

# 3rd Party package imports

# Local imports

# -----------------------------------------------------------------------------
# CONSTANTS

# -----------------------------------------------------------------------------
# CLASSES


class CustomFormatter(logging.Formatter):
    green = "\x1b[32;20m"
    cyan = "\x1b[36;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "[%(levelname)s]:%(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: green + format + reset,
        logging.INFO: cyan + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class SimpleFormatter(logging.Formatter):
    format = "%(message)s"

    FORMATS = {
        logging.DEBUG: format,
        logging.INFO: format,
        logging.WARNING: format,
        logging.ERROR: format,
        logging.CRITICAL: format
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


CH = logging.StreamHandler()
CH.setFormatter(CustomFormatter())

CH_SIMPLE = logging.StreamHandler()
CH_SIMPLE.setFormatter(SimpleFormatter())

# -----------------------------------------------------------------------------
# FUNCTIONS

# -----------------------------------------------------------------------------

