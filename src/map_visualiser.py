from map import Map
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.patches import Rectangle
import matplotlib.ticker as mticker
from solution_input import SolutionInput


class MapVisualiser(FigureCanvas):
    BACKGROUND_COLOR = "#FAFAFA"
    OBSTACLE_COLOR = "#D9D9D9"

    def __init__(self, map_file_path, parent_widget) -> None:
        # Connect Map to Parent Widget
        self.parent_widget = parent_widget

        # Retrieve Map Details from file
        self.map = Map(map_file_path)
        self.map_height = self.map.map_height
        self.map_width = self.map.map_width

        # Create Solution FIle
        # self.solution

        # Flags
        self.inside_axes = False

        # Setting up Backend
        matplotlib.use("QTAgg")

        # Initialise Map
        self.fig = Figure(figsize=(100, 100), layout="constrained")
        FigureCanvas.__init__(self, self.fig)
        self.setup_map()
        self.setup_all_event_handlers()

        # Intialise Modes
        self.edit_agent_mode = False
        self.add_agent_mode = False

        # Draw
        self.draw()

    def setup_map(self):
        self.fig.patch.set_facecolor(self.BACKGROUND_COLOR)

        # Set axis font.
        self.ax = self.fig.gca()
        self.ax.set_aspect("equal")
        self.ax.set_axisbelow(True)

        # Hide outside map.
        # self.fig.tight_layout(pad=3.0, w_pad=2.0)

        # Set background color
        self.ax.set_facecolor("white")

        # Set axis range.
        x_min = 0
        y_min = 0
        x_max = self.map_width
        y_max = self.map_height
        # x_step = 5 if x_max <= 50 else 10
        # y_step = 5 if y_max <= 50 else 10

        # if you want to see 1 by 1 grid use these two steps
        x_step = 1
        y_step = 1

        self.ax.set_xlim(x_min, x_max)
        self.ax.set_ylim(y_min, y_max)

        # Shift axis to the middle of each coordinate.
        self.ax.xaxis.set(
            ticks=[i + 0.5 for i in range(0, x_max, x_step)],
        )
        xticklabels = list(range(0, x_max, x_step))
        # Set x tick Labels for x axis for every 5
        if len(xticklabels) > 10:
            for l_index in range(0, len(xticklabels)):
                if not l_index % 5 == 0:
                    xticklabels[l_index] = ""
        self.ax.set_xticklabels(xticklabels, rotation=45)

        self.ax.yaxis.set(
            ticks=[i + 0.5 for i in range(0, y_max, y_step)],
            ticklabels=range(0, y_max, y_step),
        )
        # Reverse vertical axis.
        self.ax.invert_yaxis()

        # Only put tick labels for every 2 or 5 labels
        # def func(x, pos):
        #     if not x % 5:
        #         return "{:g}".format(x)
        #     else:
        #         return ""

        # self.ax.xaxis.set_major_formatter(mticker.FuncFormatter(func))
        # self.fig.setp(self.ax.axes.get_xticklabels(), visible=False)
        # self.fig.setp(self.ax.axes.get_xticklabels()[::5], visible=True)

        # Make make top have ticks and labels for x acis
        self.ax.xaxis.set_tick_params(
            labeltop=True, labelbottom=False, top=True, bottom=False
        )
        # self.ax.xaxis.set_major_locator(mticker.MaxNLocator())
        self.ax.grid(zorder=2)
        # self.ax.xaxis.set_major_locator(mticker.MultipleLocator(5))
        for y in range(self.map_height):
            x_begin = 0
            x_end = self.map_width
            while x_begin < self.map_width:
                if not self.map.map_content[x_begin, y]:
                    for x in range(x_begin + 1, self.map_width):
                        if self.map.map_content[x, y]:
                            x_end = x
                            break
                    self.ax.add_patch(
                        Rectangle(
                            (x_begin, y),
                            x_end - x_begin,
                            1,
                            zorder=3,
                            facecolor=self.OBSTACLE_COLOR,
                            edgecolor="none",
                        )
                    )
                    x_begin = x_end + 1
                else:
                    x_begin += 1

    def setup_all_event_handlers(self):
        self.fig.canvas.mpl_connect("axes_enter_event", self.enter_axes)
        self.fig.canvas.mpl_connect("axes_leave_event", self.leave_axes)
        self.fig.canvas.mpl_connect("button_press_event", self.on_press)
        self.fig.canvas.mpl_connect("motion_notify_event", self.motion_notify)
        self.fig.canvas.mpl_connect("pick_event", self.pick_event)

    def enter_axes(self, event):
        print("Axis Entered", event.canvas.figure)
        self.inside_axes = True
        # Update Location

    def leave_axes(self, event):
        print("Axis Exited", event.canvas.figure)
        # Stop Tracking Location
        self.inside_axes = False

    def on_press(self, event):
        # Check if the Press is inside the Axis
        if self.inside_axes == True:
            print(
                "Click Registered:", round(event.xdata - 0.5), round(event.ydata - 0.5)
            )
            # Re offset the x and y axis

            # if self.

    def motion_notify(self, event):
        if self.inside_axes == True:
            print(
                "Mouse Movement:",
                round(event.xdata - 0.5) if event.xdata != None else "Invalid x",
                round(event.ydata - 0.5) if event.ydata != None else "Invalid y",
            )
            # print(
            #     "Mouse Movement:",
            #     round(event.xdata - 0.5) if event.xdata != None else "Invalid x",
            #     round(event.ydata - 0.5) if event.ydata != None else "Invalid y",
            # )

    def pick_event(self, event):
        pass

    def __add_object(self, event):
        pass
