import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QPushButton,
    QLabel,
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
        # Setup base
        self.base_layout = QVBoxLayout()
        self.stackedWidget = QStackedWidget()
        self.base_layout.addWidget(self.stackedWidget)
        self.stackedWidget.addWidget(self.create_map_page())
        self.stackedWidget.addWidget(self.create_solution_page())
        # layout = QVBoxLayout()
        # self.fig_can = MapVisualiser("31x79-w5.map")
        self.button = QPushButton("switch", self)
        self.button.clicked.connect(self.switch_layout)
        self.base_layout.addWidget(self.button)

        # layout.addWidget(self.button)
        self.setLayout(self.base_layout)
        self.stackedWidget.setCurrentIndex(1)

    def create_map_page(self):
        map_page = QWidget()
        layout = QVBoxLayout(map_page)
        self.fig_can = MapVisualiser("31x79-w5.map")
        layout.addWidget(self.fig_can)
        self.button = QPushButton("Print", self)
        self.button.clicked.connect(self.switch_layout)
        layout.addWidget(self.button)
        return map_page

    def create_solution_page(self):
        solution_page = QWidget()
        layout = QVBoxLayout(solution_page)
        label = QLabel("My text")
        layout.addWidget(label)
        return solution_page

    def switch_layout(self):
        if self.stackedWidget.currentIndex() == 0:
            self.stackedWidget.setCurrentIndex(1)
        else:
            self.stackedWidget.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StackedWidget()
    window.show()
    app.exec()
