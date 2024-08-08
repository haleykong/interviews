# Heirloom Carbon
# Senior Backend Software Engineer

# https://codeshare.io/8Xn7KB

from enum import Enum


MAX_RETRIES = 3

class Failure(Enum):
    NONE = 0
    EQUIPMENT = 1


class RetryMachine(Machine):

    def __init__(self):
        self.count = 0  # Count number of retries

    def pick(self):
        if self.pick() == Machine.errorMachineFaulted:
            return Failure.EQUIPMENT
        elif self.count == MAX_RETRIES:
            return Failure.EQUIPMENT
        elif self.pick() == Machine.errorItemNotPresent:
            self.count += 1
            self.pick()
        elif self.pick() == Machine.errorRFIDRead:
            self.count += 1
            # Item must first be successfully placed before retrying pick op
            if self.place():
                self.pick()
            else:
                pass
                # ???
        else:
            self.count = 0

    def place(self):
        if self.place() == Machine.errorMachineFaulted:
            return Failure.EQUIPMENT
        elif self.count == MAX_RETRIES:
            return Failure.EQUIPMENT
        elif self.place() == Machine.errorLocationOccupied:
            self.count += 1
            self.place()
        elif self.place() == Machine.errorRFIDRead:
            self.count += 1
            # Item must first be successfully picked before retrying place op
            if self.pick():
                self.place()
            else:
                pass
                # ???
        else:
            self.count = 0

# QUESTIONS
# Can you retry the failed pick and place operations up to 3 times each or total?
# Up to 3 times per type of error?
# How do you tell if the item is successfully picked or placed?
# What do you do if the item is not successfully placed?
# Does the retry counter reset for machine faulted? Or does that count as a retry?
# What is returned if you exceed the 3 retries?

# IMPROVEMENTS
# Need different levels of errors
# Status for success
# Counter by error message