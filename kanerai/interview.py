import json

input_str = """
   ID        NAME           ORAT CRAT AMT  Cover
470474AQ0 JTWN 2014-4A A1AR AAA  AAA  7.65 99.535
59802UAX7 MIDO 2014-3A A3A2 AAA  AAA   1   97.631
449255AC2 ICG 2017-2A A1    AAA  AAA   1   98.261
14315LAA2 CGMS 2014-3RA A1A AAA  AAA   1   97.92
66860PAA2 WOODS 2018-17A A  AAA  AAA   1    DNT"""

desired_output = {
    "columns": ["ID", "NAME", "ORAT", "CRAT", "AMT", "Cover"],
    "data": [
        ["470474AQ0", "JTWN 2014-4A A1AR", "AAA", "AAA", "7.65", "99.535"],
        ["59802UAX7", "MIDO 2014-3A A3A2", "AAA", "AAA", "1", "97.631"],
        ["449255AC2", "ICG 2017-2A A1", "AAA", "AAA", "1", "98.261"],
        ["14315LAA2", "CGMS 2014-3RA A1A", "AAA", "AAA", "1", "97.92"],
        ["66860PAA2", "WOODS 2018-17A A", "AAA", "AAA", "1", "DNT"]
    ]
}

# Split the string into lines
lines = input_str.strip().split("\n")

# Extract the header
columns = lines[0].split()

# Extract the data rows
data = []
for line in lines[1:]:
    row = line.split()
    id_row, *name_parts, orat, crat, amt, cover = row
    name = " ".join(name_parts)
    data.append([id_row, name, orat, crat, amt, cover])

# Create the dictionary
result = {
    "columns": columns,
    "data": data
}


# Custom print function to match the desired format
def pretty_print_dict(d):
    print("{")
    print(f'  "columns": {json.dumps(d["columns"])},')
    print('  "data": [')
    for row in d["data"]:
        print(f'    {json.dumps(row)},')
    print('  ]')
    print("}")


# Pretty-print the dictionary
pretty_print_dict(result)
