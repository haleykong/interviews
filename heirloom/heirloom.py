from enum import Enum
import numpy as np
import logging


# CONSTANTS
MAX_NUM_RETRIES = 3
DEFAULT_NUM_SLOTS = 10


# LOGGING SET-UP
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


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

# create logger with 'spam_application'
logger = logging.getLogger("My_app")
logger.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

logger.debug("debug message")
logger.info("info message")
logger.warning("warning message")
logger.error("error message")
logger.critical("critical message")


class Actions(Enum):
    PICK = 0
    PLACE = 1


class ErrorCodes(Enum):
    SUCCESS = 0
    ITEM_NOT_PRESENT = 1
    LOCATION_OCCUPIED = 2
    RFID_READ = 3
    MACHINE_FAULTED = 4
    RETRIES_EXCEEDED = 5


class FailureCode(Enum):
    NONE = 0
    EQUIPMENT = 1


class Machine:
    """Interface for a machine on the processing line

    This interface is configured for machines that can perform pick
    and place operations. It will keep track of what it has picked
    and any associated errors.

    """

    MACHINE_FAULT_RATE = 0.1  # Probability of fault errors
    RFID_FAULT_RATE = 0.25  # Probability of RFID read errors

    def __init__(self,
                 simulate_machine_faults=False,
                 simulate_rfid_read=False):
        self.cur_item = None
        self.last_action = None
        self.last_result = None
        self.last_vstack = None
        self.last_slot_index = None
        self.num_retries = 0
        self.simulate_machine_faults = simulate_machine_faults
        self.simulated_rfid_read = simulate_rfid_read

    def check_machine(self):
        """Check to see if machine operated sucessfully

        This is used only for simulation as the machine faults should
        be coming from the equipment

        Returns
        -------
        error_code : str
            Error code of machine success or fault

        """
        if np.random.binomial(1, self.MACHINE_FAULT_RATE, 1):
            return ErrorCodes.MACHINE_FAULTED
        else:
            return ErrorCodes.SUCCESS

    def read_rfid(self):
        if np.random.binomial(1, self.RFID_FAULT_RATE, 1):
            return ErrorCodes.RFID_READ
        else:
            return ErrorCodes.SUCCESS

    def pick(self, vstack, slot_index):
        # Check for machine fault
        if self.simulate_machine_faults:
            status = self.check_machine()

        if status == ErrorCodes.SUCCESS:
            # Check for item present
            if vstack.slot_available(slot_index):
                self.num_retries += 1
                self.last_action = Actions.PICK
                self.last_vstack = vstack
                self.last_slot_index = slot_index
                self.last_result = ErrorCodes.ITEM_NOT_PRESENT
                self.retry()

    def check_retries(self):
        """

        Returns
        -------
        error_code
            Error code if number of retires has exceeded maximum number of
            retries

        """
        if self.num_retries >= MAX_NUM_RETRIES:
            return ErrorCodes.RETRIES_EXCEEDED
        return

        # if self.pick() == Machine.errorMachineFaulted:
        #     return Failure.EQUIPMENT
        # elif self.count == MAX_RETRIES:
        #     return Failure.EQUIPMENT
        # elif self.pick() == Machine.errorItemNotPresent:
        #     self.count += 1
        #     self.pick()
        # elif self.pick() == Machine.errorRFIDRead:
        #     self.count += 1
        #     # Item must first be successfully placed before retrying pick op
        #     if self.place():
        #         self.pick()
        #     else:
        #         pass
        #         # ???
        # else:
        #     self.count = 0


    def place(self, vstack, slot_index):
        pass

    def retry(self):
        self.check_retries()

        # Retry for item not present
        if self.last_result == ErrorCodes.ITEM_NOT_PRESENT:
            pick(self.last_vstack, self.last_slot_index)


class VStack:
    """Structure that holds the trays in vertical stacks
    """

    def __init__(self, num_slots=DEFAULT_NUM_SLOTS):
        self.slots = [""] * num_slots

    def add_tray(self, index, t_id):
        if self.slot_available(index):
            self.slots[index] = t_id
            return ErrorCodes.SUCCESS
        else:
            log.error(
                f"ERROR: Could not add tray '{t_id}' at index {index}: "
                f"{ErrorCodes.LOCATION_OCCUPIED.name}")
            return ErrorCodes.LOCATION_OCCUPIED

    def remove_tray(self, index):
        if self.slot_available(index):
            log.error(
                f"ERROR: Could not remove tray from index {index}: "
                f"{ErrorCodes.ITEM_NOT_PRESENT.name}"
            )
            return ErrorCodes.ITEM_NOT_PRESENT
        else:
            self.slots[index] = ""
            return ErrorCodes.SUCCESS

    def slot_available(self, index):
        return self.slots[index] == ""


class Tray:
    """Container that contains material for processing
    """

    def __init__(self, tray_id):
        self.id = tray_id
        self.weight = 0
        self.dry_duration = 0  # To be integrated with the dryer step
        self.prev_step = None

    def update_weight(self, weight):
        if weight >= 0:
            self.weight = weight
        else:
            log.error("ERROR: Please enter a valid weight (kg)")

# TESTING
log.info("Starting Tests...")

# Tray Tests
log.info("=" * 79)
log.info("1) Tray Tests:")
log.info("Initiating trays...")
tray1 = Tray("A1")
tray2 = Tray("B2")
tray3 = Tray("C3")

log.info("Adding weights")
tray1.update_weight(10)
log.info(f"Tray {tray1.id} weight has been updated to {tray1.weight}")
log.info("Adding negative weights")
log.info(tray1.update_weight(-10))

# Vertical Stack Tests
log.info("=" * 79)
log.info("2) Vertical Stack Tests:")

log.info("Initiating vstack...")
vstack = VStack()
log.info(vstack.slots)

log.info("Adding trays...")
vstack.add_tray(0, "abc")
vstack.add_tray(1, "def")
vstack.add_tray(2, "egh")
log.info(vstack.slots)

log.info("Removing tray at index 1")
vstack.remove_tray(1)
log.info(vstack.slots)

log.info("Attempt to add while tray is present")
log.info(vstack.add_tray(0, "xyz"))
log.info(vstack.slots)

# Machine Tests
log.info("=" * 79)
log.info("3) Vertical Stack Tests:")

m = Machine(simulate_machine_faults=True, simulate_rfid_read=True)
# Pick item at slot 0
m.pick(vstack, slot_index=0)

# # Put item into slot 3 (empty)
# h.place(3)

# # Pick item at slot 1
# h.pick(1)

# # Put it in slot 0
# h.place(0)

