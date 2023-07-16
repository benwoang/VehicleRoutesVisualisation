import matplotlib
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle, Rectangle, RegularPolygon

from collections import deque


from solution import Solution
from math import floor
from cmath import pi

import copy

import timeit


class SolutionVisualiser:
    OBSTACLE_COLOR = "#D9D9D9"
    BACKGROUND_COLOR = "#FAFAFA"
    AGENT_NUMBER_SIZE = 6
    AGENT_BORDER_WIDTH = 0.3
    TASK_NUMBER_SIZE = 5
    TASK_BORDER_WIDTH = 0.3
    TASK_ALPHA = 1.0
    PATH_WIDTH = 0.8
    PATH_ALPHA = 0.8
    TIME_RESOLUTION = 10
    DPI = 600
    VIDEO_FPS = 4 * TIME_RESOLUTION
    FIG_SIZE = 5
    OUTPUT_DIR = "./"
    NUM_PROCESSES = 6

    SHOW_TIMESTEP = False
    SHOW_AGENT_NUMBER = True
    SHOW_REQUEST_NUMBER = True

    def __init__(self, solution_file_path) -> None:
        self.soln = Solution(solution_file_path)
        self.map_height = self.soln.map.map_height
        self.map_width = self.soln.map.map_width

        # Plot Speed Up
        # matplotlib.rcParams["path.simplify"] = True
        # matplotlib.rcParams["path.simplify_threshold"] = 1
        # mplstyle.use("fast")

        # Don't show plots.
        plt.ioff()
        matplotlib.use(
            "QTAgg"
        )  # When using TkAgg FuncAnimtion interval must be larger than 0

        # Create empty plot.
        aspect = self.map_width / self.map_height
        self.fig = plt.figure(figsize=(self.FIG_SIZE * aspect, self.FIG_SIZE))

        self.animation = FuncAnimation(
            self.fig,
            self.update,
            init_func=self.init,
            frames=self.time_generator(0),
            interval=20,
            blit=True,
        )

    def setup_plot(self):
        self.fig.patch.set_facecolor(self.BACKGROUND_COLOR)

        # Set axis font.
        self.ax = plt.gca()
        # self.ax.set_axisbelow(True)

        # Hide outside map.
        plt.tight_layout(pad=1.0)

        # Set background color
        self.ax.set_facecolor("white")

        # Set axis range.
        x_min = 0
        y_min = 0
        x_max = self.map_width
        y_max = self.map_height
        x_step = 5 if x_max <= 50 else 10
        y_step = 5 if y_max <= 50 else 10

        # if you want to see 1 by 1 grid use these two steps
        # x_step = 1
        # y_step = 1

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

        # title_text = self.ax.text(
        #     -11.5,
        #     -3.0,
        #     "Branch-and-cut-and-price for multi-agent pickup and delivery",
        #     horizontalalignment="left",
        # )
        # author_text = self.ax.text(
        #     -11.5,
        #     -1.3,
        #     "Edward Lam <edward.lam@monash.edu>",
        #     horizontalalignment="left",
        # )

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

    def time_generator(self, t_start):
        # t is in seconds wrt the solver data
        return [
            time / self.TIME_RESOLUTION
            for time in range(
                t_start * self.TIME_RESOLUTION,
                (self.soln.makespan * self.TIME_RESOLUTION) + 1,
            )
        ]

    def setup_artists(self):
        # Build Obstacles
        # x_s = timeit.default_timer()
        for y in range(self.map_height):
            x_begin = 0
            x_end = self.map_width
            while x_begin < self.map_width:
                if not self.soln.map.map_content[x_begin, y]:
                    for x in range(x_begin + 1, self.map_width):
                        if self.soln.map.map_content[x, y]:
                            x_end = x
                            break
                    self.ax.add_patch(
                        Rectangle(
                            (x_begin, y),
                            x_end - x_begin,
                            1,
                            zorder=-2,
                            facecolor=self.OBSTACLE_COLOR,
                            edgecolor="none",
                        )
                    )
                    x_begin = x_end + 1
                else:
                    x_begin += 1
        # print("init_func")
        # print(timeit.default_timer() - x_s)
        # Draw agents.
        self.agent_objects = []
        self.agent_name_objects = []
        for a, (route, path) in enumerate(zip(self.soln.routes, self.soln.paths)):
            x, y = (path[0][0] + 0.13, path[0][1] + 0.13)
            object = self.ax.add_patch(
                Rectangle(
                    (x, y),
                    width=0.7,
                    height=0.7,
                    zorder=10000,
                    facecolor=COLORS[a % len(COLORS)],
                    edgecolor="black",
                    linewidth=self.AGENT_BORDER_WIDTH,
                )
            )
            self.agent_objects.append(object)

            if self.SHOW_AGENT_NUMBER:
                x, y = (path[0][0] + 0.49, path[0][1] + 0.53)
                text = self.ax.text(
                    x,
                    y,
                    f"{a}",
                    color="black",
                    zorder=10001,
                    fontsize=self.AGENT_NUMBER_SIZE,
                    horizontalalignment="center",
                    verticalalignment="center",
                )
                #    fontfamily='Helvetica Neue')
                self.agent_name_objects.append(text)

        # Draw tasks.
        # List
        self.task_tuple_objects = []
        for time_int, task_no, (x, y), agent_no in self.soln.tasks:
            if task_no < len(self.soln.tasks) / 2:
                # Pickup
                task = self.ax.add_patch(
                    RegularPolygon(
                        (x + 0.5, y + 0.56),
                        numVertices=3,
                        radius=0.35,
                        orientation=pi,
                        zorder=task_no,
                        facecolor=COLORS[agent_no % len(COLORS)]
                        if time_int >= 0
                        else "white",
                        edgecolor="black",
                        linewidth=self.TASK_BORDER_WIDTH,
                        alpha=self.TASK_ALPHA,
                    )
                )
                # self.task_objects.append(object)

                if self.SHOW_REQUEST_NUMBER:
                    label = f"{task_no}"
                    task_text = self.ax.text(
                        x + 0.49,
                        y + 0.56,
                        label,
                        color="black",
                        zorder=task_no + 0.5,
                        fontsize=self.TASK_NUMBER_SIZE,
                        horizontalalignment="center",
                        verticalalignment="center",
                    )
                    # fontfamily='Helvetica Neue')
                # self.task_objects.append(object)
                self.task_tuple_objects.append((time_int, task, task_text))
            else:
                # Delivery
                task = self.ax.add_patch(
                    RegularPolygon(
                        (x + 0.5, y + 0.43),
                        numVertices=3,
                        radius=0.35,
                        orientation=0,
                        zorder=task_no,
                        facecolor=COLORS[agent_no % len(COLORS)]
                        if time_int >= 0
                        else "white",
                        edgecolor="black",
                        linewidth=self.TASK_BORDER_WIDTH,
                        alpha=self.TASK_ALPHA,
                    )
                )
                # self.task_objects.append(object)

                if self.SHOW_REQUEST_NUMBER:
                    label = f"{int(task_no - len(self.soln.tasks) / 2)}"
                    task_text = self.ax.text(
                        x + 0.49,
                        y + 0.45,
                        label,
                        color="black",
                        zorder=task_no + 0.5,
                        fontsize=self.TASK_NUMBER_SIZE,
                        horizontalalignment="center",
                        verticalalignment="center",
                    )
                    # fontfamily='Helvetica Neue')
                self.task_tuple_objects.append((time_int, task, task_text))

        # Sets
        # # self.task_objects = []
        # # self.task_name_objects = []
        # for time_tasks in self.soln.tasks.items():
        #     time_int = time_tasks[0]
        #     for task_no, (x, y), agent in time_tasks[1]:
        #         # Delivery task number will always be Pickup task number + Number of tasks / 2
        #         if task_no < len(self.soln.tasks) / 2:
        #             # Pickup
        #             object = self.ax.add_patch(
        #                 RegularPolygon(
        #                     (x + 0.5, y + 0.56),
        #                     numVertices=3,
        #                     radius=0.35,
        #                     orientation=pi,
        #                     zorder=task_no,
        #                     facecolor=COLORS[agent % len(COLORS)]
        #                     if time_int >= 0
        #                     else "white",
        #                     edgecolor="black",
        #                     linewidth=self.TASK_BORDER_WIDTH,
        #                     alpha=self.TASK_ALPHA,
        #                 )
        #             )
        #             # self.task_objects.append(object)

        #             if self.SHOW_REQUEST_NUMBER:
        #                 label = f"{task_no}"
        #                 object = self.ax.text(
        #                     x + 0.49,
        #                     y + 0.56,
        #                     label,
        #                     color="black",
        #                     zorder=task_no + 0.5,
        #                     fontsize=self.TASK_NUMBER_SIZE,
        #                     horizontalalignment="center",
        #                     verticalalignment="center",
        #                 )
        #                 # fontfamily='Helvetica Neue')
        #                 # self.task_name_objects.append(object)

        #         else:
        #             # Delivery
        #             object = self.ax.add_patch(
        #                 RegularPolygon(
        #                     (x + 0.5, y + 0.43),
        #                     numVertices=3,
        #                     radius=0.35,
        #                     orientation=0,
        #                     zorder=task_no,
        #                     facecolor=COLORS[agent % len(COLORS)]
        #                     if time_int >= 0
        #                     else "white",
        #                     edgecolor="black",
        #                     linewidth=self.TASK_BORDER_WIDTH,
        #                     alpha=self.TASK_ALPHA,
        #                 )
        #             )
        #             # self.task_objects.append(object)

        #             if self.SHOW_REQUEST_NUMBER:
        #                 label = f"{int(task_no - len(self.soln.tasks) / 2)}"
        #                 object = self.ax.text(
        #                     x + 0.49,
        #                     y + 0.45,
        #                     label,
        #                     color="black",
        #                     zorder=task_no + 0.5,
        #                     fontsize=self.TASK_NUMBER_SIZE,
        #                     horizontalalignment="center",
        #                     verticalalignment="center",
        #                 )
        #                 # fontfamily='Helvetica Neue')
        #                 # self.task_name_objects.append(object)
        ## Set Time Tuples
        test = []  # deque()
        for a, b, c in self.task_tuple_objects:
            test.append(b)
            test.append(c)

        # Draw Initial Lines
        self.path_objects = []
        for a, (route, path) in enumerate(zip(self.soln.routes, self.soln.paths)):
            self.path_objects.append(
                self.ax.add_line(
                    plt.Line2D(
                        [xx + 0.5 for (xx, yy) in path],
                        [yy + 0.5 for (xx, yy) in path],
                        color=COLORS[a % len(COLORS)],
                        zorder=-1,
                        linewidth=self.PATH_WIDTH,
                        alpha=self.PATH_ALPHA,
                    )
                )
            )
        # self.path_objects_copy = copy.deepcopy(self.path_objects)

        return self.agent_objects + self.agent_name_objects + test + self.path_objects

    def update(self, t):
        updated_line_objects = []
        rounded_time = floor(t)
        offset_time = t - rounded_time  # / self.TIME_RESOLUTION
        for agent in self.path_objects:
            agent_copy = copy.copy(agent)
            x_raw = agent_copy.get_xdata()
            # Check if the line has any more lines
            if t <= len(x_raw):
                # Get all x, y values
                x = x_raw[rounded_time:]
                y = agent_copy.get_ydata()[rounded_time:]
                # Check if you need to offset and only when there is more than 1 item left in array
                if offset_time != 0 and len(x) > 1 and len(y) > 1:
                    # time is not an integer adjust first array value
                    # Check if only x or y changes if none change no need to adjust
                    if x[0] != x[1]:
                        if x[1] > x[0]:
                            x[0] = x[0] + offset_time
                        else:
                            x[0] = x[0] - offset_time
                    elif y[0] != y[1]:
                        if y[1] > y[0]:
                            y[0] = y[0] + offset_time
                        else:
                            y[0] = y[0] - offset_time
                # elif offset_time > 0 and len(x) > 1 and len(y) > 1:

                agent_copy.set_xdata(x)
                agent_copy.set_ydata(y)
                updated_line_objects.append(agent_copy)

        # x_22 = timeit.default_timer()
        # Draw agents and paths.
        # path_objects = []
        for a, (route, path) in enumerate(zip(self.soln.routes, self.soln.paths)):
            # Get position.
            agent_time = t  # + substep / self.TIME_RESOLUTION
            index = floor(agent_time)
            proportion = agent_time - index
            x_curr, y_curr = path[index] if index < len(path) else path[-1]
            x_next, y_next = path[index + 1] if index + 1 < len(path) else path[-1]
            x = proportion * (x_next - x_curr) + x_curr
            y = proportion * (y_next - y_curr) + y_curr

            # Update position.
            self.agent_objects[a].set_xy((x + 0.13, y + 0.13))
            if self.SHOW_AGENT_NUMBER:
                self.agent_name_objects[a].set_position((x + 0.49, y + 0.53))

        # Tasks are only Removed during whole numbers

        # task_t = floor(t)
        # for time_tasks in self.soln.tasks.items():
        # time_int = time_tasks[0]

        # for task_no, (x, y), agent in time_tasks[1]:
        #     # Delivery task number will always be Pickup task number + Number of tasks / 2
        #     if task_no < len(self.soln.tasks) / 2:
        #         # Pickup
        #         object = self.ax.add_patch(
        #             RegularPolygon(
        #                 (x + 0.5, y + 0.56),
        #                 numVertices=3,
        #                 radius=0.35,
        #                 orientation=pi,
        #                 zorder=task_no,
        #                 facecolor=COLORS[agent % len(COLORS)]
        #                 if time_int >= 0
        #                 else "white",
        #                 edgecolor="black",
        #                 linewidth=self.TASK_BORDER_WIDTH,
        #                 alpha=self.TASK_ALPHA,
        #             )
        #         )
        #         self.task_objects.append(object)

        #         if self.SHOW_REQUEST_NUMBER:
        #             label = f"{task_no}"
        #             object = self.ax.text(
        #                 x + 0.49,
        #                 y + 0.56,
        #                 label,
        #                 color="black",
        #                 zorder=task_no + 0.5,
        #                 fontsize=self.TASK_NUMBER_SIZE,
        #                 horizontalalignment="center",
        #                 verticalalignment="center",
        #             )
        #             # fontfamily='Helvetica Neue')
        #             self.task_name_objects.append(object)

        #     else:
        #         # Delivery
        #         # Delivery
        #         object = self.ax.add_patch(
        #             RegularPolygon(
        #                 (x + 0.5, y + 0.43),
        #                 numVertices=3,
        #                 radius=0.35,
        #                 orientation=0,
        #                 zorder=task_no,
        #                 facecolor=COLORS[agent % len(COLORS)]
        #                 if time_int >= 0
        #                 else "white",
        #                 edgecolor="black",
        #                 linewidth=self.TASK_BORDER_WIDTH,
        #                 alpha=self.TASK_ALPHA,
        #             )
        #         )
        #         self.task_objects.append(object)

        #         if self.SHOW_REQUEST_NUMBER:
        #             label = f"{int(task_no - len(self.soln.tasks) / 2)}"
        #             object = self.ax.text(
        #                 x + 0.49,
        #                 y + 0.45,
        #                 label,
        #                 color="black",
        #                 zorder=task_no + 0.5,
        #                 fontsize=self.TASK_NUMBER_SIZE,
        #                 horizontalalignment="center",
        #                 verticalalignment="center",
        #             )
        #             # fontfamily='Helvetica Neue')
        #             self.task_name_objects.append(object)

        # Update Tasks
        test = []
        less_time = True
        # i = 0
        # while i < len(self.task_tuple_objects):
        #     if t < self.task_tuple_objects[i][0]:
        #         test.append(self.task_tuple_objects[i][1])
        #         test.append(self.task_tuple_objects[i][2])
        #     i += 1

        j = len(self.task_tuple_objects) - 1

        while j >= 0 and self.task_tuple_objects[j][0] > t:
            test.append(self.task_tuple_objects[j][1])
            test.append(self.task_tuple_objects[j][2])
            j -= 1

        # print(timeit.default_timer() - x_22)
        # print("t = " + str(t) + "\n")
        # print(updated_line_objects[1].get_xdata())
        return (
            updated_line_objects + self.agent_objects + self.agent_name_objects + test
        )

    def init(self):
        self.setup_plot()
        return self.setup_artists()


if __name__ == "__main__":
    COLORS = [
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
    ## Generating Animation
    agent_s = timeit.default_timer()
    # solution = SolutionVisualiser("solution.txt")
    solution = SolutionVisualiser("solution.txt")
    # solution = SolutionVisualiser("solution_short_long.txt")
    agent_time = timeit.default_timer() - agent_s  # THis only mesaures update speed
    print("Animation Creation Time: ")
    print(agent_time)

    ## Saving Animation
    # agent_s = timeit.default_timer()
    # solution.animation.save("movie.mp4")
    # agent_time = timeit.default_timer() - agent_s
    # print(agent_time)

    ## Showing Animation
    # plt.grid(which="both")
    plt.show()
