# PART 1
# INSTRUCTIONS

# EXAMPLE

# PART 2

# INSTRUCTIONS

# EXAMPLE

from .base_solver import solver
import math
import pandas as pd

# solver class has a self.parser to read the file for the day.
class solve(solver):
    def part1(self):
        data = self.parser.file_to_dataframe("pro", sep=' ')
        ops = data.iloc[-1].tolist()
        data = data.iloc[:-1]  # Remove ops row
        
        # Convert to numeric
        data = data.apply(pd.to_numeric)

        # Calculate sum and product for each column
        col_sums = data.sum()
        col_prods = data.prod()

        # Use ops to select sum or product for each column
        result = col_sums.where(pd.Series(ops) == '+', col_prods)

        return result.sum()
    
    def part2(self):
        data = self.parser.file_to_matrix_keep_spaces()
        data = list(zip(*data))[::-1]
        data = [list(row) for row in data]
        ops = [row.pop() for row in data if row[-1] != ' ']
        data = [''.join(row).strip() for row in data]
        data.append('') # to handle last operation
        
        res = []
        current_numbers = []
        for val in data:
            if val == '':
                op = ops[len(res)]
                res.append(sum(current_numbers) if op == '+' else math.prod(current_numbers))
                current_numbers = []
            else:
                current_numbers.append(int(val))
                
        return sum(res)