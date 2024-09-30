# Tesla Live Assessment
###############################################################################

# Question 1
"""
Write a function that returns the second highest unique number in a list
"""


# 1st approach
def second_highest_number(nums):
    unique_nums = set(nums)
    unique_nums.remove(max(unique_nums))
    return max(unique_nums)


# 2nd approach
def second_highest_number2(nums):
    # Remove duplicates by converting the list to a set, then back to a list
    unique_numbers = list(set(nums))

    if len(nums) < 2:
        return None

    # Sort the list in descending order
    unique_numbers.sort(reverse=True)

    return unique_numbers[1]


nums1 = [1, 2, 3, 4, 4, 4]
nums2 = [4, 1, 2, 3, 4, 5, 5]
print(second_highest_number(nums1))
print(second_highest_number2(nums2))

###############################################################################

# Question 2
"""
Return the differing keys between 2 dictionaries
"""


# 1st approach
def compare_dicts(dict1, dict2):
    keys = []

    for k in dict1.keys():
        if k not in dict2:
            keys.append(k)
    for k in dict2.keys():
        if k not in dict1:
            keys.append(k)
    return keys


# 2nd approach
def compare_dicts2(dict1, dict2):
    # Get the keys that are in dict1 but not in dict2, and vice versa
    keys_in_dict1_not_in_dict2 = dict1.keys() - dict2.keys()
    keys_in_dict2_not_in_dict1 = dict2.keys() - dict1.keys()

    # Combine the two sets of differing keys
    differing_keys = keys_in_dict1_not_in_dict2.union(
        keys_in_dict2_not_in_dict1
    )

    return differing_keys


dict1 = {"a": 1, "b": 2, "c": 3}
dict2 = {"a": 1, "b": 2, "d": 4}
print(compare_dicts(dict1, dict2))
print(compare_dicts2(dict1, dict2))

###############################################################################

# Question 3
"""
Return the differing keys between 2 dictionaries if the dictionaries can be
nested
"""


def differing_keys_recursive(dict1, dict2, parent_key=''):
    differing_keys = set()

    # Get all keys in both dictionaries
    all_keys = set(dict1.keys().union(set(dict2.keys())))

    for key in all_keys:
        full_key = f"{parent_key}.{key}" if parent_key else key

        # If the key exists in one dictionary but not the other
        if key not in dict1:
            differing_keys.add(full_key)
        elif key not in dict2:
            differing_keys.add(full_key)
        else:
            # If both values are dictionaries, recursively check their keys
            if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                differing_keys.update(
                    differing_keys_recursive(dict1[key], dict2[key], full_key)
                )
            # If the values are not equal, add the key
            elif dict1[key] != dict2[key]:
                differing_keys.add(full_key)

    return differing_keys


dict1 = {
    'a': 1,
    'b': {
        'x': 10,
        'y': 20,
        'z': 30
    },
    'c': 3
}

dict2 = {
    'b': {
        'x': 10,
        'y': 21,
        'w': 40
    },
    'c': 4,
    'd': 5
}

result = differing_keys_recursive(dict1, dict2)
print(result)
