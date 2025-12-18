from collections import defaultdict

class counter_with_wraparound:
    def __init__(self, start: int, end: int, initial_value: int) -> None:
        self.start = start
        self.end = end
        self.value = initial_value

    def change(self, value: int) -> int:
        #module of value based on max range
        range_size = self.end - self.start + 1
        offset = (self.value - self.start + value) % range_size
        self.value = self.start + offset
        return self.value
    
class dial_counter(counter_with_wraparound):
    def __init__(self, start: int, end: int, initial_value: int, watch_points: list[int]) -> None:
        super().__init__(start, end, initial_value)
        
        self.range_size = self.end - self.start + 1
        self.watch_points = {wp for wp in watch_points if start <= wp <= end}
        self.pass_counts = {wp: 0 for wp in self.watch_points}

    def change(self, value: int) -> tuple[int, dict[int, int]]:
        previous = self.value
        new_value = super().change(value)
        passes = self._count_passes(previous, value)
        for wp, count in passes.items():
            self.pass_counts[wp] += count
        return new_value, passes

    def _count_passes(self, previous: int, delta: int) -> dict[int, int]:
        if delta == 0:
            return {}
        passes = {}
        steps = abs(delta)
        start_offset = (previous - self.start) % self.range_size
        direction = 1 if delta > 0 else -1

        for wp in self.watch_points:
            target_offset = (wp - self.start) % self.range_size
            if direction > 0:
                distance = (target_offset - start_offset) % self.range_size or self.range_size
            else:
                distance = (start_offset - target_offset) % self.range_size or self.range_size
            if distance > steps:
                continue
            hits = 1 + (steps - distance) // self.range_size
            passes[wp] = hits
        return passes

class matrix_navigator:
    def __init__( self, matrix: list[list], start_pos: tuple[int, int] = (0, 0), out_of_bounds_value = None) -> None:
        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0])
        self.position = start_pos
        self.out_of_bounds_value = out_of_bounds_value

    def _in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.rows and 0 <= col < self.cols

    def move(self, delta_row: int, delta_col: int) -> tuple[int, int] | object:
        new_row = self.position[0] + delta_row
        new_col = self.position[1] + delta_col
        if not self._in_bounds(new_row, new_col):
            return self.out_of_bounds_value
        self.position = (new_row, new_col)
        return self.position
    
    def move_to(self, row: int, col: int) -> tuple[int, int] | object:
        if not self._in_bounds(row, col):
            return self.out_of_bounds_value
        self.position = (row, col)
        return self.position
    
    def insert(self, value, pos) -> None:
        row, col = pos
        if self._in_bounds(row, col):
            self.matrix[row][col] = value
    
    def get_neighbors(self, pos: tuple[int, int]) -> list:
        deltas = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),          (0, 1),
                  (1, -1),  (1, 0), (1, 1)]
        neighbors = []
        for dr, dc in deltas:
            r = pos[0] + dr
            c = pos[1] + dc
            if self._in_bounds(r, c):
                neighbors.append(self.matrix[r][c])
            else:
                neighbors.append(self.out_of_bounds_value)
        return neighbors

class shape():
    def __init__(self, grid: list[list[int]]) -> None:
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0

    def __str__(self):
        return '\n' + '\n'.join(''.join(str(cell) for cell in row) for row in self.grid) + '\n'

    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        if not isinstance(other, shape):
            return False
        return self.grid == other.grid
    
    def filled_area(self) -> int:
        return sum(1 for row in self.grid for cell in row if cell == '#')
    
    def rotate_clockwise(self):
        rotated = [[self.grid[self.rows - 1 - c][r] for c in range(self.rows)] for r in range(self.cols)]
        return shape(rotated)
    
    def flip_horizontal(self):
        flipped = [list(reversed(row)) for row in self.grid]
        return shape(flipped)
    
    def flip_vertical(self):
        flipped = list(reversed(self.grid))
        return shape(flipped)
    
    def get_all_shape_variations(self):
        base_shapes = list()
        
        shape_obj = self.grid
        shape_obj_hf = self.flip_horizontal()
        shape_obj_vf = self.flip_vertical()
        
        base_shapes =([shape_obj, shape_obj_hf, shape_obj_vf])

        all_shape_variations = list()
        all_shape_variations.extend(base_shapes)
        
        for s in base_shapes:
            for i in range(3):
                s = s.rotate_clockwise()
                if(s not in all_shape_variations):
                    all_shape_variations.append(s)
                    
        return all_shape_variations
        
    
        
    
    
def split_into_parts(s: str, part_size: int) -> list[str]:
    return [s[i:i + part_size] for i in range(0, len(s), part_size)]

if __name__ == "__main__":
    # testing the utilities:
    a = '12121212'
    print(set(split_into_parts(a, 2)))

        