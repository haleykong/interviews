# ****************************************************************************
# Author: Haley Kong
# Date Created: Sun Sep  8 16:31:32 2024
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
import textwrap
import numpy as np
import time
from matplotlib import pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm

# 3rd Party package imports

# Local imports

# -----------------------------------------------------------------------------
# CONSTANTS

# -----------------------------------------------------------------------------
# CLASSES

# -----------------------------------------------------------------------------
# FUNCTIONS

# -----------------------------------------------------------------------------


def config_ax(ax, minor_color="r", ycolor="", xcolor="", width=60):
    """Standardize Ky-anh's favourite plot settings.

    Parameters
    ----------
    ax : matplotlib axes object
    Returns
    -------
    modified ax object
    """
    ax.grid(which="major", color="k", linestyle="-", alpha=0.25)
    ax.grid(which="minor", color=minor_color, linestyle=":", alpha=0.25)
    ax.minorticks_on()
    ax.tick_params(
        axis="x", which="both", bottom=True, top=False, labelbottom=True
    )
    ax.xaxis.set_tick_params(labelbottom=True)
    ax.yaxis.set_tick_params(labelleft=True)
    if len(ycolor) > 0:
        ax.yaxis.label.set_color(ycolor)
        ax.tick_params(axis="y", colors=ycolor)
    if len(xcolor) > 0:
        ax.yaxis.label.set_color(xcolor)
        ax.tick_params(axis="x", colors=xcolor)

    # Check if there is a label
    if ax.get_legend_handles_labels()[1]:
        ax.legend(loc="upper right")
        uniquify_leg(ax)
    # Wrap title if necessary
    cur_title = ax.get_title()
    wrap_title = "\n".join(textwrap.wrap(cur_title, width))
    ax.set_title(wrap_title)
    return ax


def uniquify_leg(ax):
    """Uniquify legend.

    Parameters
    ----------
    ax : matplotlib ax object

    Returns
    -------
    leg: legend object
    """
    # Uniquify legend
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    leg = ax.legend(by_label.values(), by_label.keys(), fontsize=8)
    return leg


def findOptimalResources_using_set(arr, k):
    # Approach 1) Using set to track unique values
    n = len(arr)
    if n < k:
        return -1  # Not enough elements for a subarray of length k

    max_sum = -1
    current_sum = 0
    window_set = set()

    left = 0  # Left pointer for the sliding window

    for right in range(n):
        while arr[right] in window_set:
            # Remove elements from the left to maintain unique elements in the
            # window
            window_set.remove(arr[left])
            current_sum -= arr[left]
            left += 1

        # Add the current element to the window
        window_set.add(arr[right])
        current_sum += arr[right]

        # Check if we have a valid window of size k
        if right - left + 1 == k:
            max_sum = max(max_sum, current_sum)
            # Remove the leftmost element to maintain the sliding window size
            # of k
            window_set.remove(arr[left])
            current_sum -= arr[left]
            left += 1

    return max_sum
           


def findOptimalResources(arr, k):
    n = len(arr)
    if k > n:
        return -1
    # Logistics grab length
    n = len(arr)
   
    # initialize a rolling sum list (onlys tore valid sms)
    sums = []
   
    # initilize # of elements in first window : will track # of unique elements
    # as we ingest new values
    nelem = len(set(arr[:k]))
    # initialize initial sum
    s = sum(arr[:k])
   
    # if number of element is k (unique): append sum to list of valids sums
    if nelem == k:
        maxsum = s
    else:
        maxsum = -1
       
    # Track number of elements withing current window in a dictionary
    # key = element, value = number of counts found
    cnt = {}
    for x in arr[:k]:
        if x in cnt:
            cnt[x] += 1
        else:
            cnt[x] = 1
   
    # Add 1 new element at a time:
    for ii in range(n-k):
        xold = arr[ii]
        xnew = arr[ii + k]
        s += (xnew - xold)
        cnt[xold] -= 1
        if cnt[xold] == 0:
            nelem -= 1
        if xnew in cnt:
            if cnt[xnew] == 0:
                nelem += 1
            cnt[xnew] += 1
        else:
            cnt[xnew] = 1
            nelem += 1

        if nelem == k:
            maxsum = max([s, maxsum])

    return maxsum

# Create n, k values to sweep over
nsize = np.arange(1e6, 1e7, 1e6, dtype=int)
ksize = np.arange(1e4, 1e5, 1e4, dtype=int)

# Create function list to sweep over:
funcs = [findOptimalResources, findOptimalResources_using_set]
step = ksize[1] - ksize[0]

# Initialize colorbar settings
cmap = plt.get_cmap("jet", len(ksize))  # Color map choice
norm = mpl.colors.Normalize(vmin=-step/2.0, vmax=max(ksize) + step/2.0)
# Color bar scaling
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)

# Store run times for given function, n, k value in 2-d numpy array
runtimes = np.zeros((len(nsize), len(ksize), 2))

# Sweep over all combinations of n, k value, and function to run.
for ii, n in enumerate(nsize):
    print('-' * 79)
    print(f"Running n={n}, trial {ii+1} of {len(nsize)}")
    t = list(np.random.randint(0, 1e9, size=n, dtype=int))
    for kk, k in enumerate(ksize):
        print(f"  - Running k={k}")
        for ll, func in enumerate(funcs):
            print(f"    - Running func={func.__name__}")
            tic = time.time()
            func(t, k)
            toc = time.time()
            runtimes[ii, kk, ll] = toc - tic

# Create plot here:
fh, ax = plt.subplots()
STYLES = ['-o', '--'] # Different plot style for different functions
for kk, k in enumerate(ksize):
    for ll, func in enumerate(funcs):
        # Plot runtimes for given k, function against n value
        # (nsize).
        ax.plot(nsize / 1e6, runtimes[:, kk, ll],
                STYLES[ll],
                label=func.__name__,
                c=cmap(kk))
   
ax.set_ylabel('Run time [s]')
ax.set_xlabel('n: input array size [Millions]')
ax.legend()
ax.grid()
# Label colorbar
cbar = fh.colorbar(sm, ax=ax)
cbar.ax.set_title('k: window')

uniquify_leg(ax)
config_ax(ax)
