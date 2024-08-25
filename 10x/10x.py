## Input is located in "/home/coderpad/data/spreadsheet.txt"
from itertools

FILENAME = '/home/coderpad/data/spreadsheet.txt'

# def calculate_checksum(filename):
#     checksum = 0
#     with open(filename, 'r') as file:
#         for line in file:
#             # Parse the line into list of ints
#             int_list = list(map(int, line.split()))
#             # Calculate checksum
#             checksum += (max(int_list) - min(int_list))

#     return checksum

def open_file(filename):
    int_list = []
    with open(filename, 'r') as file:
        for line in file:
            # Parse the line into list of ints
            int_list.append(list(map(int, line.split())))
    return int_list

def calculate_checksum(filename):
    # Open file
    checksum = 0
    int_list = open_file(filename)
    # Calculate checksum
    for l in int_list:
        checksum += max(l) - min(l)
    return checksum

def div_result(l):
    for i in range(len(l)):
        for j in range(len(l)):
            if i == j:
                continue
            if l[i] % l[j] == 0:
                return l[i] / l[j]
            elif l[j] % l[i] == 0:
                return l[j] / l[i]
    return 0

def divisor(filename):
    result = 0
    int_list = open_file(filename)
    # Calculate checksum
    for l in int_list: 
        result += div_result(l)
    return int(result)

print(divisor(FILENAME))  
# divisor(FILENAME) 
