# PART 1
# INSTRUCTIONS

# EXAMPLE

# PART 2

# INSTRUCTIONS

# EXAMPLE

from .base_solver import solver

def get_highest_joltage(row:list[int]) -> int:
    # get index of highest value
    highest = max(row)
    high_index = row.index(highest)
    
    # if highest is last element, pick the second highest from the left side
    if high_index == len(row) - 1:
        second_digit = max(row[:high_index])
        return int(str(second_digit) + str(highest))
    
    # remove all elements to the left of highest
    to_eval = row[high_index+1:]
    second_digit = max(to_eval)
    
    #concat both values as strings
    return int(str(highest) + str(second_digit))


def get_highest_joltage_part_2(row : list[int], active_cells: int) -> int:
    if not row or active_cells <= 0:
        return 0

    remaining = active_cells
    selected_digits = []
    start = 0

    while remaining > 0:
        window_end = len(row) - remaining + 1
        best_digit = -1
        best_idx = start

        for idx in range(start, window_end):
            digit = row[idx]
            if digit > best_digit:
                best_digit = digit
                best_idx = idx
                if digit == 9:
                    break

        selected_digits.append(str(best_digit))
        start = best_idx + 1
        remaining -= 1

    return int("".join(selected_digits))
    

# solver class has a self.parser to read the file for the day.
class solve(solver):
    def part1(self):
        data = self.parser.file_to_matrix()
        res = 0
        for i, row in enumerate(data):
            int_row = [int(x) for x in row]
            highest = get_highest_joltage(int_row)
            res += highest
        return res
    
    def part2(self):
        data = self.parser.file_to_matrix()
        res = 0
        for i, row in enumerate(data):
            int_row = [int(x) for x in row]
            active_cells = 12  # Example fixed number of active cells
            joltage = get_highest_joltage_part_2(int_row, active_cells)
            res += joltage
        return res
            
    
    