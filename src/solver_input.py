from map import Map
from solution_visualiser import COLORS
from matplotlib.patches import Rectangle, RegularPolygon
from matplotlib.text import Text

from cmath import pi


class SolverInput:
    AGENT_COLOURS = [
        # "#000000",  # black
        "#ffffff",  # white
    ]
    TASK_COLOURS = [
        "#F85647",  # red
        "#FEDC2C",  # yellow
        "#50D546",  # green
        "#5CB4FF",  # blue
        "#C397FD",  # purple
        "#F494C4",  # pink
        "#57DBC2",  # mint
        "#FF9F2C",  # orange
        "#7FA4E9",  # violet
        # '#F6968C', # salmon
        "#B9DC67",  # lime
        "#EAAF89",  # tan
        # '#00B0F0', # ProcessBlue
        # '#ED1B23', # Red
        # '#FFDF42', # Goldenrod
        # '#00A64F', # Green
        # '#7977B8', # Periwinkle
        # '#F7921D', # BurntOrange
        # '#00B3B8', # BlueGreen
        # '#F69289', # Salmon
        "#C6DC67",  # SpringGreen
        "#F49EC4",  # Lavender
        "#EC008C",  # Magenta
        "#008B72",  # PineGreen
        "#99479B",  # Purple
        "#0071BC",  # RoyalBlue
        "#DA9D76",  # Tan
    ]
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
        self.map_string = map_string  # TODO: Fix this
        if map_string != None:
            self.map = Map(map_string)

    def change_map(self, map_file_string):
        self.map = Map(map_file_string)

    def add_new_agent(self, x_int, y_int):
        if (
            self.map.is_obstacle(x_int, y_int) == False
            and self.check_occupied(x_int, y_int) == False
        ):
            agent = Rectangle(
                (x_int + 0.13, y_int + 0.13),
                width=0.7,
                height=0.7,
                zorder=10000,
                facecolor=self.AGENT_COLOURS[
                    len(self.agent_objects) % len(self.AGENT_COLOURS)
                ],
                edgecolor="black",
                linewidth=0.3,
                picker=True,
            )

            agent_text = Text(
                x_int + 0.49,
                y_int + 0.53,
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

    def check_occupied(self, x, y):
        occupied = False
        for item, text in self.agent_objects + self.task_objects:
            if item.contains_point([x, y]):
                occupied = True
            elif (
                type(item) == Rectangle
                and round(item.get_x() - 0.13) == x
                and round(item.get_y() - 0.13) == y
            ):
                occupied = True
            elif (
                type(item) == RegularPolygon
                and round(item.xy[0] - 0.5) == x
                and round(item.xy[1] - 0.56) == y
            ):
                occupied = True
        print("Occupied: " + str(occupied))
        return occupied

    def add_new_task(self, x_exact, y_exact):
        if (
            self.map.is_obstacle(x_exact, y_exact) == False
            and self.check_occupied(x_exact, y_exact) == False
        ):
            task = RegularPolygon(
                (x_exact + 0.5, y_exact + 0.56),
                numVertices=3,
                radius=0.5,
                orientation=pi if len(self.task_objects) % 2 == 0 else 0.0,
                zorder=10000,
                facecolor=self.TASK_COLOURS[
                    (len(self.task_objects)//2) % len(self.TASK_COLOURS)
                ],
                edgecolor="black",
                linewidth=0.3,
                picker=True,
            )

            task_text = Text(
                x_exact + 0.49,
                y_exact + 0.56,
                f"{len(self.task_objects)//2 if len(self.task_objects)%2==0 else (len(self.task_objects)-1)//2}",
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

    def delete_tasks(self):
        for item, task in self.task_objects:
            item.remove()
            task.remove()
        self.task_objects = []

    def delete_agents(self):
        for agent, task in self.agent_objects:
            agent.remove()
            task.remove()
        self.agent_objects = []

    def generate_text_file(self):
        f = open("demo.scen", "w")
        f.write('version 2\n')
        time_horizon = 300
        f.write(f'time horizon {time_horizon}\n')

        for a, (agent, task) in enumerate(self.agent_objects):
            f.write(f'{a:5d}')
            f.write(f'{self.map_string:>20s}')
            f.write(f'{self.map.map_width:5d}')
            f.write(f'{self.map.map_height:5d}')
            f.write(f'{round(agent.get_x() - 0.13):5d}')
            f.write(f'{round(agent.get_y() - 0.13):5d}')
            f.write(f'{round(agent.get_x() - 0.13):5d}')
            f.write(f'{round(agent.get_y() - 0.13):5d}')
            f.write('\n')

        f.write('requests\n')
        for t, (task, task2) in enumerate(self.task_objects):
            if t % 2 == 1:
                f.write(f'{round(task.xy[0] - 0.5):5d}')
                f.write(f'{round(task.xy[1] - 0.56):5d}')
                f.write(f'{0:5d}')
                f.write(f'{time_horizon:5d}')
                f.write(f'{0:5d}')
                f.write(f'{time_horizon:5d}')
                f.write('\n')

            else:
                f.write(f'{t // 2:5d}')
                f.write(f'{round(task.xy[0] - 0.5):5d}')
                f.write(f'{round(task.xy[1] - 0.56):5d}')

        f.close()
