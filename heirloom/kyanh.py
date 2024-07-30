import enum

class Handler:
    """This is some sort of machine interface
   
    Actually this is handler (also called "RetryMachine")
    (Cheap ATE)
   
    Ideally it can be shared for any machines that has:
        - pick/place type operations
        - has a bunch of slots that are either occupied or not
        occupied.
       
    The machine interface object keeps track of what it current
    ly has picked.
    """
    def __init__(self, nretry=3):
        self.cur_item = None
        self.last_action = None
        self.last_result = None
        self.num_retries = nretry
       
    def retry(self):
        """My job.

        Returns
        -------
        None.
        """
           
           

    def pick(slots, slot_index):
        """Written by tao

        Parameters
        ----------
        slots : slots object
            some slots object handler is interacting with
        slot_index : int
            index at which you are picking

        Returns
        -------
        None.
        """

    def place(slots, slot_index):
        """Written by colin

        Parameters
        ----------
        slots : slots object
            some slots object handler is interacting with
        slot_index : int
            index at which you are placing

        Returns
        -------
        None.
        """

class SlotState(enum.enum):
    EMPTY = 0
    FULL = 1

class ErrorCodes(enum.enum):
    ITEM_NOT_PRESENT = 0
    LOCATION_OCCUPIED = 1
    RFID_READ = 2
    MACHINE_FAULTED = 3
    SUCCESS = 4

class Slots():
    """This is a prototypical line of objects
   
    Basically keeps track of the state of the slots
    """
    def __init__(self, num_slots=5):
        self.slots = [SlotState.EMPTY] * num_slots
       
    def add_item(self, loc, item):
        self.slots[loc] = item
   
    def remove_item(self, loc):
        self.slots[loc] = SlotState.EMPTY
       
class Item():
    """Prototype class for items
    aka stuff you can put in a slot
    """
    def __init__(self, id_num):
        self.id = id_num
# Example of how we may want to use this (API definition)

# Instantiate a handler
h = Handler()

# Create a bunch of items
NUM_ITEMS = 3
items = [Item(ID=ii) for ii in range(NUM_ITEMS)]

# Create slots
slots = Slots(num_slots=5)

# Put items in slot 0,... NUM_ITEMS-1
for loc, item in enumerate(items):
    slots.add_item(loc, item)

# Interact with the slots with the handler (machine interface)

# pick item at slot 0
h.pick(0)

# put item into slot 3 (empty)
h.place(3)

# pick item at slot 1
h.pick(1)

# put it in slot 0
h.place(0)

# ...