"""<One-line description.>

<More detailed description here.>
"""

# standard imports

# 3rd party package imports

# local imports


# -----------------------------------------------------------------------------
# CONSTANTS

# -----------------------------------------------------------------------------
# CLASSES

# -----------------------------------------------------------------------------
# FUNCTIONS

# -----------------------------------------------------------------------------
"""Module that provides path configurations."""

import os
# Path of Python project relative to Git repo root directory
PROJ_REV_PATH = 'python/'

def repo_root():
    """Return absolute path to the root of current Git repo.

    Searches in the path to current working directory for the first directory
    which contains a '.git' sub-directory which contains a file named 'HEAD'.
    """
    # files to recognize a Git repo directory
    GIT_FILES = ('.git/config', '.git/HEAD')
    # search based on current working directory
    cwd = os.getcwd()
    head, tail = os.path.split(cwd)
    # keep going up the hierarchy until 'tail' is the root Git repo folder
    while any((not os.path.isfile(os.path.join(head, tail, f)))
              for f in GIT_FILES):
        next_head, tail = os.path.split(head)
        if head == next_head:
            # this means the search has reached the root of the file system
            raise FileNotFoundError(f'No Git repo found in path {cwd}')
        head = next_head
    repo_path = os.path.join(head, tail)
    return os.path.abspath(repo_path)