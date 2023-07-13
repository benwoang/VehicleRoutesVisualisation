import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from solution import Solution


class SolutionVisualiser:
    BACKGROUND_COLOR = "#FAFAFA"
    FIG_SIZE = 4

    def __init__(self, solution_file_path) -> None:
        self.solution = Solution(solution_file_path)
        self.animation = FuncAnimation(
            self.fig,
            self.update,
            init_func=self.init,
            frames=100,
            interval=100,
            blit=True,
        )

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


if __name__ == "__main__":
    solution = SolutionVisualiser("solution.txt")
