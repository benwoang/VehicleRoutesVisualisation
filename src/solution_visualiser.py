import matplotlib
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib.patches import Rectangle, RegularPolygon
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from solution_output import SolutionOutput
from math import floor
from cmath import pi

import time
import timeit

from matplotlib.backends.backend_qt import TimerQT


class SolutionVisualiser(FuncAnimation, FigureCanvas):
    OBSTACLE_COLOR = "#D9D9D9"
    BACKGROUND_COLOR = "#FAFAFA"
    AGENT_NUMBER_SIZE = 6
    AGENT_BORDER_WIDTH = 0.3
    TASK_NUMBER_SIZE = 5
    TASK_BORDER_WIDTH = 0.3
    TASK_ALPHA = 1.0
    PATH_WIDTH = 0.8
    PATH_ALPHA = 0.8
    TIME_RESOLUTION = 5
    DPI = 40
    FIG_SIZE = 4

    task_time_sum = 0

    def __init__(self, solution_file_path, *args, **kwargs) -> None:
        self.soln = SolutionOutput(solution_file_path)
        self.map_height = self.soln.map.map_height
        self.map_width = self.soln.map.map_width

        # Plot Speed Up
        matplotlib.rcParams["path.simplify"] = True
        matplotlib.rcParams["path.simplify_threshold"] = 1
        # mplstyle.use("fast")

        # Show plots.
        matplotlib.use(
            "QTAgg"
        )  # When using TkAgg FuncAnimtion interval must be larger than 0

        # Create empty plot.
        aspect = self.map_width / self.map_height
        self.fig = Figure(
            figsize=(self.FIG_SIZE * aspect, self.FIG_SIZE), layout="constrained"
        )

        self.canvas = FigureCanvas.__init__(self, self.fig, *args, **kwargs)
        self.animation = FuncAnimation.__init__(
            self,
            fig=self.fig,
            func=self.update_func,
            init_func=self.init,
            frames=self.time_generator(0),
            interval=0,
            blit=True,
            cache_frame_data=False,
            *args,
            **kwargs,
        )

        print("HI")

    def setup_plot(self):
        self.fig.patch.set_facecolor(self.BACKGROUND_COLOR)

        # Set axis font.
        self.ax = self.fig.gca()
        # self.ax.set_axisbelow(True)

        # Hide outside map.
        # self.fig.tight_layout(pad=1.0)

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

        self.ax.set_xlim(x_min, x_max)
        self.ax.set_ylim(y_min, y_max)

        # Shift axis to the middle of each coordinate.
        self.ax.xaxis.set(
            ticks=[i + 0.5 for i in range(0, x_max, x_step)],
            ticklabels=range(0, x_max, x_step),
        )
        self.ax.yaxis.set(
            ticks=[i + 0.5 for i in range(0, y_max, y_step)],
            ticklabels=range(0, y_max, y_step),
        )
        # self.ax.grid()

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
        self.ax.set_aspect("equal")

    # def time_generator(self, t_start):
    #     # t is in seconds wrt the solver data
    #     return [
    #         time / self.TIME_RESOLUTION
    #         for time in range(
    #             t_start * self.TIME_RESOLUTION,
    #             (self.soln.makespan * self.TIME_RESOLUTION) + 1,
    #         )
    #     ]

    def time_generator(self, t_start):
        # while True:
        #     yield t_start + 0.2
        # t is in seconds wrt the solver data
        # return [
        #     time / self.TIME_RESOLUTION
        for time in range(
            t_start * self.TIME_RESOLUTION,
            (self.soln.makespan * self.TIME_RESOLUTION) + 1,
        ):
            yield time / self.TIME_RESOLUTION

    # ]

    def setup_artists(self):
        # Build Obstacles
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
        self.task_objects = []
        temp_task_input = []
        for time_int, task_no, (x, y), agent_no in self.soln.tasks:
            if task_no < len(self.soln.tasks) / 2:
                # Pickup
                task = self.ax.add_patch(
                    RegularPolygon(
                        (x + 0.5, y + 0.56),
                        numVertices=3,
                        radius=0.5,
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

            else:
                # Delivery
                task = self.ax.add_patch(
                    RegularPolygon(
                        (x + 0.5, y + 0.43),
                        numVertices=3,
                        radius=0.5,
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
            temp_task_input.append(task)
            temp_task_input.append(task_text)
            self.task_objects.append((time_int, task, task_text))

        # Draw Initial Lines
        self.path_x_list = []
        self.path_y_list = []
        self.path_objects = [
            self.__setup_lines(a, path)
            for a, (route, path) in enumerate(zip(self.soln.routes, self.soln.paths))
        ]

        return (
            self.agent_objects
            + self.agent_name_objects
            + temp_task_input
            + self.path_objects
        )

    def __setup_lines(self, a, path):
        temp_x = [x_val + 0.5 for (x_val, _) in path]
        temp_y = [y_val + 0.5 for (_, y_val) in path]
        self.path_x_list.append(temp_x)
        self.path_y_list.append(temp_y)
        return self.ax.add_line(
            Line2D(
                temp_x[:],
                temp_y[:],
                color=COLORS[a % len(COLORS)],
                zorder=-1,
                linewidth=self.PATH_WIDTH,
                alpha=self.PATH_ALPHA,
            )
        )
        # self.fig.canvas.draw_idle()

    def update_func(self, t=0):
        # if t == 5:
        # print("HI")
        # self.time_generator(7.4)
        # self.update(7.4)
        # self.animation.pause()
        # self.animation._stop()
        # self.animation = FuncAnimation(
        #     self.fig,
        #     func=self.update,
        #     init_func=self.init,
        #     frames=self.time_generator(10),
        #     interval=1 if len(self.soln.routes) > 5 else 25,
        #     blit=True,
        #     cache_frame_data=False,
        # )
        # self.animation.resume()
        # Draw Paths
        rounded_time = floor(t)
        offset_time = t - rounded_time  # / self.TIME_RESOLUTION

        agent_index = 0
        for agent in self.path_objects:
            x_raw = self.path_x_list[agent_index]

            # Check if needs updating
            if t <= len(x_raw):
                x = self.path_x_list[agent_index][rounded_time:]
                y = self.path_y_list[agent_index][rounded_time:]

                if offset_time != 0 and len(x) > 1 and len(y) > 1:
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

                agent.set_xdata(x)
                agent.set_ydata(y)
            agent_index += 1

        # Draw agents.
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
            self.agent_name_objects[a].set_position((x + 0.49, y + 0.53))

        # Tasks are only Removed during whole numbers
        if t % 1 == 0:
            self.output_tasks = []
            j = len(self.task_objects) - 1
            while j >= 0 and self.task_objects[j][0] > t:
                self.output_tasks.append(self.task_objects[j][1])
                self.output_tasks.append(self.task_objects[j][2])
                j -= 1

        return (
            self.agent_objects
            + self.agent_name_objects
            + self.path_objects
            + self.output_tasks
        )

    def init(self):
        self.setup_plot()
        return self.setup_artists()

    def save_to_mp4(self):
        writer = FFMpegWriter(fps=15, metadata=dict(artist="Me"), bitrate=1800)
        self.animation.save("movie.mp4", writer=writer)

    def _draw_next_frame(self, framedata, blit):
        min_frame_draw_time = 0.04  # 25FPS
        # Extends the origial FuncAnimation draw_next_frame function and sleeps it if is took short
        draw_frame_start = timeit.default_timer()
        super(SolutionVisualiser, self)._draw_next_frame(framedata, blit)
        draw_frame_time = timeit.default_timer() - draw_frame_start
        if draw_frame_time < min_frame_draw_time:
            time.sleep(min_frame_draw_time - draw_frame_time)


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

if __name__ == "__main__":
    ## Generating Animation
    agent_s = timeit.default_timer()
    solution = SolutionVisualiser("solution_many_short.txt")
    agent_time = timeit.default_timer() - agent_s  # THis only mesaures update speed
    print("Animation Creation Time: ")
    print(agent_time)

    ## Saving Animation
    # agent_s = timeit.default_timer()
    # solution.animation.save("movie.mp4")
    # agent_time = timeit.default_timer() - agent_s
    # print(agent_time)

    ## Showing Animation
    # grid(which="both")
    # SolutionVisualiser.fig.show()
