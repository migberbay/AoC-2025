# PART 1
# INSTRUCTIONS

# EXAMPLE

# PART 2

# INSTRUCTIONS

# EXAMPLE

from pprint import pprint
from .base_solver import solver
from .utils import shape
import math

# solver class has a self.parser to read the file for the day.
class solve(solver):
    def part1(self):
        data = self.parser.file_from_day_12()
        shape_dict = data[0]
        trees = data[1]
        shapes = {k: shape(v) for k, v in shape_dict.items()}
            
        res = 0
        for t in trees:
            tot_area_filled = 0
            available_space = math.prod(t[0])
            for k, num_presents in t[1].items():
                s = shapes[k]
                tot_area_p = s.filled_area() * num_presents
                tot_area_filled += tot_area_p
            
            if(tot_area_filled <= available_space):
                res += 1

        return res