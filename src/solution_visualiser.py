import re
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class SolutionVisualiser:
    BACKGROUND_COLOR = "#FAFAFA"
    FIG_SIZE = 4

    def __init__(self, file_path=None) -> None:
        self.offset = 1
        self.routes, self.paths = self.read_routes_and_paths(file_path)
        self.makespan = max(len(path) for path in self.paths)
        self.tasks = self.get_tasks()
        self.animation = FuncAnimation(
            self.fig,
            self.update,
            init_func=self.init,
            frames=100,
            interval=100,
            blit=True,
        )

    def load_solution_file(self):
        pass

    def read_routes_and_paths(self, txt):
        lines = self.__escape_ansi(txt).split("\n")

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
        tasks = {}
        for agent_no, (route, path) in enumerate(zip(self.routes, self.paths)):
            for r, t in route[1:-1]:  # uses route in between first and last items
                tasks[r] = (t, path[t], agent_no)
        return tasks

    def setup_plot(self):
        # Don't show plots.
        plt.ioff()
        matplotlib.use("TkAgg")

        # Create empty plot.
        aspect = map_width / map_height
        self.fig = plt.figure(figsize=(self.FIG_SIZE * aspect, self.FIG_SIZE))
        self.fig.patch.set_facecolor(self.BACKGROUND_COLOR)

        # Set axis font.
        self.ax = plt.gca()

        # Hide outside map.
        plt.tight_layout(pad=1.0)

        # Set background color
        self.ax.set_facecolor("white")

        # Set axis range.
        x_min = 0
        y_min = 0
        x_max = map_width
        y_max = map_height
        x_step = 5 if x_max <= 50 else 10
        y_step = 5 if y_max <= 50 else 10
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)

        # Shift axis to the middle of each coordinate.
        self.ax.xaxis.set(
            ticks=[i + 0.5 for i in range(0, x_max, x_step)],
            ticklabels=range(0, x_max, x_step),
        )
        self.ax.yaxis.set(
            ticks=[i + 0.5 for i in range(0, y_max, y_step)],
            ticklabels=range(0, y_max, y_step),
        )

        # Hide ticks
        self.ax.tick_params(
            axis="both",  # changes apply to both axes
            which="both",  # both major and minor ticks are affected
            left=False,  # ticks along the left edge are off
            right=False,  # ticks along the right edge are off
            top=False,  # ticks along the top edge are off
            bottom=False,  # ticks along the bottom edge are off
            labelleft=False,  # labels along the left edge are off
            labelbottom=False,
        )  # labels along the bottom edge are off

        # Reverse vertical axis.
        self.ax.invert_yaxis()

    def setup_artists(self):
        pass

    def update(self, i):
        pass

    def init(self):
        self.setup_plot()
        return self.setup_artists()

    def __escape_ansi(self, line):
        ansi_escape = re.compile("(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]")
        return ansi_escape.sub("", line)


if __name__ == "__main__":
    file_path = "./SampleData/solution.txt"
    solution = SolutionVisualiser(file_path=file_path)
