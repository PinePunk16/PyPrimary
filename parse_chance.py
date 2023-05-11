import random

# Picks a random line from a file
# If the line is a percentage (ex. 50%) the file will pick a random line, in the lines before the next percentage or the end of file, with a 50% chance
# If there's at least one percentage the percentages have to line up to 100, otherwise the result is None
# To define a None value, make the percentage section it's in empty

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
        result_list = non_percentages[0]
    
    if result_list:
        return random.choice(result_list)
    else:
        return None