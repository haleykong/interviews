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
import os

# 3rd Party package imports

# Local imports
# FIXME: HACK TO BE ABLE TO RUN IN TERMINAL
# Didn't have time to set $PATH variable automatically.
os.sys.path.append("..")
from modules import machine as m
from utils import logconfig
from utils import pathconfig

# -----------------------------------------------------------------------------
# CONSTANTS
FILE = os.path.join(pathconfig.repo_root(),
                    "heirloom/data/configs/machine_configs/simulate.yml")
TXN_FILE = os.path.join(pathconfig.repo_root(),
                    "heirloom/data/configs/txn_configs/base.yml")


logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(logconfig.CH)
log.propagate = False


# -----------------------------------------------------------------------------
# CLASSES

# -----------------------------------------------------------------------------
# FUNCTIONS

# -----------------------------------------------------------------------------

# TESTING
log.info("Starting Tests...")

# Tray Tests
log.info("=" * 79)
log.info("1) Tray Tests:")
log.info("Initiating trays")
tray1 = m.Tray("A1")
tray2 = m.Tray("B2")
tray3 = m.Tray("C3")

log.info("Adding weight to Tray 1")
tray1.update_weight(10)
log.info(f"Tray {tray1.id} weight has been updated to {tray1.weight}")
log.info("Adding negative weights")
tray1.update_weight(-10)

# Vertical Stack Tests
log.info("=" * 79)
log.info("2) Vertical Stack Tests:")

log.info("Initiating vstack")
vstack = m.VStack()
log.info(vstack)

log.info("Adding trays...")
vstack.add_item(0, tray1)
vstack.add_item(1, tray2)
vstack.add_item(2, tray3)
log.info(vstack)

log.info("Check if slot 0 is available")
log.info(vstack.slot_available(0))
log.info("Check if slot 4 is available")
log.info(vstack.slot_available(4))

log.info("Removing tray at index 1")
vstack.remove_item(1)
log.info(vstack)

log.info("Attempt to add tray to Slot 0 while tray is present")
log.info(vstack.add_item(0, "xyz"))
log.info(vstack)

# Machine Tests
log.info("=" * 79)
log.info("3) Machine Tests:")

mach_1 = m.Machine()

# Initialize config from YAML file
machine_config = m.Config(FILE)
mach_1.configs = machine_config
# Dynamically modify configurations
mach_1.configs.simulate.machine_faults = False

log.info("")
log.info("Pick item from slot 0")
mach_1.pick(vstack, slot_index=0)
log.info(mach_1.transactions[-1])

# Test retry functionality
log.info("")
log.info("Retry picking item from slot 0 (1/4)")
mach_1.retry(vstack)
log.info(mach_1.transactions[-1])

log.info("")
log.info("Retry picking item from slot 0 (2/4)")
mach_1.retry(vstack)
log.info(mach_1.transactions[-1])

log.info("")
log.info("Retry picking item from slot 0 (3/4)")
mach_1.retry(vstack)
log.info(mach_1.transactions[-1])

log.info("")
log.info("Retry picking item from slot 0 (4/4)")
mach_1.retry(vstack)
log.info(mach_1.transactions[-1])

# Test more pick and place functionality
log.info("")
log.info("Place item in slot 4 (empty)")
mach_1.place(vstack, slot_index=4)
log.info(mach_1.transactions[-1])

log.info("")
log.info("Pick item from slot 1")
mach_1.pick(vstack, 1)
log.info(mach_1.transactions[-1])

log.info("")
log.info("Place item in slot 0")
mach_1.place(vstack, 0)
log.info(mach_1.transactions[-1])

# Create a transaction from YAML template
txn = m.Transaction(TXN_FILE)
# Modify transaction property
txn.metadata.retry = True


log.debug("debug message")
log.info("info message")
log.warning("warning message")
log.error("error message")
log.critical("critical message")
