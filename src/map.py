import numpy as np


class Map:
    def __init__(self, file_path=None) -> None:
        self.map_content = None

        if file_path != None:
            self.map_content = self.read_map(file_path)
            self.map_width = self.map_content.shape[0]
            self.map_height = self.map_content.shape[1]

    def read_map(self, file_path):
        # Read from file
        file = open("./map_files/" + file_path, "r")
        lines = file.read().splitlines()
        file.close()

        # Convert content file
        l = 0
        while lines[l] != "map":
            l += 1
        l += 1

        map = []
        y = 0
        for line in lines[l:]:
            row = []
            for x, c in enumerate(line):
                row.append(c == ".")
            y += 1
            map.append(row)

        map_final = np.array(map).transpose()
        return map_final

    def is_obstacle(self, x, y):
        return not self.map_content[x][y]
