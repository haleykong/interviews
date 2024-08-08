# ****************************************************************************
# Author: Haley Kong
# Date Created: Sat Aug  3 13:22:36 2024
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

# 3rd Party package imports

# Local imports

# -----------------------------------------------------------------------------
# # CONSTANTS
# import logging
# # -----------------------------------------------------------------------------
# # CLASSES

# # -----------------------------------------------------------------------------
# # FUNCTIONS

# # -----------------------------------------------------------------------------
# from modules import scratch


# log2 = logging.getLogger(__name__)
# ch2 = logging.StreamHandler()
# ch2.setFormatter(scratch.CustomFormatter())
# # Create console handler with a higher log level
# log2.addHandler(ch2)
# log2.propagate = False

# log2.warning("SCRACHT2")

# scratch.blah()

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
from modules import machine as m
from utils import logconfig

# -----------------------------------------------------------------------------
# CONSTANTS
logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(logconfig.CH_SIMPLE)
log.propagate = False