from map import Map
from solution_visualiser import COLORS
from matplotlib.patches import Rectangle, RegularPolygon
from matplotlib.text import Text

from cmath import pi


class SolverInput:
    AGENT_COLOURS = [
        "#F85647",  # red
        "#50D546",  # green
    ]
    TASK_COLOURS = [
        "#FEDC2C",  # yellow
        "#5CB4FF",  # blue
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
                f"{len(self.agent_objects)//2 if len(self.agent_objects)%2==0 else (len(self.agent_objects)-1)//2}",
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
                orientation=pi,
                zorder=10000,
                facecolor=self.TASK_COLOURS[
                    len(self.task_objects) % len(self.TASK_COLOURS)
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
        f_a = open("solver_input_agents.txt", "w")
        a_count = 0
        string = ""
        for agent, task in self.agent_objects:
            if a_count % 2 == 1:
                string += str(round(agent.get_x() - 0.13)) + " "
                string += str(round(agent.get_y() - 0.13)) + " "
                string += "\n"

            else:
                string += str(a_count // 2) + " "
                string += self.map_string + " "
                string += str(self.map.map_width) + " "
                string += str(self.map.map_height) + " "
                string += str(round(agent.get_x() - 0.13)) + " "
                string += str(round(agent.get_y() - 0.13)) + " "
            a_count += 1
        f_a.write(string)
        f_a.close()
        f_t = open("solver_input_tasks.txt", "w")
        t_count = 0
        string = ""
        for task, task2 in self.task_objects:
            if t_count % 2 == 1:
                string += str(round(task.xy[0] - 0.5)) + " "
                string += str(round(task.xy[1] - 0.56)) + " "
                string += "0 300 "
                string += "\n"

            else:
                string += str(t_count // 2) + " "
                string += str(round(task.xy[0] - 0.5)) + " "
                string += str(round(task.xy[1] - 0.56)) + " "
                string += "0 300 "
            t_count += 1

        f_t.write(string)
        f_t.close()
