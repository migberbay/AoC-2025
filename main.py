from solvers import day1, day2, day3, day4, day5, day6, day7, day8, day9, day10, day11, day12
from time import time
from pprint import pprint
import sys

solvers = [day1, day2, day3, day4, day5, day6, day7, day8, day9, day10, day11, day12]

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: python main.py [day] [parts]")
        sys.exit(1)
    
    if len(sys.argv) > 1:
        try:
            day_to_run = int(sys.argv[1])
            if day_to_run < 1 or day_to_run > 12:
                print("Error: Day must be between 1 and 12")
                sys.exit(1)
        except ValueError:
            print("Error: Day must be a number between 1 and 12")
            sys.exit(1)
            
    parts_to_run = [1, 2]  # Default: run both parts
    if len(sys.argv) > 2:
        parts_arg = sys.argv[2]
        print(f"Requested parts: {parts_arg}")
        if parts_arg == "1":
            parts_to_run = [1]
        elif parts_arg == "2":
            parts_to_run = [2]
        elif parts_arg in ["1,2", "2,1"]:
            parts_to_run = [1, 2]
        else:
            print("Error: Parts must be 1, 2, or 1,2")
            sys.exit(1)        
    
    print(f"#### Solving day {day_to_run} ####")
    solve = solvers[day_to_run - 1].solve(day_to_run)
    s = [solve.part1, solve.part2]
    
    skip_parts = [i for i in [1, 2] if i not in parts_to_run]
    
    for i in range(1, 3):
        if i in skip_parts:
            print(f" \n---- Skipping part {i} -----")
            continue
        
        print(f" \n---- Starting part {i} -----")
        time_start = time()
        pprint(s[i - 1]())
        print(f"Part {i} took {(time() - time_start) * 1000:.2f} ms")