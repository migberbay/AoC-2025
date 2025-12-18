# PART 1
# INSTRUCTIONS

# EXAMPLE

# PART 2

# INSTRUCTIONS

# EXAMPLE

from .base_solver import solver
from tqdm import tqdm

# solver class has a self.parser to read the file for the day.
class solve(solver):
    def part1(self):
        data = self.parser.file_to_matrix()
        x = data[0].index('S')
        ray_coords = set([x])
        splits = 0
        
        for data_row in data[2::2]:
            new_rays = set()
            split_positions = []
            for ray_pos in ray_coords:
                if data_row[ray_pos] == '^':
                    split_positions.append(ray_pos)
                    splits += 1
                    new_rays.update([ray_pos - 1, ray_pos + 1])
                    
            ray_coords.difference_update(split_positions)    
            ray_coords.update(new_rays)

        return splits

    def part2(self):
        data = self.parser.file_to_matrix()
        x = data[0].index('S')
        ray_coords = {x: 1}
        
        for data_row in data[2::2]:
            new_rays = dict()
            for ray_pos, ray_count in ray_coords.items():
                if data_row[ray_pos] == '^':
                    new_rays[ray_pos - 1] = new_rays.get(ray_pos - 1, 0) + ray_count
                    new_rays[ray_pos + 1] = new_rays.get(ray_pos + 1, 0) + ray_count
                else: 
                    new_rays[ray_pos] = new_rays.get(ray_pos, 0) + ray_count

            ray_coords = new_rays

        return sum(ray_coords.values())