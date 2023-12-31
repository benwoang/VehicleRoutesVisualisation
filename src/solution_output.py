import re
from map import Map
from collections import deque


class SolutionOutput:
    def __init__(self, file_path=None) -> None:
        # Initialise Variables from Solution File
        solution_array = self.load_solution_file("./solution_files/" + file_path)
        map_file_path = solution_array[0]
        solution_string = solution_array[1]
        self.offset = int(solution_array[2])
        self.prefix = solution_array[3]

        self.map = Map(map_file_path)
        self.routes, self.paths = self.read_routes_and_paths(solution_string)
        self.makespan = max(len(path) for path in self.paths)
        self.tasks = self.get_tasks()

    def load_solution_file(self, file_path):
        # Read text files and apply string processing
        with open(file_path) as f:
            file_content = f.read()

        chunks = re.findall(r"^.+=[^=]+\n", file_content, flags=re.MULTILINE)
        chunks = [chunk[:-1] for chunk in chunks if chunk[3:] != "'''"]
        chunks = [chunk.split(" = ", 1) for chunk in chunks]
        chunks = [chunk[1].replace("'", "") for chunk in chunks]

        return chunks

    def read_routes_and_paths(self, solution_string):
        lines = self.__escape_ansi(solution_string).split("\n")

        routes = [line for line in lines if "Route:" in line]
        routes = [re.findall(r"(\d+) \((\d+)\)", route) for route in routes]
        routes = [[(int(r), int(t)) for r, t in route] for route in routes]

        paths = [line for line in lines if "Path:" in line]
        paths = [re.findall(r"\((\d+),(\d+)\)", path) for path in paths]
        paths = [
            [(int(x) - self.offset, int(y) - self.offset) for x, y in path]
            for path in paths
        ]

        assert len(routes) == len(paths)

        # Post-process to remove paths going backwards and forwards
        excluded_times = {(a, t) for a, route in enumerate(routes) for (_, t) in route}
        makespan = max(route[-1][1] for route in routes)
        used_vertices = set()
        for a, path in enumerate(paths):
            length = len(path)
            for t in range(makespan):
                used_vertices.add((a, t, path[min(length - 1, t)]))
        for a, path in enumerate(paths):
            for t in range(len(path) - 2):
                if (a, t + 1) not in excluded_times:
                    if path[t] != path[t + 1] and path[t] == path[t + 2]:
                        xxx = [
                            (a2, t2, v2)
                            for (a2, t2, v2) in used_vertices
                            if (t2, v2) == (t + 1, path[t])
                        ]
                        if len(xxx) > 0:
                            print(f"Not modifying agent {a} time {t + 1}")
                        else:
                            path[t + 1] = path[t]
                            print(f"Modifying agent {a} time {t + 1}")

        return routes, paths

    def get_tasks(self):
        tasks = []
        for agent_no, (route, path) in enumerate(zip(self.routes, self.paths)):
            # Both Routes and Paths are lined up for each agent
            ## LIST with TUPLES
            for route_number, time_int in route[1:-1]:
                tasks.append((time_int, route_number, path[time_int], agent_no))

        tasks.sort(key=lambda task: task[0])  # Sort by time
        # route and task number are synonomous
        return tasks

    def __escape_ansi(self, line):
        ansi_escape = re.compile("(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]")
        return ansi_escape.sub("", line)


if __name__ == "__main__":
    soln = SolutionOutput("solution.txt")
