import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout
from solution_visualiser import SolutionVisualiser


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._main = QWidget()
        self.setCentralWidget(self._main)
        layout = QHBoxLayout(self._main)
        self.fig_can = SolutionVisualiser("solution_simple.txt")
        layout.addWidget(self.fig_can)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
