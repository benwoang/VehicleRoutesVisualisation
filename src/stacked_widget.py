import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QVBoxLayout,
    QStackedWidget,
    QPushButton,
)
from solution_visualiser import SolutionVisualiser
from map_visualiser import MapVisualiser


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self._main = QWidget()

#         # self.stackedWidget = QStackedWidget()
#         self.setCentralWidget(self._main)
#         layout = QVBoxLayout(self._main)
#         self.fig_can = MapVisualiser("31x79-w5.map")
#         layout.addWidget(self.fig_can)
#         self.button = QPushButton("test", self)
#         layout.addWidget(self.button)


class StackedWidget(QWidget):
    def __init__(self):
        super().__init__()

        # self.stackedWidget = QStackedWidget()
        layout = QVBoxLayout(self)
        self.fig_can = MapVisualiser("31x79-w5.map")
        layout.addWidget(self.fig_can)
        self.button = QPushButton("test", self)
        layout.addWidget(self.button)

    # def create_stacked_widget(self):
    #     self.stackedWidget = QStackedWidget()
    def create_map_page(self):
        pass

    def create_solution_page(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StackedWidget()
    window.show()
    app.exec()
