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
    QFrame,
    QGridLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QFontDatabase

from solution_visualiser import SolutionVisualiser
from map_visualiser import MapVisualiser


class StackedWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(
            """
            QWidget{
                background-color: #E8EDF0;}
            QPushButton[flat="true"]{
                background-color: #D9D9D9;
                padding-top:2px;
                padding-bottom:2px;
                min-width: 15em;
                max-width:20em;
                background-position: bottom right;
                border-radius:3px;
                font-size: 16px
            }
            QPushButton[flat="true"]:pressed{
                background-color: #808080;
            }
        """
        )
        # Setup base
        self.base_layout = QVBoxLayout()
        self.stackedWidget = QStackedWidget()
        self.base_layout.addWidget(self.stackedWidget)
        self.stackedWidget.addWidget(self.create_map_page())
        self.setLayout(self.base_layout)

    def create_solution_page(self):
        # Create Solver Input File
        self.map_fig_can.solution()
        # Create output Page
        solution_page = QWidget()
        layout = QVBoxLayout(solution_page)

        # Heading
        header_text = QLabel("Solver - Output")
        header_text.setStyleSheet(
            """
            QLabel {  color : #0F2D48; font: bold 36px; max-height:56px;}
            """
        )
        header_text.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
        layout.addWidget(header_text)

        # Animation
        self.fig_can = SolutionVisualiser("solution.txt")
        layout.addWidget(self.fig_can)

        self.stackedWidget.addWidget(solution_page)
        self.stackedWidget.setCurrentIndex(1)

    def create_map_page(self):
        self.map_fig_can = MapVisualiser(self)
        map_page = QWidget()
        layout = QVBoxLayout(map_page)

        ## Heading
        header_text = QLabel("Solver - Input")
        header_text.setStyleSheet(
            """
            QLabel {  color : #0F2D48; font: bold 36px; max-height:56px;}
            """
        )
        header_text.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
        layout.addWidget(header_text)

        ## Mode Control Panel
        mode_control_widget = QWidget()
        mode_control_layout = QGridLayout()
        mode_control_widget.setLayout(mode_control_layout)

        # Agent Header
        agent_header = QLabel("Agents")
        agent_header.setStyleSheet(
            """
            QLabel {  color : #0F2D48; font: bold 24px; max-height:56px;}
            """
        )
        mode_control_layout.addWidget(
            agent_header, 0, 0, 1, 5, Qt.AlignmentFlag.AlignCenter
        )

        # Agent Add Button
        agent_add_button = QPushButton("Add Agents", flat=True)
        agent_add_button.clicked.connect(
            lambda: self.map_fig_can.select_mode("add", "agents")
        )
        mode_control_layout.addWidget(
            agent_add_button, 1, 1, 1, 3, Qt.AlignmentFlag.AlignCenter
        )

        # Agent Delete All Button
        agent_delete_button = QPushButton(
            "Delete All Agents",
            flat=True,
        )
        agent_delete_button.clicked.connect(
            lambda: self.map_fig_can.delete_agents_from_map()
        )
        mode_control_layout.addWidget(
            agent_delete_button, 2, 1, 1, 3, Qt.AlignmentFlag.AlignCenter
        )

        # Task Header
        tasks_header = QLabel("Tasks")
        tasks_header.setStyleSheet(
            """
            QLabel {  color : #0F2D48; font: bold 24px; max-height:56px;}
            """
        )
        mode_control_layout.addWidget(
            tasks_header, 0, 5, 1, 5, Qt.AlignmentFlag.AlignCenter
        )

        # Task Add Button
        task_add_button = QPushButton("Add Tasks", flat=True)
        task_add_button.clicked.connect(
            lambda: self.map_fig_can.select_mode("add", "tasks")
        )
        mode_control_layout.addWidget(
            task_add_button, 1, 6, 1, 3, Qt.AlignmentFlag.AlignCenter
        )

        # Task Delete All Button
        task_delete_button = QPushButton(
            "Delete All Tasks",
            flat=True,
        )
        task_delete_button.clicked.connect(
            lambda: self.map_fig_can.delete_tasks_from_map()
        )
        mode_control_layout.addWidget(
            task_delete_button, 2, 6, 1, 3, Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(mode_control_widget)

        ## Mapping
        layout.addWidget(self.map_fig_can)

        ## Button
        self.button = QPushButton("Solve", self, flat=True)
        self.button.clicked.connect(self.create_solution_page)
        layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignRight)

        return map_page


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StackedWidget()
    window.showMaximized()
    window.show()
    app.exec()
