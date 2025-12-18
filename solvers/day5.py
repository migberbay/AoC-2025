# PART 1
# INSTRUCTIONS

# EXAMPLE

# PART 2

# INSTRUCTIONS

# EXAMPLE

from .base_solver import solver

def between(value, start, end):
    return start <= value <= end

def pre_process(data):
    ids, ranges = [], []
        
    for x in data: 
        if x == '':
            continue
        
        if '-' in x:
            start, end = map(int, x.split('-'))
            ranges.append( (start, end) )
        else:
            ids.append( int(x) )
            
    return ids, ranges

def ranges_touch(r1, r2):
    return (
        r1[0] == r2[0]
        or r1[0] == r2[1]
        or r1[1] == r2[0]
        or r1[1] == r2[1]
    )

def try_combine(r1, r2):
    if (between(r1[0], r2[0], r2[1]) 
    or between(r1[1], r2[0], r2[1])
    or between(r2[0], r1[0], r1[1])
    or between(r2[1], r1[0], r1[1]) 
    or ranges_touch(r1, r2)):
        return (min(r1[0], r2[0]), max(r1[1], r2[1]))


# solver class has a self.parser to read the file for the day.
class solve(solver):
    def part1(self):
        data = self.parser.file_to_list()
        ids, ranges = pre_process(data)
        
        res = 0
        
        for i in ids:
            for r in ranges:
                if between(i, r[0], r[1]):
                    res += 1
                    break
                    
        return res
    
    def part2(self):
        data = self.parser.file_to_list()
        _, ranges = pre_process(data)
        
        res = []
        
        for evaluated in ranges:
            modif = False
            # try to combine it with existing ranges
            for i, existing in enumerate(res):
                new_r = try_combine(evaluated, existing)
                if new_r is not None:
                    res[i] = new_r
                    modif = True
                    break
            
            # if was not combinable, just add it
            if not modif:
                res.append(evaluated)
                
            # if it was combinable, we need to check again all ranges
            # for new possible combinations.
            else:
                # we will keep checking until no more combinations are possible
                # len_res stays the same we know we are done
                len_res = len(res)
                
                while True:
                    changed_range = res[i]
                    del res[i]
                    
                    for r in res:
                        new_r = try_combine(changed_range, r)
                        if new_r is not None: #if combination succeeded
                            changed_range = new_r
                            res.remove(r) # out with the old
                    res.append(changed_range) # in with the new
                    # if we made no changes, we are done
                    if len(res) == len_res:
                        break
                    else:
                        len_res = len(res)
                
        tot_ids = 0
        for r in res:
            tot_ids += (r[1] - r[0] + 1)
            
        return tot_ids