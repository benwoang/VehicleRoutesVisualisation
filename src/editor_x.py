# Form implementation generated from reading ui file 'QT_UI_Designs\editor.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

import math
import sys
from matplotlib.patches import Rectangle
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from PyQt6 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

FIG_SIZE = 4
OBSTACLE_COLOR = '#D9D9D9'
BACKGROUND_COLOR = '#FAFAFA'

class EditorPlot(FigureCanvas):
    
    def __init__(self,parent,map,map_width, map_height) -> None:
        self.map_height = map_height
        self.map_width = map_width
        self.map = map
        aspect = map_width / map_height
        self.fig = plt.figure(figsize=(FIG_SIZE * aspect, FIG_SIZE))
        self.connect()
        plt.tight_layout(pad=1.0)
        self.plotGraph()
        plt.show()
        super(EditorPlot, self).__init__(self.fig)
        
    
    def plotGraph(self):
        ax = plt.gca()
        # Set background color
        ax.set_facecolor('white')

        # Set axis range.
        x_min = 0
        y_min = 0
        x_max = self.map_width
        y_max = self.map_height
        x_step = 5 if x_max <= 50 else 10
        y_step = 5 if y_max <= 50 else 10
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)

        # Shift axis to the middle of each coordinate.
        ax.xaxis.set(ticks=[i + 0.5 for i in range(0, x_max, x_step)], ticklabels=range(0, x_max, x_step))
        ax.yaxis.set(ticks=[i + 0.5 for i in range(0, y_max, y_step)], ticklabels=range(0, y_max, y_step))

        # Hide major tick labels.
        # ax.set_xticklabels('')
        # ax.set_yticklabels('')

        # Hide ticks
        ax.tick_params(axis='both',       # changes apply to both axes
                    which='both',      # both major and minor ticks are affected
                    left=False,        # ticks along the left edge are off
                    right=False,       # ticks along the right edge are off
                    top=False,         # ticks along the top edge are off
                    bottom=False,      # ticks along the bottom edge are off
                    labelleft=False,   # labels along the left edge are off
                    labelbottom=False) # labels along the bottom edge are off

        # Customize minor tick labels.
        # ax.set_xticks([i + 0.5 for i in range(0, x_max, x_step)], minor=True)
        # ax.set_xticklabels(range(0, x_max, x_step), minor=True)

        # Reverse vertical axis.
        ax.invert_yaxis()

                # Draw obstacles.
        for y in range(self.map_height):
            x_begin = 0
            while x_begin < self.map_width:
                if not self.map[x_begin, y]:
                    x_end = self.map_width
                    for x in range(x_begin + 1, self.map_width):
                        if  self.map[x, y]:
                            x_end = x
                            break
                    ax.add_patch(Rectangle((x_begin, y), x_end - x_begin, 1, zorder=-2, facecolor=OBSTACLE_COLOR, edgecolor='none'))
                    x_begin = x_end + 1
                else:
                    x_begin += 1
    
    def connect(self):
        print("connect!")
        self.cidpress = self.fig.canvas.mpl_connect(
            'button_press_event', self.on_press)
    def on_press(self, event):
        print("clicked!")
        print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))
    def disconnect(self):
        self.fig.canvas.mpl_disconnect(self.cidpress)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 546)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pbSolve = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pbSolve.setGeometry(QtCore.QRect(710, 110, 75, 24))
        self.pbSolve.setObjectName("pbSolve")
        self.pbLoadMap = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pbLoadMap.setGeometry(QtCore.QRect(630, 110, 75, 24))
        self.pbLoadMap.setObjectName("pbLoadMap")
        self.gridLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(630, 20, 160, 84))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 1, 1, 1)
        self.label = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        #Plot
        self.intialiseGraph()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    def intialiseGraph(self):
        # matplotlib.rcParams['toolbar'] = 'None'
        map_file = '31x79-w5.map'
        map = self.read_map(map_file)
        map_width = map.shape[0]
        map_height = map.shape[1]

        matplotlib.use('Qt5Agg')

        self.plot = EditorPlot(self.centralwidget,map,map_width,map_height)
        # self.plot.setObjectName("widgetPlot")

        self.plotContainer= QtWidgets.QVBoxLayout()
        self.plotContainer.addWidget(self.plot)
        self.plotContainer.setGeometry(QtCore.QRect(20, 20, 20+map_height, 441+map_width))
    
    def read_map(self,map_file):
        f = open("./SampleData/"+map_file, 'r')
        lines = f.read().splitlines()
        f.close()

        l = 0
        while lines[l] != 'map':
            l += 1
        l += 1

        map = []
        y = 0
        for line in lines[l:]:
            row = []
            for (x, c) in enumerate(line):  
                row.append(c == '.')
            y += 1
            map.append(row)

        map2 = np.array(map).transpose()
        return map2

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pbSolve.setText(_translate("MainWindow", "Solve"))
        self.pbLoadMap.setText(_translate("MainWindow", "Load Map"))
        self.label_2.setText(_translate("MainWindow", "Y Position"))
        self.label_4.setText(_translate("MainWindow", "X Position"))
        self.label_3.setText(_translate("MainWindow", "0"))
        self.label.setText(_translate("MainWindow", "0"))



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())