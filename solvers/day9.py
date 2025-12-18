# PART 1
# INSTRUCTIONS

# EXAMPLE

# PART 2

# INSTRUCTIONS

# EXAMPLE

from tqdm import tqdm
from .base_solver import solver
from shapely.geometry import Point, Polygon

def rectangle_area(p1, p2) -> int:
    return (abs((p2[0] - p1[0])) + 1) * (abs(p2[1] - p1[1]) + 1)

def points_to_lines(points):
    horizontal_lines = []
    vertical_lines = []
    
    for i in range(len(points)):
        p1 = points[i]
        p2 = points[(i + 1) % len(points)]
        
        if p1[0] == p2[0]:
            vertical_lines.append((min(p1[1], p2[1]), max(p1[1], p2[1]), p1[0]))
            
        elif p1[1] == p2[1]:
            horizontal_lines.append((min(p1[0], p2[0]), max(p1[0], p2[0]), p1[1]))
    
    return horizontal_lines, vertical_lines

def points_to_polygon(points):
    shapely_points = [Point(p) for p in points]
    polygon = Polygon(shapely_points)
    return shapely_points, polygon

def check_intersections(p1, p2, horizontal_lines, vertical_lines):
    rect_x_min = min(p1[0], p2[0])
    rect_x_max = max(p1[0], p2[0])
    rect_y_min = min(p1[1], p2[1])
    rect_y_max = max(p1[1], p2[1])
    
    # Check vertical lines (sorted by x coordinate)
    # We only care about vertical lines strictly between rect_x_min and rect_x_max
    for v_line in vertical_lines:
        y_min, y_max, x_pos = v_line
        
        # Skip lines before the rectangle
        if x_pos <= rect_x_min:
            continue
        
        # Stop checking once we've passed the rectangle
        if x_pos >= rect_x_max:
            break
        
        # This vertical line is in the interior (rect_x_min < x_pos < rect_x_max)
        # Check if it crosses through the rectangle's height
        if y_max > rect_y_min and y_min < rect_y_max:
            return True
    
    # Check horizontal lines (sorted by y coordinate)
    # We only care about horizontal lines strictly between rect_y_min and rect_y_max
    for h_line in horizontal_lines:
        x_min, x_max, y_pos = h_line
        
        # Skip lines before the rectangle
        if y_pos <= rect_y_min:
            continue
        
        # Stop checking once we've passed the rectangle
        if y_pos >= rect_y_max:
            break
        
        # This horizontal line is in the interior (rect_y_min < y_pos < rect_y_max)
        # Check if it crosses through the rectangle's width
        if x_max > rect_x_min and x_min < rect_x_max:
            return True
    
    return False

# solver class has a self.parser to read the file for the day.
class solve(solver):
    def part1(self):
        data = self.parser.file_to_matrix_sep(',', int)
        max_area = 0
        for p1 in data:
            for p2 in data:
                if p1 != p2:
                    area = rectangle_area(p1, p2)
                    max_area = max(max_area, area)
        return max_area
    
    def part2(self):
        data = self.parser.file_to_matrix_sep(',', int)
        horizontal_lines, vertical_lines = points_to_lines(data)
        horizontal_lines.sort(key=lambda x: x[2])
        vertical_lines.sort(key=lambda x: x[2])
        
        shapely_points, polygon = points_to_polygon(data)
        
        max_area = 0
        res_points = None
        for i in tqdm(range(len(data))):
            for j in range(len(data)):
                p1, p2 = data[i], data[j]
                p1s, p2s = shapely_points[i], shapely_points[j]
                
                if p1 != p2:
                    # Check all 4 corners of the rectangle
                    p3 = [p1[0], p2[1]]
                    p4 = [p2[0], p1[1]]
                    p3s = Point(p3)
                    p4s = Point(p4)
                    
                    all_inside = all([
                        polygon.contains(pt) or polygon.intersects(pt)
                        for pt in [p1s, p2s, p3s, p4s]
                    ])
                    
                    if all_inside:
                        if(not check_intersections(p1, p2, horizontal_lines, vertical_lines)):
                            area = rectangle_area(p1, p2)
                            if area > max_area:
                                max_area = area
                                res_points = (p1, p2)
                        
        return max_area, res_points