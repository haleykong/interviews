# IBM 2023-2024 Backend Developer Assessment

def minParen(s: str):
    """Get minimum number of parens to complete string.

    Parameters
    ----------
    s : str
        Input string (only made of parentheses)

    Returns
    -------
    num_parens: int
        Minimum number of parentheses to close out string.

    """
    stack = []

    for x in s:
        if len(stack) > 0 and x == ")" and stack[-1] == "(":
            stack.pop()
        else:
            stack.append(x)

    num_parens = len(stack)
    return num_parens


TEST_CASES = ["()()", "(())", "))((", ")(()())((("]
n = len(TEST_CASES)

print("=" * 79)
print(f"Running {len(TEST_CASES)} tests...")
print()

for ii, test in enumerate(TEST_CASES):
    print("-" * 79)
    print(f"TEST #{ii + 1} of {n}:")
    print(f"\t{test}")
    print(f"\tResult: {minParen(test)}")

###############################################################################
# IBM General Software Engineering Assessment
# Question 1)


def longestEvenWord(sentence):
    """Find and return the first word in the sentence that has a length that is
    both an even number and has the greatest length of all even-length words in
    the sentence.

    Parameters
    ----------
    sentence : string
        A sentence string consisting of words separated by spaces where each
        word is a substring that consists of English alphabetic letters only

    Returns
    -------
    word : string
        First word that has the greatest length of all even-length words. If no
        even words, returns '00'

    """
    # Get length of words
    words = sentence.split()
    char_count = [len(word) for word in words if (len(word) % 2 == 0)]

    # No even length words
    if len(char_count) == 0:
        return "00"

    max_count = max(char_count)

    # Find first word with the longest even length
    for word in words:
        if len(word) == max_count:
            return word


TEST_CASES = ["This is a pleasant day", "Hello World", "My name is Haley"]
n = len(TEST_CASES)

print("=" * 79)
print(f"Running {len(TEST_CASES)} tests...")
print()

for ii, test in enumerate(TEST_CASES):
    print("-" * 79)
    print(f"TEST #{ii + 1} of {n}:")
    print(f"\t{test}")
    print(f"\tResult: {longestEvenWord(test)}")

###############################################################################
# Question 2)


def findOptimalResources(arr, k):
    """Identify a subarray that optimally utilizes these resources. The
    subarray must have a specific length k, and the elements in the subarray
    must be unique, representing distinct resource allocations.

    Parameters
    ----------
    arr : List
        Array of size n that represents a set of available resources
    k : int
        Subarray length

    Returns
    -------
    max_sum : int
        Maximum resource allocation. Returns -1 if no valid subarray

    """

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

    # # Approach 2) Using dictionary to track unique values
    # n = len(arr)

    # max_sum = -1
    # curr_sum = 0

    # n_elem = len((set(arr[:k])))  # Number of unique elements in the 1st window

    # # If first window has k unique elements, assign the sum
    # if n_elem == k:
    #     curr_sum = sum(arr[:k])

    # # Create dictionary to track the count of each element in the window
    # counts = {}
    # for x in arr[:k]:
    #     counts[x] = counts.get(x, 0) + 1

    # # Start sliding the window
    # for ii in range(n - k):
    #     xold = arr[ii]
    #     xnew = arr[ii + k]

    #     # Update the sum for the sliding window
    #     curr_sum += xnew
    #     curr_sum -= xold

    #     # Update the counts for outgoing element (xold)
    #     counts[xold] -= 1
    #     # If count of the outgoing element becomes 0, it is no longer in the
    #     # window
    #     if counts[xold] == 0:
    #         n_elem -= 1

    #     # Update the counts for the incoming element (xnew)
    #     if xnew in counts:
    #         # If it's being added back after its count reached 0, it is a
    #         # unique element
    #         if counts[xnew] == 0:
    #             n_elem += 1
    #         counts[xnew] += 1
    #     else:
    #         # Completely new element
    #         counts[xnew] = 1
    #         n_elem += 1

    #     # If the window has exactly k unique elements, add the sum to the list
    #     if n_elem == k and max_sum < curr_sum:
    #         max_sum = curr_sum

    # # Return the maximum sum
    # return max_sum


TEST_CASES = [[1, 2, 3, 7, 3, 5],  # Answer: 15
              [1, 2, 7, 7, 4, 3, 6],  # Answer: 14
              [1, 1, 1, 1, 2, 2]  # Answer: -1
              ]

n = len(TEST_CASES)

print("=" * 79)
print(f"Running {len(TEST_CASES)} tests...")
print()

for ii, test in enumerate(TEST_CASES):
    print("-" * 79)
    print(f"TEST #{ii + 1} of {n}:")
    print(f"\t{test}")
    print(f"\tResult: {findOptimalResources(test, 3)}")
