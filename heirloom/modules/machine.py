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
from enum import Enum
import numpy as np
import logging
from datetime import datetime
from collections import deque
import tabulate as tab
import os

# 3rd Party package imports
import yaml

# Local imports
from utils import logconfig
from utils.db import HierarchicalDict
from utils import pathconfig

# -----------------------------------------------------------------------------
# CONSTANTS
ID_LENGTH = 10
MAX_NUM_RETRIES = 3
DEFAULT_NUM_SLOTS = 10
NUM_OP_CHECK = 3  # Must be 2 or greater

log = logging.getLogger(__name__)
log.addHandler(logconfig.CH)
log.propagate = False

# -----------------------------------------------------------------------------
# CLASSES


class Actions(Enum):
    PICK = 0
    PLACE = 1


class _Check(Enum):
    SUCCESS = 0
    MACHINE_OCCUPIED = 1
    MACHINE_EMPTY = 2
    SLOT_OCCUPIED = 3
    SLOT_EMPTY = 4


class _Actuate(Enum):
    SUCCESS = 0
    FAULTED = 1


class _Rfid(Enum):
    SUCCESS = 0
    READ_ERROR = 1


class _RetryCheck(Enum):
    SUCCESS = 0
    RETRIES_EXCEEDED = 1


class _VStack(Enum):
    SUCCESS = 0
    SLOT_OCCUPIED = 1
    SLOT_EMPTY = 2


class ErrorCodes:
    CHECK = _Check
    ACTUATE = _Actuate
    RFID = _Rfid
    RETRY_CHECK = _RetryCheck
    VSTACK = _VStack


class Machine:
    """Interface for a machine on the processing line

    This interface is configured for machines that can perform pick
    and place operations. It will keep track of what it has picked
    and any associated errors.

    """

    MACHINE_FAULT_RATE = 0  # Probability of fault errors
    RFID_FAULT_RATE = .25  # Probability of RFID read errors

    def __init__(self):
        self.cur_item = None
        self.transactions = deque(maxlen=MAX_NUM_RETRIES + 1)
        self.configs = None  # TODO


    def _check_operation(self, operation, vstack):
        """Check to see if machine is able to execute its operation

        This is dependent on the state of the environment

        Parameters
        ----------
        operation : enum
            Type of operation the machine will be executing
        vstack : VStack
            VStack at which the machine will be executing its operation

        Raises
        ------
        Exception
            Invalid operation

        Returns
        -------
        ErrorCode : enum
            Error code of check operation step

        """
        action, slot_index = operation

        # Pick action checks
        if action == Actions.PICK:
            # Robot should not have an item
            if self.cur_item:
                return ErrorCodes.CHECK.MACHINE_OCCUPIED
            # Slot should not be occupied
            elif vstack.slot_available(slot_index):
                return ErrorCodes.CHECK.SLOT_EMPTY
            else:
                return ErrorCodes.CHECK.SUCCESS

        # Place action checks
        elif action == Actions.PLACE:
            # Robot should have an item
            if self.cur_item is None:
                return ErrorCodes.CHECK.MACHINE_EMPTY
            elif not vstack.slot_available(slot_index):
                return ErrorCodes.CHECK.SLOT_OCCUPIED
            else:
                return ErrorCodes.CHECK.SUCCESS

        # Action is invalid
        else:
            err_msg = f"Action {action} invalid"
            log.error(err_msg)
            raise Exception(err_msg)

    def _actuate(self, operation, vstack):
        """Check to see if machine operated sucessfully

        This is used only for simulation as the machine faults should
        be coming from the equipment

        Returns
        -------
        ErrorCode : enum
            Error code of machine success or fault

        """
        error_code = None
        if self.configs.simulate.machine_faults:
            if np.random.binomial(1, self.MACHINE_FAULT_RATE, 1):
                error_code = ErrorCodes.ACTUATE.FAULTED
            else:
                error_code = ErrorCodes.ACTUATE.SUCCESS
        else:
            # FIXME: machine specific actuation API
            error_code = ErrorCodes.ACTUATE.SUCCESS

        # Update state of Machine if actuation was successful
        if error_code == ErrorCodes.ACTUATE.SUCCESS:
            if operation[0] == Actions.PICK:
                slot_index = operation[1]
                self.cur_item = vstack.slots[slot_index]
                vstack.remove_item(slot_index)
            elif (operation[0] == Actions.PLACE):
                slot_index = operation[1]
                vstack.add_item(slot_index, self.cur_item)
                self.cur_item = None
        return error_code


    def _read_rfid(self):
        """Check to see if RFID was read sucessfully

        This is used only for simulation as the RFID read faults should
        be coming from the equipment

        Returns
        -------
        ErrorCode : enum
            Error code of machine success or fault

        """
        if self.configs.simulate.machine_faults:
            if np.random.binomial(1, self.RFID_FAULT_RATE, 1):
                return ErrorCodes.RFID.READ_ERROR
            else:
                return ErrorCodes.RFID.SUCCESS
        else:
            # Some RFID api read machine specific.
            return ErrorCodes.RFID.SUCCESS

    def carry_op(self, operation, vstack, retry=False):
        """
        Parameters
        ----------
        operation : tuple
            Actions.ENUM, slot_index = operation
        vstack: Vstack

        Returns
        -------
        None

        """
        error_codes = []

        # Check if operation is allowed
        error_codes.append(self._check_operation(operation, vstack))
        if error_codes[0] == ErrorCodes.CHECK.SUCCESS:
            # Actuation
            error_codes += [self._actuate(operation, vstack)]
            # RFID read
            error_codes += [self._read_rfid()]
        else:
            error_codes += [None] * (NUM_OP_CHECK - 1)

        # Update machine and vstack accordingly
        error_code_sum = sum(
            error.value
            for error in error_codes
            if error is not None
        )

        # Create and store metadata
        metadata = {
            'operation': operation,
            'error_codes': error_codes,
            'retry': retry
        }
        return Transaction(metadata)

    def pick(self, vstack, slot_index):
        operation = (Actions.PICK, slot_index)
        txn = self.carry_op(operation, vstack)
        self.transactions.append(txn)

    def place(self, vstack, slot_index):
        operation = (Actions.PLACE, slot_index)
        txn = self.carry_op(operation, vstack)
        self.transactions.append(txn)

    def retry(self, vstack):
        err_code = self._check_retries()
        if err_code != ErrorCodes.RETRY_CHECK.RETRIES_EXCEEDED:
            txn = self.carry_op(self.transactions[-1].metadata['operation'],
                                vstack, retry=True)
        else:
            metadata = {
                'operation':
                    self.transactions[-1].metadata['operation'],
                'error_codes': [err_code] * NUM_OP_CHECK,
                'retry': True
            }
            txn = Transaction(metadata)
        self.transactions.append(txn)

    def _check_retries(self):
        """Check if the machine has exceeded the maximum number of retries

        Returns
        -------
        error_code
            Error code if number of retires has exceeded maximum number of
            retries

        """
        # Check total number of transactions
        if len(self.transactions) < MAX_NUM_RETRIES:
            return ErrorCodes.RETRY_CHECK.SUCCESS
        else:
            # Check if the past transactions have been retries
            for ii in range(1, MAX_NUM_RETRIES + 1):
                if self.transactions[-ii].metadata['retry'] is False:
                    return ErrorCodes.RETRY_CHECK.SUCCESS
        return ErrorCodes.RETRY_CHECK.RETRIES_EXCEEDED


