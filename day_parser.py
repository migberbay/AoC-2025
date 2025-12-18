import pandas as pd

class day_parser:
    def __init__(self, day: int) -> None:
        self.filename = f"days/day{day}.txt"

    def file_to_list(self) -> list[str]:
        with open(self.filename, 'r') as file:
            lines = [line.strip() for line in file.readlines()]
        return lines
    
    def file_to_matrix(self) -> list[list[str]]:
        with open(self.filename, 'r') as file:
            matrix = [list(line.strip()) for line in file.readlines()]
        return matrix
    
    def file_to_matrix_keep_spaces(self) -> list[list[str]]:
        with open(self.filename, 'r') as file:
            matrix = [list(line.rstrip('\n')) for line in file.readlines()]
        return matrix
    
    def file_to_matrix_sep(self, separator: str, to_type = str) -> list[list[str]]:
        with open(self.filename, 'r') as file:
            matrix = [line.strip().split(separator) for line in file.readlines()]
            # remove empty strings if any
            matrix = [[to_type(item) for item in row if item] for row in matrix]
        return matrix
        
    def file_to_dataframe(self, mode, sep=',') -> pd.DataFrame:
        if mode == 'basic':
            matrix = self.file_to_matrix()
        else:
            matrix = self.file_to_matrix_sep(sep)
            
        df = pd.DataFrame(matrix)
        return df
    
    def file_string_to_list(self, delimiter: str = ',') -> list[str]:
        with open(self.filename, 'r') as file:
            content = file.read().strip()
            items = content.split(delimiter)
        return [item.strip() for item in items]
    
    def file_from_day_12(self):
        with open(self.filename, 'r') as file:
            skipcount, getcount, presents = 0, 3, 0
            present_shapes = dict()
            current_shape = []
            trees = []
            for i, line in enumerate(file.readlines()):
                if i == 0: continue  #skip first line 
                
                if presents < 6:
                    if skipcount > 0:
                        skipcount -= 1
                        continue
                    
                    if getcount > 0:
                        getcount -= 1
                        current_shape.append(line.strip())
                    
                    if getcount == 0 and skipcount == 0:
                        present_shapes[presents] = current_shape
                        presents += 1
                        getcount = 3
                        skipcount = 2
                        current_shape = []
                
                else: #parse the plots under the trees
                    # if line is empty, continue
                    if not line.strip().strip('\n'):
                        continue
                    
                    size, presents_needed = line.split(': ')
                    a,b = size.split('x')
                    size = (int(a), int(b))
                    presents_needed = presents_needed.split(' ')
                    presents_needed = {i:int(x.strip()) for i,x in enumerate(presents_needed)}
                    trees.append( (size, presents_needed) )

            return present_shapes, trees
