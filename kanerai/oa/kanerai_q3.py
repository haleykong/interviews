def findTotalWeight(products):
    cost = 0
    while len(products) > 0:
        # Get index of minimum element
        m = min(products)
        idx = products.index(m)

        cost += products[idx]

        # Remove from right of index
        if idx <= len(products) - 2:
            del products[idx + 1]
        # Remove from index
        del products[idx]
        # Remove from left of index
        if idx >= 1:
            del products[idx - 1]
    return cost


###############################################################################
# CHATGPT SOLUTION #
###############################################################################
# Time Complexity: O(n log n)
import heapq


def findTotalWeightGPT(products):
    total_weight = 0
    n = len(products)

    # Create a min-heap of (weight, index)
    heap = [(weight, i) for i, weight in enumerate(products)]
    heapq.heapify(heap)

    # Set to keep track of removed indices
    removed = set()

    while heap:
        weight, i = heapq.heappop(heap)

        # Skip if this product has already been removed
        if i in removed:
            continue

        # Add the weight of the current product
        total_weight += weight

        # Mark this product and its adjacent products as removed
        removed.add(i)
        if i - 1 >= 0:
            removed.add(i - 1)
        if i + 1 < n:
            removed.add(i + 1)

        # Remove elements from heap if they are marked as removed
        while heap and heap[0][1] in removed:
            heapq.heappop(heap)

    return total_weight


# Example usage
products = [6, 4, 9, 10, 34, 56, 54]
print(findTotalWeightGPT(products))  # Output should be 68
