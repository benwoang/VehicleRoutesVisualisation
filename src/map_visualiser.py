import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.patches import Rectangle

from solver_input import SolverInput
from solution_visualiser import COLORS


class MapVisualiser(QWidget):
    BACKGROUND_COLOR = "#FFFFFF"
    OBSTACLE_COLOR = "#D9D9D9"

    def __init__(self, parent_widget) -> None:
        # Connect Map to Parent Widget
        self.parent_widget = parent_widget

        # Setting up Backend
        matplotlib.use("QTAgg")

        # Initialise Map Figure
        self.fig = Figure(figsize=(60, 20), layout="constrained")
        self.canvas = FigureCanvas(self.fig)
        # self.fig.tight_layout()

        # Create Sovler Input File
        # self.solver_input = SolverInput()
        self.solver_input = SolverInput("31x79-w5.map")
        if self.solver_input != None:  # TODO: change to parent_widget.value !=None
            self.setup_map()

        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)

        # Flags
        self.inside_axes = False
        # Intialise Modes
        self.delete_agent_mode = False
        self.add_agent_mode = False
        self.delete_task_mode = False
        self.add_task_mode = False

        # Draw
        self.canvas.draw_idle()
        self.canvas.flush_events()

    def setup_map(self):
        self.fig.patch.set_facecolor(self.BACKGROUND_COLOR)

        # Set axis font.
        self.ax = self.fig.gca()
        self.ax.set_aspect("equal")
        self.ax.set_axisbelow(True)

        # Hide outside map.
        # self.fig.tight_layout(w_pad=10.0)

        # Set background color
        self.ax.set_facecolor("white")

        # Set axis range.
        x_min = 0
        y_min = 0
        x_max = self.solver_input.map.map_width
        y_max = self.solver_input.map.map_height

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
        self.ax.set_xticklabels(xticklabels)  # , rotation=45)

        self.ax.yaxis.set(
            ticks=[i + 0.5 for i in range(0, y_max, y_step)],
            ticklabels=range(0, y_max, y_step),
        )
        # Reverse vertical axis.
        self.ax.invert_yaxis()

        # Make make top have ticks and labels for x acis
        # self.ax.xaxis.set_tick_params(
        #     labeltop=True, labelbottom=False, top=True, bottom=False
        # )
        # self.ax.grid(zorder=2)

        self.ax.tick_params(
            axis="both",  # changes apply to both axes
            which="both",  # both major and minor ticks are affected
            left=False,  # ticks along the left edge are off
            right=False,  # ticks along the right edge are off
            top=False,  # ticks along the top edge are off
            bottom=False,  # ticks along the bottom edge are off
            labelleft=False,  # labels along the left edge are off
            labelbottom=False,
        )

        # Create Obstacles
        for y in range(self.solver_input.map.map_height):
            x_begin = 0
            x_end = self.solver_input.map.map_width
            while x_begin < self.solver_input.map.map_width:
                if not self.solver_input.map.map_content[x_begin, y]:
                    for x in range(x_begin + 1, self.solver_input.map.map_width):
                        if self.solver_input.map.map_content[x, y]:
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
        self.setup_all_event_handlers()

    def setup_all_event_handlers(self):
        # Connect all map handlers
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
        print("DoubleClick: " + str(event.dblclick))
        if self.inside_axes == True and not event.dblclick:
            # Re offset the x and y axis
            x_display = round(event.xdata - 0.5)
            y_display = round(event.ydata - 0.5)
            print("Click Registered:", x_display, y_display)
            if self.add_agent_mode:
                try:
                    new_agent, new_agent_text = self.solver_input.add_new_agent(
                        x_display, y_display
                    )
                except TypeError:
                    print("Is Obstacle, cannot add agent")
                else:
                    self.ax.add_patch(new_agent)
                    self.ax.add_artist(new_agent_text)

            elif self.add_task_mode:
                try:
                    new_task, new_task_text = self.solver_input.add_new_task(
                        x_display, y_display
                    )
                except TypeError:
                    print("Is Obstacle, cannot add task")
                else:
                    self.ax.add_patch(new_task)
                    self.ax.add_artist(new_task_text)
            self.canvas.draw_idle()
            self.canvas.flush_events()

    def motion_notify(self, event):
        if self.inside_axes == True and event.dblclick == True:
            print(
                "Mouse Movement:",
                round(event.xdata - 0.5) if event.xdata != None else "Invalid x",
                round(event.ydata - 0.5) if event.ydata != None else "Invalid y",
            )

    def pick_event(self, event):
        print("Picked Event")

    def select_mode(self, mode_in, object_in):
        self.reset_modes()
        if object_in == "agents":
            if mode_in == "add":
                print("Add Agent On")
                self.add_agent_mode = True
        elif object_in == "tasks":
            if mode_in == "add":
                self.add_task_mode = True

    def delete_tasks_from_map(self):
        self.solver_input.delete_tasks()
        self.canvas.draw_idle()
        self.canvas.flush_events()

    def delete_agents_from_map(self):
        self.solver_input.delete_agents()
        self.canvas.draw_idle()
        self.canvas.flush_events()

    def reset_modes(self):
        self.add_agent_mode = False
        self.edit_agent_mode = False
        self.add_task_mode = False
        self.edit_agent_mode = False

    def solution(self):
        self.solver_input.generate_text_file()
