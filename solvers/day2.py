# PART 1
# INSTRUCTIONS
# get the ranges and look for numbers which have repeating digits in the first and second half.

# EXAMPLE
# 11-22 has two invalid IDs, 11 and 22.
# 95-115 has one invalid ID, 99.
# 998-1012 has one invalid ID, 1010.

# PART 2

# INSTRUCTIONS

# EXAMPLE

from .base_solver import solver
from .utils import split_into_parts

class solve(solver):
    def part1(self):
        data = self.parser.file_string_to_list()
        res = 0
        for item in data:
            if item is None:
                continue

            start, end = item.split('-')
            start, end = int(start), int(end)            
            
            for i in range(start, end + 1):
                str_i = str(i)
                mid = len(str_i) // 2
                first_half = str_i[:mid]
                second_half = str_i[mid:]
                
                if first_half == second_half:
                    res += int(i)
             
        return res
    
    def part2(self):
        data = self.parser.file_string_to_list()
        res = 0
        
        for item in data:
            if item is None:
                continue

            start, end = item.split('-')
            start, end = int(start), int(end)
                        
            for i in range(start, end + 1):
                str_i = str(i)
                for j in range((len(str_i)//2), 0, -1):
                    rep = set(split_into_parts(str_i, j))
                    if len(rep) == 1:
                        res += int(i)
                        break
                    
        return res