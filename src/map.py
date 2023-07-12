import numpy as np
class Map:

    def __init__(self, file_path=None) -> None:
        self.file_path = file_path
        self.map_content = None
        
        if self.file_path != None:
            self.map_content = self.read_map();


    def read_map(self):
        # Read from file
        file = open("./SampleData/"+ self.file_path, 'r')
        lines = file.read().splitlines()
        file.close()

        # Convert content file
        l = 0
        while lines[l] != 'map':
            l += 1
        l += 1

        map = []
        y = 0
        for line in lines[l:]:
            row = []
            for (x, c) in enumerate(line):
                row.append(c == '.')
            y += 1
            map.append(row)

        map_final = np.array(map).transpose()
        return map_final
