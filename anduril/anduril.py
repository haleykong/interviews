# Given an array of strings “strs”, group any anagrams together. You can return the answer in any order.

# - An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.

# Example:
# ```
# strs = [“eat”, “tea”, “bat”, “ate”]
# out = [ [“eat”, “tea”, “ate”], [“bat”] ]

# strs = [“”]
# out = [ [“”] ]

# strs = [“a”]
# out = [ [“a”] ]
# ```

def group_anagrams(strs):
    
    d = {}
    for s in strs:
        sorted_s = ("").join(sorted(s))
        if sorted_s in d:
            d[sorted_s].append(s)
        else:
            d[sorted_s] = [s]
        
    # Create result array from values
    res = []
    for v in d.values():
        res.append(v)
    
    return res
    
print(group_anagrams(["eat", "tea", "bat", "ate"]))
