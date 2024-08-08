# ****************************************************************************
# Author: Haley Kong
# Date Created: Wed Aug  7 16:15:46 2024
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
import threading
import time
import sys

# 3rd Party package imports

# Local imports
from utils import consts as c

# -----------------------------------------------------------------------------
# CONSTANTS
KIRBY_DANCE = c.KIRBY_DANCE
PROGRESS_BAR_DURATION = 10  # Adjust this as needed
PROGRESS_BAR_STEPS = 20  # Adjust this as needed
DANCE_DELAY = 0.1  # Adjust this to make the dance slower

# -----------------------------------------------------------------------------
# CLASSES
# Class to manage the progress bar thread
class ProgressBarThread(threading.Thread):
    def __init__(self, duration, steps):
        super().__init__()
        self.duration = duration
        self.steps = steps
        self._stop_event = threading.Event()

    def run(self):
        progress_bar(self.duration, self.steps)

    def stop(self):
        self._stop_event.set()
        self.join()


# -----------------------------------------------------------------------------
# FUNCTIONS


# Function to create the progress bar with Kirby dancing
def progress_bar(duration, steps, delay):
    for i in range(steps):
        # Calculate progress
        progress = (i + 1) / steps
        # Print Kirby's current dance move and progress
        sys.stdout.write(
            f"\r{KIRBY_DANCE[i % len(KIRBY_DANCE)]} [{int(progress * 100)}%]"
        )
        sys.stdout.flush()
        time.sleep(delay)
    # Final dance move
    sys.stdout.write(f"\r{KIRBY_DANCE[-1]} [{int(progress * 100)}%]")
    print()  # Move to the next line after completion


# -----------------------------------------------------------------------------
progress_bar(PROGRESS_BAR_DURATION, PROGRESS_BAR_STEPS, DANCE_DELAY)