class Transaction:
    """Class that holds the transaction metadata
    """
    FORMAT_FILE = os.path.join(pathconfig.repo_root(),
                               "heirloom/data/configs/txn_configs/base.yml")

    def __init__(self, metadata: dict):
        # Get transaction data template from YAML file
        data = Config(Transaction.FORMAT_FILE)

        # Update data with calculated data
        data['timestamp'] = datetime.now()
        data['error_codes'] = [None] * NUM_OP_CHECK

        # Update data with transaction data
        for key in data.keys():
            if key in metadata:
                data[key] = metadata[key]

        # Update with calculated result
        error_code_sum = sum(
            error.value
            for error in data.error_codes
            if error is not None
        )
        if error_code_sum == 0:
            data['result'] = "Pass"
        else:
            data['result'] = "Fail"

        self.metadata = HierarchicalDict(data)

    def __repr__(self):
        repstr = '-' * 79 + '\nTransaction Summary\n'
        repstr += HierarchicalDict._print(self.metadata)
        return repstr


class Config(HierarchicalDict):

    def __init__(self, data):
        """

        Parameters
        ----------
        data : str | dict
            Configuration data from the user as either an absolute path to yml
            file or a dictionary

        Returns
        -------
        None.

        """
        # Data is filepath of yml
        if isinstance(data, str):
            try:
                with open(data, 'r') as file:
                    data = yaml.safe_load(file)
            except FileNotFoundError:
                err_msg = f"File {data} was not found"
                log.error(err_msg)
            except yaml.YAMLError as e:
                err_msg = f"File {data} could not be loaded: {str(e)}"
                log.error(err_msg)
                raise
            except Exception as e:
                err_msg = (
                    f"An unexpected error occurred while loading the file "
                    f"{data}: {str(e)}"
                )
                log.error(err_msg)
                raise

        # Data should be a dictionary
        if not isinstance(data, dict):
            err_msg = "Data must be a dictionary"
            log.error(err_msg)
            raise Exception(err_msg)
        # Parse data
        else:
            super().__init__(data)


class VStack:
    """Class that holds the items in vertical stacks
    """

    def __init__(self, num_slots=DEFAULT_NUM_SLOTS):
        self.slots = [None] * num_slots

    def __repr__(self):
        return self._ascii_representation()

    def _ascii_representation(self):
        rows = [['Slot Index', 'ID']]
        rows += [[f'{ii}', f'{slot}'] for ii, slot in enumerate(self.slots)]
        # You want the rows to go bottom up
        rows.reverse()
        return tab.tabulate(rows, headers='firstrow', tablefmt='fancy_grid')

    def add_item(self, index, item):
        if self.slot_available(index):
            self.slots[index] = item
            return ErrorCodes.VSTACK.SUCCESS
        else:
            log.error(
                f"Could not add item '{item}' at slot {index}: "
                f"{ErrorCodes.VSTACK.SLOT_OCCUPIED.name}")
            return ErrorCodes.VSTACK.SLOT_OCCUPIED

    def remove_item(self, index):
        if self.slot_available(index):
            log.error(
                f"Could not remove item from slot {index}: "
                f"{ErrorCodes.ITEM_NOT_PRESENT.name}"
            )
            return ErrorCodes.VSTACK.SLOT_EMPTY
        else:
            self.slots[index] = None
            return ErrorCodes.VSTACK.SUCCESS

    def slot_available(self, index):
        return self.slots[index] is None


class Item:
    """General container used for tracking
    """

    def __init__(self, item_id):
        self.id = item_id


class Tray(Item):
    """Item that contains material for processing
    """

    def __init__(self, item_id):
        super().__init__(item_id)
        self.weight = 0

    def __repr__(self):
        return f"{self.id}"

    def update_weight(self, weight):
        if weight >= 0:
            self.weight = weight
        else:
            log.error("Please enter a valid weight (kg)")


# -----------------------------------------------------------------------------
# FUNCTIONS

# -----------------------------------------------------------------------------
# metadata = {'operation': 'pick'}
# t = Transaction(metadata)
