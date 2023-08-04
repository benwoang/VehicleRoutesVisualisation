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
    QSpacerItem,
    QSizePolicy,
    QStyle,
    QGraphicsOpacityEffect,
    QDialog,
    QDialogButtonBox,
    QMessageBox,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject, QSize, QTimer
from PyQt6.QtGui import QFont, QFontDatabase, QMovie

from solution_visualiser import SolutionVisualiser
from map_visualiser import MapVisualiser

import time


class StackedWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(
            """
            QWidget{
                background-color: white;
            }
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

    def create_map_page(self):
        self.map_fig_can = MapVisualiser(self)
        self.map_page = QWidget()
        layout = QVBoxLayout(self.map_page)

        ## Heading
        header_text = QLabel("Multi-Robot Pickup and Delivery")
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
        agent_header = QLabel("Robots")
        agent_header.setStyleSheet(
            """
            QLabel {  color : #0F2D48; font: bold 24px; max-height:56px;}
            """
        )
        mode_control_layout.addWidget(
            agent_header, 0, 0, 1, 5, Qt.AlignmentFlag.AlignCenter
        )

        # Agent Add Button
        agent_add_button = QPushButton("Add Robots", flat=True)
        agent_add_button.clicked.connect(
            lambda: self.map_fig_can.select_mode("add", "agents")
        )
        mode_control_layout.addWidget(
            agent_add_button, 1, 1, 1, 3, Qt.AlignmentFlag.AlignCenter
        )

        # Agent Delete All Button
        agent_delete_button = QPushButton(
            "Delete All Robots",
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
        map_choice = QWidget()
        map_choice_layout = QGridLayout()
        map_choice.setLayout(map_choice_layout)

        print("Map Page Stacked Widget COunt: " + str(self.stackedWidget.count()))

        self.button_exist = QPushButton("Show Previous Paths", self, flat=True)
        self.button_exist.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.button_exist.setVisible(False)  # Hide until a solution is made
        map_choice_layout.addWidget(
            self.button_exist, 0, 3, 1, 1  # , alignment=Qt.AlignmentFlag.AlignRight
        )

        self.button_solve = QPushButton("Calculate New Paths", self, flat=True)
        self.button_solve.clicked.connect(self.create_solution_page)
        map_choice_layout.addWidget(
            self.button_solve, 0, 4, 1, 1  # , alignment=Qt.AlignmentFlag.AlignRight
        )
        layout.addWidget(map_choice)

        return self.map_page

    def create_solution_page(self):
        # self.create_error_message("Can't do that", "Add 1 or more items")
        print("Solution Page Count: " + str(self.stackedWidget.count()))
        self.button_exist.setVisible(True)
        if self.stackedWidget.count() > 1:
            # if both are in remove map which is the last one and recreate it
            self.fig_can.close_event()
            self.stackedWidget.removeWidget(self.solution_page)
        # Create Solver Input File
        self.map_fig_can.solution()

        # TODO: Add Loading Page Here
        # self.stackedWidget.addWidget(self.create_loading_page())
        # self.stackedWidget.setCurrentIndex(1)
        # self.create_loading_page()
        # self.thread = QThread()

        # TODO: EDDIE INSERT CALL TO SOLVER

        # TODO: Remove Loading PAger here

        # Create output Page
        self.solution_page = QWidget()
        layout = QVBoxLayout(self.solution_page)

        # Heading
        header_text = QLabel("Multi-Robot Pickup and Delivery")
        header_text.setStyleSheet(
            """
            QLabel {  color : #0F2D48; font: bold 36px; max-height:56px;}
            """
        )
        header_text.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
        layout.addWidget(header_text)

        # Player
        player = QWidget()
        player_layout = QHBoxLayout()
        player.setLayout(player_layout)

        self.fig_can = SolutionVisualiser("solution.txt")  # TODO: SOLVER OUTPUT INSERT
        self.fig_can.resize(self.map_page.width(), self.map_page.height())

        ## Buttons
        # self.play_button = QPushButton("Play", self, flat=True)
        # self.play_button.clicked.connect(self.fig_can.resume)
        # self.play_button.setIcon(
        #     self.style().standardIcon(getattr(QStyle.StandardPixmap, "SP_MediaPlay"))
        # )
        # player_layout.addWidget(self.play_button)
        # self.pause_button = QPushButton("Pause", self, flat=True)
        # self.pause_button.clicked.connect(self.fig_can.pause)
        # self.pause_button.setIcon(
        #     self.style().standardIcon(getattr(QStyle.StandardPixmap, "SP_MediaPause"))
        # )
        # player_layout.addWidget(self.pause_button)
        layout.addWidget(player)

        # Spacer
        layout.addSpacing(50)

        # Animation
        layout.addWidget(self.fig_can)

        ##BUttons
        self.button = QPushButton("Back", self, flat=True)
        self.button.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignRight)

        self.stackedWidget.addWidget(self.solution_page)
        self.stackedWidget.setCurrentIndex(1)

    def create_loading_page(self):
        self.loading = QWidget()
        self.loading.setMinimumSize(self.screen().size())
        # self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # self.loading.setSizePolicy(
        #     QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        # )
        self.loading.setStyleSheet("background-color:#80808080;")  # Opacity
        # self.loading.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # self.loading.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        # self.loading.setGraphicsEffect(QGraphicsOpacityEffect(opacity=0.5))
        # self.loading.setWindowOpacity(0.4)
        loading_layout = QVBoxLayout()
        loading_layout.setContentsMargins(0, 0, 0, 0)
        loading_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading.setLayout(loading_layout)
        gif_label = QLabel()
        loading_gif = QMovie("./graphics/loading.gif")
        loading_gif.setScaledSize(
            QSize(80, 80)
        )  # No need for setMaximumsize or set scaled contents
        gif_label.setMovie(loading_gif)
        loading_gif.start()
        gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # gif_label.setGraphicsEffect(QGraphicsOpacityEffect(opacity=1))
        gif_label.setStyleSheet("background-color:transparent")
        loading_layout.addWidget(gif_label)

        # Solving Label
        self.loading_text = QLabel("Solving...")
        self.loading_text.setStyleSheet("font-size: 20pt;background-color:transparent;")
        self.loading_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.loading_text.setGraphicsEffect(QGraphicsOpacityEffect(opacity=1))
        loading_layout.addWidget(self.loading_text)

        # Timer Label
        self.timer_label = QLabel()
        self.current_time = 0
        self.timer = QTimer()
        self.timer.start(100)  # 100ms
        self.timer.timeout.connect(self.timer_update)
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setStyleSheet("background-color:transparent;")
        # self.timer_label.setGraphicsEffect(QGraphicsOpacityEffect(opacity=1))
        loading_layout.addWidget(self.timer_label)
        self.base_layout.addChildWidget(self.loading)

        # self.loading.show()
        # self.loading.activateWindow()
        # self.loading.raise_()
        # return self.loading

    def timer_update(self):
        self.current_time = round(self.current_time + 0.1, 1)
        # if self.current_time % 1 == 0:
        #     # Make sure only update every whole second
        #     if self.current_time % 3 == 0:
        #         self.loading_text.setText("Solving.  ")
        #     elif self.current_time % 3 == 1:
        #         self.loading_text.setText("Solving.. ")
        #     elif self.current_time % 3 == 2:
        #         self.loading_text.setText("Solving...")
        self.timer_label.setText("Time Elapsed: " + str(self.current_time))

    def create_error_message(self, message_title_text, message_infomative_text):
        self.error_dialog = QMessageBox(self)
        self.error_dialog.setIcon(QMessageBox.Icon.Warning)
        self.error_dialog.setWindowTitle("Warning")
        self.error_dialog.setText(message_title_text)
        self.error_dialog.setInformativeText(message_infomative_text)
        # self.message_label = QLabel(message_text)
        # self.error_dialog.layout().addWidget(self.message_label)
        # self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        # self.error_dialog.layout().addWidget(self.buttonBox)
        self.error_dialog.exec()


class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    # TODO: PUT EDDIE CODE HERE IN run()

    def run(self):
        """Long-running task."""
        for i in range(5):
            # sleep(1)
            self.progress.emit(i + 1)
        self.finished.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StackedWidget()
    window.setWindowTitle("Multi-Robot Path Finding - Pickup and Delivery")
    window.showMaximized()
    window.show()
    app.exec()
