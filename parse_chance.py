# parse_chance.py
# For parsing of pool files.

import random



"""
Picks a random line from a file. If the line is a percentage (e.g. "50%"), the function will pick a random line 
from the lines before the next percentage (or the end of the file) with the specified probability. 

There must be at least one percentage, and the percentages must add up to 100, otherwise the function will return None. 
To define a None value, make the percentage section it's in empty.

To select a random integer in a range, use the syntax "random[a, b)" for an exclusive range or "random[a, b]" for an inclusive range.

Example 1:

----------------
50%
    4
    2
25%
25%
    random[0, 10)
-----------------

In this example, the function will generate either 4 or 2 with a 50% chance. 
With a 25% chance, it will return None. 
With another 25% chance, it will generate a random value between 0 (inclusive) and 10 (inclusive).

Example 2:
----------------
99.99%
    Martha
    John
    Alan
    Jake
    Alex
0.01%
    Ashlathon the conquerer of worlds
-----------------

In this example, the function will generate with a high change a name between "Martha", "John", "Alan", "Jake" and "Alex".
With a very low chance, the name will be "Ashlathon the conquerer of worlds".
"""

def parse_chance(file_path: str) -> str:
    lines: list[str] = []
    
    try:
        with open(file_path, "r") as file:
            for line in file:
                lines.append(line.strip())
    except Exception as exception:
        print(f"ERROR: {exception}")
    
    percentages: list[float] = []
    non_percentages: list[list[str]] = [[]]
    percentages_index: int = 0
    
    for line in lines:
        if line.endswith("%"):
            percentages_index += 1
            non_percentages.append([])
            
            percentages.append(float(line[:-1]))
        else:
            non_percentages[percentages_index].append(line)
    non_percentages.pop(0)
    
    result_list: list[str] = None
    
    if not non_percentages:
        return None
    
    if(percentages):
        total_percentage = sum(percentages)
        if(total_percentage != 100):
            return None
        
        random_number = random.uniform(0, 100)
        cumulative_percentage = 0
        for index, percentage in enumerate(percentages):
            cumulative_percentage += percentage
            if random_number <= (cumulative_percentage / total_percentage * 100) or index == len(percentages) - 1:
                result_list = non_percentages[index]
                break
    else:
        return None
    
    if result_list:
        result: str = random.choice(result_list)
        
        if (result.startswith("random(") or result.startswith("random[")) and (result.endswith(")") or result.endswith("]")):
            values: list[float] = result[7:-1].split(",")
            min_value: int = int(values[0])
            max_value: int = int(values[1])

            left_inclusive: bool = result[6] == "["
            right_inclusive: bool  = result[-2] == "]"
            
            return str(random.randint(min_value if left_inclusive else min_value + 1, max_value if right_inclusive else max_value - 1))
        else:
            return result
    else:
        return None