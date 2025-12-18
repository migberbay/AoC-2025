# PART 1
# INSTRUCTIONS

# EXAMPLE

# PART 2

# INSTRUCTIONS

# EXAMPLE

from collections import deque
from z3 import *

from tqdm import tqdm
from .base_solver import solver

def parse_button(button_str, num_lights, as_positions=False):
    button_str = button_str[1:-1]  # remove parentheses
    button_positions = button_str.split(',')
    
    if as_positions:
        # Return list of position indices for part 2
        return [int(pos.strip()) for pos in button_positions]
    
    # Return bitmask for part 1
    # Position N in the string (left-to-right) corresponds to bit (num_lights - 1 - N)
    bitmask = 0
    for pos in button_positions:
        pos_int = int(pos.strip())
        bitmask |= (1 << (num_lights - 1 - pos_int))
    return bitmask

def indicators_to_bit(indicators):
    # convert list of '.' and '#' to integer bit representation
    # leftmost character (position 0) = highest bit
    bit_representation = 0
    for i, indicator in enumerate(indicators):
        if indicator == '#':
            bit_representation |= (1 << (len(indicators) - 1 - i))
    return bit_representation

def parse_row(row, as_positions=False):
    lights = row[0][1:-1]
    buttons = row[1:-1]
    joltages = row[-1]
    
    num_lights = len(lights)
    
    lights = indicators_to_bit(list(lights))
    buttons = [parse_button(b, num_lights, as_positions) for b in buttons]
    joltages = [int(a) for a in joltages[1:-1].split(',')]
    
    return num_lights, lights, buttons, joltages

def pseudoBFS(target, buttons, num_lights):
    # Start with all lights OFF (0)
    initial_state = 0
    
    state = (initial_state, 0)  # (current light state, button press count)
    q = deque([state])
    visited = {initial_state}

    while q:
        current_lights, presses = q.popleft()
        
        # Check if we reached the target configuration
        if current_lights == target:
            return presses

        # Explore all button presses
        for button in buttons:
            new_lights = current_lights ^ button  # XOR to toggle bits
            
            if new_lights not in visited:
                visited.add(new_lights)
                q.append((new_lights, presses + 1))

    return -1  # If no solution is found

def Z3solver(target, buttons):
    button_presses = [Int(f'button_{i}') for i in range(len(buttons))]
    
    # Create the optimizer (finds minimum solutions)
    opt = Optimize()
    
    # Constraint: each button must be pressed 0 or more times
    for press in button_presses:
        opt.add(press >= 0)
    
    # Constraint: for each joltage position, the sum of all button effects
    # must equal the target joltage value
    for pos in range(len(target)):
        # Sum up the effect of all buttons on this position
        position_sum = Sum([
            button_presses[i] * (1 if pos in buttons[i] else 0)
            for i in range(len(buttons))
        ])
        opt.add(position_sum == target[pos])
    
    # Minimize the total number of button presses
    total_presses = Sum(button_presses)
    opt.minimize(total_presses)
    
    # Solve
    if opt.check() == sat:
        model = opt.model()
        result = sum(model[press].as_long() for press in button_presses)
        return result
    else:
        return -1  # No solution found

# solver class has a self.parser to read the file for the day.
class solve(solver):
    def part1(self):
        data = self.parser.file_to_matrix_sep(' ')
        results = []
        
        for row in tqdm(data):
            size, target, buttons, _ = parse_row(row)
            min_presses = pseudoBFS(target, buttons, size)
            results.append(min_presses)
        
        return sum(results)
    
    def part2(self):
        data = self.parser.file_to_matrix_sep(' ')
        results = []
        for row in tqdm(data):
            _, _, buttons, joltages = parse_row(row, as_positions=True)
            min_presses = Z3solver(joltages, buttons)
            results.append(min_presses)
        
        return sum(results)
