# PART 1
# INSTRUCTIONS

# EXAMPLE

# PART 2

# INSTRUCTIONS

# EXAMPLE

from .base_solver import solver
from .utils import matrix_navigator


# solver class has a self.parser to read the file for the day.
class solve(solver):
    def part1(self):
        data = self.parser.file_to_matrix()
        navigator = matrix_navigator(data, start_pos=(0, 0))
        res = 0
        for i in range(navigator.rows):
            for j in range(navigator.cols):
                navigator.move_to(i, j)
                neighbors = navigator.get_neighbors(navigator.position)
                # count the number of '@' in the neighbors
                if sum(1 for n in neighbors if n == '@') < 4 and data[i][j] == '@':
                    res += 1
        return res
    
    def part2(self):
        data = self.parser.file_to_matrix()
        navigator = matrix_navigator(data, start_pos=(0, 0))
        res = 0
        while True:
            rolls_extracted_positions = []
            for i in range(navigator.rows):
                for j in range(navigator.cols):
                    navigator.move_to(i, j)
                    neighbors = navigator.get_neighbors(navigator.position)
                    # count the number of '@' in the neighbors
                    if sum(1 for n in neighbors if n == '@') < 4 and data[i][j] == '@':
                        res += 1
                        rolls_extracted_positions.append((i, j))
            
            if not rolls_extracted_positions:
                break
            
            for pos in rolls_extracted_positions:
                navigator.insert('.', pos)
            
                        
        return res
