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
