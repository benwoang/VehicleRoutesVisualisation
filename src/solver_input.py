from map import Map
from solution_visualiser import COLORS
from matplotlib.patches import Rectangle, RegularPolygon
from matplotlib.text import Text

from cmath import pi


class SolverInput:
    # Format
    # Agent
    # 0	31x79-w5.map	79	31	41	18	71	0	0
    # Agent number, map file, map width, map height, x y of start position, x y of end position, dummy number

    # Tasks
    # 0	24	15	28	12	19	37	26	44
    # 1	(39	10	24	18)	(154	196	177	219)
    # Task number, pickup x y, pickup time window (I forgot to explain to you time window, just put 0, 300), delivery xy, delivery time window
    def __init__(self, map_string=None) -> None:
        self.task_objects = []  # Contains task
        self.agent_objects = []  # Contains tuple of agent and its text
        self.map = None
        if map_string != None:
            self.map = Map(map_string)

    def change_map(self, map_file_string):
        self.map = Map(map_file_string)

    def add_new_agent(self, x_exact, y_exact):
        if (
            self.map.is_obstacle(x_exact, y_exact) == False
            and self.check_occupied(x_exact, y_exact) == False
        ):
            agent = Rectangle(
                (x_exact + 0.13, y_exact + 0.13),
                width=0.7,
                height=0.7,
                zorder=10000,
                facecolor=COLORS[len(self.agent_objects) % len(COLORS)],
                edgecolor="black",
                linewidth=0.3,
                picker=True,
            )

            agent_text = Text(
                x_exact + 0.49,
                y_exact + 0.53,
                f"{len(self.agent_objects)}",
                color="black",
                zorder=10001,
                fontsize=6,
                horizontalalignment="center",
                verticalalignment="center",
                picker=True,
            )
            self.agent_objects.append((agent, agent_text))
            return agent, agent_text
        else:
            return None

    def remove_agent(self):
        pass

    def check_occupied(self, x, y):
        occupied = False
        for item, text in self.agent_objects + self.task_objects:
            if item.contains_point([x, y]):
                occupied = True
            elif item.get_x() - 0.13 == x and item.get_y() - 0.13 == y:
                occupied = True
            elif item.get_x() - 0.5 == x and item.get_y() - 0.56 == y:
                occupied = True
        return occupied

    def add_task(self, x_exact, y_exact):
        if (
            self.map.is_obstacle(x_exact, y_exact) == False
            and self.check_occupied(x_exact, y_exact) == False
        ):
            task = RegularPolygon(
                (x_exact + 0.5, y_exact + 0.56),
                numVertices=3,
                radius=0.5,
                orientation=pi,
                zorder=10000,
                facecolor=COLORS[len(self.task_objects) % len(COLORS)],
                edgecolor="black",
                linewidth=0.3,
                picker=True,
            )

            task_text = Text(
                x_exact + 0.49,
                y_exact + 0.56,
                f"{len(self.task_objects)}",
                color="black",
                zorder=10001,
                fontsize=6,
                horizontalalignment="center",
                verticalalignment="center",
                picker=True,
            )
            self.task_objects.append((task, task_text))
            return task, task_text
        else:
            return None

    def remove_task(self):
        pass

    def generate_text_file(self):
        pass
