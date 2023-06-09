# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from UI_QRC import add, less, logo, button
from GUI.Secondary_interface import CustomComboBox

class Ui_Main_GUI(object):
    def setupUi(self, Main_GUI):
        Main_GUI.setObjectName("Main_GUI")
        Main_GUI.resize(1110, 825)
        Main_GUI.setMaximumSize(QtCore.QSize(1110, 825))
        font = QtGui.QFont()
        font.setPointSize(7)
        Main_GUI.setFont(font)
        Main_GUI.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        Main_GUI.setStyleSheet("background-color: qconicalgradient(cx:0, cy:1, angle:231.7, stop:0 rgba(66, 165, 0, 255), stop:1 rgba(255, 255, 255, 255));")
        self.connect = QtWidgets.QPushButton(Main_GUI)
        self.connect.setGeometry(QtCore.QRect(10, 20, 70, 70))
        self.connect.setStyleSheet("background-color: rgb(170, 170, 255);\n"
"color: rgb(255,255,255);  \n"
"border-radius: 30px;\n"
"font: 14pt \"AcadEref\";")
        self.connect.setObjectName("connect")
        self.port_name = CustomComboBox(Main_GUI)
        self.port_name.setGeometry(QtCore.QRect(90, 20, 150, 30))
        self.port_name.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 178, 102, 255), stop:0.55 rgba(235, 148, 61, 255), stop:0.98 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 0));\n"
"border:2px groove gray;\n"
"border-radius:10px;\n"
"padding:2px 4px;")
        self.port_name.setFrame(False)
        self.port_name.setObjectName("port_name")
        self.line = QtWidgets.QFrame(Main_GUI)
        self.line.setGeometry(QtCore.QRect(0, 116, 1200, 21))
        self.line.setMinimumSize(QtCore.QSize(0, 0))
        self.line.setLineWidth(4)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.init = QtWidgets.QPushButton(Main_GUI)
        self.init.setGeometry(QtCore.QRect(250, 20, 70, 70))
        self.init.setStyleSheet("background-color: rgb(0, 170, 255);\n"
"color: rgb(0,255,255);  \n"
"border-radius: 30px; \n"
"font: 14pt \"AcadEref\";")
        self.init.setObjectName("init")
        self.line_2 = QtWidgets.QFrame(Main_GUI)
        self.line_2.setGeometry(QtCore.QRect(325, 0, 21, 121))
        self.line_2.setLineWidth(3)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.logo = QtWidgets.QLabel(Main_GUI)
        self.logo.setGeometry(QtCore.QRect(342, 0, 390, 120))
        self.logo.setAcceptDrops(False)
        self.logo.setStyleSheet("background-image: url(:/gui_logo/logo.jpg);")
        self.logo.setFrameShape(QtWidgets.QFrame.Box)
        self.logo.setText("")
        self.logo.setScaledContents(True)
        self.logo.setObjectName("logo")
        self.line_3 = QtWidgets.QFrame(Main_GUI)
        self.line_3.setGeometry(QtCore.QRect(730, 0, 21, 121))
        self.line_3.setLineWidth(3)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.init0 = QtWidgets.QPushButton(Main_GUI)
        self.init0.setGeometry(QtCore.QRect(770, 20, 70, 70))
        self.init0.setStyleSheet("background-color: rgb(50, 100, 150);\n"
"color: rgb(255,120,60);  \n"
"border-radius: 30px;\n"
"font: 14pt \"AcadEref\";\n"
"")
        self.init0.setObjectName("init0")
        self.end_tool = QtWidgets.QComboBox(Main_GUI)
        self.end_tool.setGeometry(QtCore.QRect(860, 20, 150, 30))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.end_tool.setFont(font)
        self.end_tool.setStyleSheet("background-color: qconicalgradient(cx:0, cy:1, angle:231.7, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
"border:2px groove gray;\n"
"border-radius:10px;\n"
"padding:2px 4px;")
        self.end_tool.setObjectName("end_tool")
        self.end_tool.addItem("")
        self.end_tool.addItem("")
        self.end_tool.addItem("")
        self.urgent_stop = QtWidgets.QPushButton(Main_GUI)
        self.urgent_stop.setGeometry(QtCore.QRect(1020, 20, 70, 70))
        self.urgent_stop.setStyleSheet("background-color: rgb(255, 0, 0);\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(252, 28, 32, 255), stop:1 rgba(255, 255, 255, 255));\n"
"color: rgb(0,0,0);  \n"
"border-radius: 30px;\n"
"font: 14pt \"AcadEref\";")
        self.urgent_stop.setObjectName("urgent_stop")
        self.line_4 = QtWidgets.QFrame(Main_GUI)
        self.line_4.setGeometry(QtCore.QRect(150, 130, 21, 661))
        self.line_4.setLineWidth(3)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.line_5 = QtWidgets.QFrame(Main_GUI)
        self.line_5.setGeometry(QtCore.QRect(730, 130, 21, 661))
        self.line_5.setLineWidth(3)
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.layoutWidget = QtWidgets.QWidget(Main_GUI)
        self.layoutWidget.setGeometry(QtCore.QRect(190, 150, 530, 643))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(20, 20, 20, 20)
        self.gridLayout.setSpacing(20)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_4 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_4.setMinimumSize(QtCore.QSize(150, 180))
        self.pushButton_4.setStyleSheet("background-color: qconicalgradient(cx:0, cy:1, angle:231.7, stop:0 rgba(78, 125, 207, 255), stop:1 rgba(255, 255, 255, 255));\n"
"color: rgb(85,85,0);  \n"
"font: 14pt \"AcadEref\";\n"
"border-style: outset;")
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 1, 0, 1, 1)
        self.pushButton_6 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_6.setMinimumSize(QtCore.QSize(150, 180))
        self.pushButton_6.setStyleSheet("background-color: qconicalgradient(cx:0, cy:1, angle:231.7, stop:0 rgba(78, 125, 207, 255), stop:1 rgba(255, 255, 255, 255));\n"
"color: rgb(85,85,0);  \n"
"font: 14pt \"AcadEref\";\n"
"border-style: outset;")
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout.addWidget(self.pushButton_6, 1, 2, 1, 1)
        self.pushButton_9 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_9.setMinimumSize(QtCore.QSize(150, 180))
        self.pushButton_9.setStyleSheet("background-color: qconicalgradient(cx:0, cy:1, angle:231.7, stop:0 rgba(78, 125, 207, 255), stop:1 rgba(255, 255, 255, 255));\n"
"color: rgb(85,85,0);  \n"
"font: 14pt \"AcadEref\";\n"
"border-style: outset;")
        self.pushButton_9.setObjectName("pushButton_9")
        self.gridLayout.addWidget(self.pushButton_9, 2, 2, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setMinimumSize(QtCore.QSize(150, 180))
        self.pushButton.setStyleSheet("background-color: qconicalgradient(cx:0, cy:1, angle:231.7, stop:0 rgba(78, 125, 207, 255), stop:1 rgba(255, 255, 255, 255));\n"
"color: rgb(85,85,0);  \n"
"font: 14pt \"AcadEref\";\n"
"border-style: outset;")
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)
        self.pushButton_8 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_8.setMinimumSize(QtCore.QSize(150, 180))
        self.pushButton_8.setStyleSheet("background-color: qconicalgradient(cx:0, cy:1, angle:231.7, stop:0 rgba(78, 125, 207, 255), stop:1 rgba(255, 255, 255, 255));\n"
"color: rgb(85,85,0);  \n"
"font: 14pt \"AcadEref\";\n"
"border-style: outset;")
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout.addWidget(self.pushButton_8, 2, 1, 1, 1)
        self.pushButton_7 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_7.setMinimumSize(QtCore.QSize(150, 180))
        self.pushButton_7.setStyleSheet("background-color: qconicalgradient(cx:0, cy:1, angle:231.7, stop:0 rgba(78, 125, 207, 255), stop:1 rgba(255, 255, 255, 255));\n"
"color: rgb(85,85,0);  \n"
"font: 14pt \"AcadEref\";\n"
"border-style: outset;")
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout.addWidget(self.pushButton_7, 2, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(150, 180))
        self.pushButton_2.setStyleSheet("background-color: qconicalgradient(cx:0, cy:1, angle:231.7, stop:0 rgba(78, 125, 207, 255), stop:1 rgba(255, 255, 255, 255));\n"
"color: rgb(85,85,0);  \n"
"font: 14pt \"AcadEref\";\n"
"border-style: outset;")
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 0, 1, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_5.setMinimumSize(QtCore.QSize(150, 180))
        self.pushButton_5.setStyleSheet("background-color: qconicalgradient(cx:0, cy:1, angle:231.7, stop:0 rgba(78, 125, 207, 255), stop:1 rgba(255, 255, 255, 255));\n"
"color: rgb(85,85,0);  \n"
"font: 14pt \"AcadEref\";\n"
"border-style: outset;")
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout.addWidget(self.pushButton_5, 1, 1, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_3.setMinimumSize(QtCore.QSize(150, 180))
        self.pushButton_3.setStyleSheet("background-color: qconicalgradient(cx:0, cy:1, angle:231.7, stop:0 rgba(78, 125, 207, 255), stop:1 rgba(255, 255, 255, 255));\n"
"color: rgb(85,85,0);  \n"
"font: 14pt \"AcadEref\";\n"
"border-style: outset;")
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 0, 2, 1, 1)
        self.port_state = QtWidgets.QLabel(Main_GUI)
        self.port_state.setGeometry(QtCore.QRect(90, 70, 150, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.port_state.setFont(font)
        self.port_state.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(252, 169, 32, 255), stop:1 rgba(255, 255, 255, 255));")
        self.port_state.setAlignment(QtCore.Qt.AlignCenter)
        self.port_state.setObjectName("port_state")
        self.end_tool_state = QtWidgets.QLabel(Main_GUI)
        self.end_tool_state.setGeometry(QtCore.QRect(860, 70, 150, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.end_tool_state.setFont(font)
        self.end_tool_state.setStyleSheet("background-color: qconicalgradient(cx:0, cy:1, angle:231.7, stop:0 rgba(255, 138, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
"color: rgb(255, 50, 90);")
        self.end_tool_state.setAlignment(QtCore.Qt.AlignCenter)
        self.end_tool_state.setObjectName("end_tool_state")
        self.line_6 = QtWidgets.QFrame(Main_GUI)
        self.line_6.setGeometry(QtCore.QRect(0, 180, 150, 3))
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.status_bar = QtWidgets.QLabel(Main_GUI)
        self.status_bar.setGeometry(QtCore.QRect(5, 140, 145, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.status_bar.setFont(font)
        self.status_bar.setAlignment(QtCore.Qt.AlignCenter)
        self.status_bar.setObjectName("status_bar")
        self.line_7 = QtWidgets.QFrame(Main_GUI)
        self.line_7.setGeometry(QtCore.QRect(0, 640, 150, 3))
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.exe_state = QtWidgets.QLabel(Main_GUI)
        self.exe_state.setGeometry(QtCore.QRect(5, 647, 141, 35))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.exe_state.setFont(font)
        self.exe_state.setAlignment(QtCore.Qt.AlignCenter)
        self.exe_state.setObjectName("exe_state")
        self.execute_state = QtWidgets.QLabel(Main_GUI)
        self.execute_state.setGeometry(QtCore.QRect(5, 700, 141, 71))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.execute_state.setFont(font)
        self.execute_state.setAlignment(QtCore.Qt.AlignCenter)
        self.execute_state.setObjectName("execute_state")
        self.control_bar = QtWidgets.QLabel(Main_GUI)
        self.control_bar.setGeometry(QtCore.QRect(757, 140, 181, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.control_bar.setFont(font)
        self.control_bar.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.control_bar.setObjectName("control_bar")
        self.line_8 = QtWidgets.QFrame(Main_GUI)
        self.line_8.setGeometry(QtCore.QRect(757, 180, 345, 6))
        self.line_8.setStyleSheet("")
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.x = QtWidgets.QLabel(Main_GUI)
        self.x.setGeometry(QtCore.QRect(774, 220, 55, 31))
        self.x.setMinimumSize(QtCore.QSize(55, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.x.setFont(font)
        self.x.setAcceptDrops(False)
        self.x.setAutoFillBackground(False)
        self.x.setStyleSheet("color: rgb(255, 0, 0);")
        self.x.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.x.setLineWidth(0)
        self.x.setAlignment(QtCore.Qt.AlignCenter)
        self.x.setObjectName("x")
        self.y = QtWidgets.QLabel(Main_GUI)
        self.y.setGeometry(QtCore.QRect(774, 290, 55, 31))
        self.y.setMinimumSize(QtCore.QSize(55, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.y.setFont(font)
        self.y.setAcceptDrops(False)
        self.y.setAutoFillBackground(False)
        self.y.setStyleSheet("color: rgb(255, 0, 0);")
        self.y.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.y.setLineWidth(0)
        self.y.setAlignment(QtCore.Qt.AlignCenter)
        self.y.setObjectName("y")
        self.z = QtWidgets.QLabel(Main_GUI)
        self.z.setGeometry(QtCore.QRect(774, 360, 55, 31))
        self.z.setMinimumSize(QtCore.QSize(55, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.z.setFont(font)
        self.z.setAcceptDrops(False)
        self.z.setAutoFillBackground(False)
        self.z.setStyleSheet("color: rgb(255, 0, 0);")
        self.z.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.z.setLineWidth(0)
        self.z.setAlignment(QtCore.Qt.AlignCenter)
        self.z.setObjectName("z")
        self.point_x = QtWidgets.QLabel(Main_GUI)
        self.point_x.setGeometry(QtCore.QRect(840, 220, 80, 35))
        self.point_x.setMinimumSize(QtCore.QSize(80, 35))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.point_x.setFont(font)
        self.point_x.setStyleSheet("border:2px groove gray;\n"
"border-radius:10px;\n"
"padding:2px 4px;")
        self.point_x.setAlignment(QtCore.Qt.AlignCenter)
        self.point_x.setObjectName("point_x")
        self.point_y = QtWidgets.QLabel(Main_GUI)
        self.point_y.setGeometry(QtCore.QRect(840, 290, 80, 35))
        self.point_y.setMinimumSize(QtCore.QSize(80, 35))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.point_y.setFont(font)
        self.point_y.setStyleSheet("border:2px groove gray;\n"
"border-radius:10px;\n"
"padding:2px 4px;")
        self.point_y.setAlignment(QtCore.Qt.AlignCenter)
        self.point_y.setObjectName("point_y")
        self.point_z = QtWidgets.QLabel(Main_GUI)
        self.point_z.setGeometry(QtCore.QRect(840, 360, 80, 35))
        self.point_z.setMinimumSize(QtCore.QSize(80, 35))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.point_z.setFont(font)
        self.point_z.setStyleSheet("border:2px groove gray;\n"
"border-radius:10px;\n"
"padding:2px 4px;")
        self.point_z.setAlignment(QtCore.Qt.AlignCenter)
        self.point_z.setObjectName("point_z")
        self.add_x = QtWidgets.QPushButton(Main_GUI)
        self.add_x.setGeometry(QtCore.QRect(940, 210, 60, 60))
        self.add_x.setStyleSheet("color: rgb(0,0,0);  \n"
"font: 14pt \"AcadEref\";\n"
"border-style: outset;\n"
"image: url(:/add_img/add.png);\n"
"border-radius: 30px;  ")
        self.add_x.setText("")
        self.add_x.setObjectName("add_x")
        self.less_x = QtWidgets.QPushButton(Main_GUI)
        self.less_x.setGeometry(QtCore.QRect(1030, 210, 60, 60))
        self.less_x.setStyleSheet("color: rgb(0,0,0);  \n"
"font: 14pt \"AcadEref\";\n"
"border-style: outset;\n"
"image: url(:/less_img/less.png);\n"
"border-radius: 30px; ")
        self.less_x.setText("")
        self.less_x.setObjectName("less_x")
        self.add_y = QtWidgets.QPushButton(Main_GUI)
        self.add_y.setGeometry(QtCore.QRect(940, 280, 60, 60))
        self.add_y.setStyleSheet("color: rgb(0,0,0);  \n"
"font: 14pt \"AcadEref\";\n"
"border-style: outset;\n"
"image: url(:/add_img/add.png);\n"
"border-radius: 30px;")
        self.add_y.setText("")
        self.add_y.setIconSize(QtCore.QSize(16, 16))
        self.add_y.setAutoDefault(False)
        self.add_y.setDefault(False)
        self.add_y.setObjectName("add_y")
        self.less_y = QtWidgets.QPushButton(Main_GUI)
        self.less_y.setGeometry(QtCore.QRect(1030, 280, 60, 60))
        self.less_y.setStyleSheet("color: rgb(0,0,0);  \n"
"font: 14pt \"AcadEref\";\n"
"border-style: outset;\n"
"image: url(:/less_img/less.png);\n"
"border-radius: 30px;")
        self.less_y.setText("")
        self.less_y.setObjectName("less_y")
        self.add_z = QtWidgets.QPushButton(Main_GUI)
        self.add_z.setGeometry(QtCore.QRect(940, 350, 60, 60))
        self.add_z.setStyleSheet("color: rgb(0,0,0);  \n"
"font: 14pt \"AcadEref\";\n"
"border-style: outset;\n"
"image: url(:/add_img/add.png);\n"
"border-radius: 30px; ")
        self.add_z.setText("")
        self.add_z.setObjectName("add_z")
        self.less_z = QtWidgets.QPushButton(Main_GUI)
        self.less_z.setGeometry(QtCore.QRect(1030, 350, 60, 60))
        self.less_z.setStyleSheet("color: rgb(0,0,0);  \n"
"font: 14pt \"AcadEref\";\n"
"border-style: outset;\n"
"image: url(:/less_img/less.png);\n"
"border-radius: 30px;")
        self.less_z.setText("")
        self.less_z.setObjectName("less_z")
        self.add_angle3 = QtWidgets.QPushButton(Main_GUI)
        self.add_angle3.setGeometry(QtCore.QRect(940, 560, 60, 60))
        self.add_angle3.setStyleSheet("color: rgb(0,0,0);  \n"
"font: 14pt \"AcadEref\";\n"
"border-style: outset;\n"
"image: url(:/add_img/add.png);\n"
"border-radius: 30px; ")
        self.add_angle3.setText("")
        self.add_angle3.setObjectName("add_angle3")
        self.angle_2 = QtWidgets.QLabel(Main_GUI)
        self.angle_2.setGeometry(QtCore.QRect(840, 500, 80, 35))
        self.angle_2.setMinimumSize(QtCore.QSize(80, 35))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.angle_2.setFont(font)
        self.angle_2.setStyleSheet("border:2px groove gray;\n"
"border-radius:10px;\n"
"padding:2px 4px;")
        self.angle_2.setAlignment(QtCore.Qt.AlignCenter)
        self.angle_2.setObjectName("angle_2")
        self.less_angle3 = QtWidgets.QPushButton(Main_GUI)
        self.less_angle3.setGeometry(QtCore.QRect(1030, 560, 60, 60))
        self.less_angle3.setStyleSheet("color: rgb(0,0,0);  \n"
"font: 14pt \"AcadEref\";\n"
"border-style: outset;\n"
"image: url(:/less_img/less.png);\n"
"border-radius: 30px; ")
        self.less_angle3.setText("")
        self.less_angle3.setObjectName("less_angle3")
        self.add_angle2 = QtWidgets.QPushButton(Main_GUI)
        self.add_angle2.setGeometry(QtCore.QRect(940, 490, 60, 60))
        self.add_angle2.setStyleSheet("color: rgb(0,0,0);  \n"
"font: 14pt \"AcadEref\";\n"
"border-style: outset;\n"
"image: url(:/add_img/add.png);\n"
"border-radius: 30px;")
        self.add_angle2.setText("")
        self.add_angle2.setObjectName("add_angle2")
        self.less_angle2 = QtWidgets.QPushButton(Main_GUI)
        self.less_angle2.setGeometry(QtCore.QRect(1030, 490, 60, 60))
        self.less_angle2.setStyleSheet("color: rgb(0,0,0);  \n"
"font: 14pt \"AcadEref\";\n"
"border-style: outset;\n"
"image: url(:/less_img/less.png);\n"
"border-radius: 30px;")
        self.less_angle2.setText("")
        self.less_angle2.setObjectName("less_angle2")
        self.angle_1 = QtWidgets.QLabel(Main_GUI)
        self.angle_1.setGeometry(QtCore.QRect(840, 430, 80, 35))
        self.angle_1.setMinimumSize(QtCore.QSize(80, 35))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.angle_1.setFont(font)
        self.angle_1.setStyleSheet("border:2px groove gray;\n"
"border-radius:10px;\n"
"padding:2px 4px;")
        self.angle_1.setObjectName("angle_1")
        self.add_angle1 = QtWidgets.QPushButton(Main_GUI)
        self.add_angle1.setGeometry(QtCore.QRect(940, 420, 60, 60))
        self.add_angle1.setStyleSheet("color: rgb(0,0,0);  \n"
"font: 14pt \"AcadEref\";\n"
"border-style: outset;\n"
"image: url(:/add_img/add.png);\n"
"border-radius: 30px; ")
        self.add_angle1.setText("")
        self.add_angle1.setObjectName("add_angle1")
        self.angle2 = QtWidgets.QLabel(Main_GUI)
        self.angle2.setGeometry(QtCore.QRect(774, 500, 55, 31))
        self.angle2.setMinimumSize(QtCore.QSize(55, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.angle2.setFont(font)
        self.angle2.setAcceptDrops(False)
        self.angle2.setAutoFillBackground(False)
        self.angle2.setStyleSheet("color: rgb(255, 0, 0);")
        self.angle2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.angle2.setLineWidth(0)
        self.angle2.setAlignment(QtCore.Qt.AlignCenter)
        self.angle2.setObjectName("angle2")
        self.less_angle1 = QtWidgets.QPushButton(Main_GUI)
        self.less_angle1.setGeometry(QtCore.QRect(1030, 420, 60, 60))
        self.less_angle1.setStyleSheet("color: rgb(0,0,0);  \n"
"font: 14pt \"AcadEref\";\n"
"border-style: outset;\n"
"image: url(:/less_img/less.png);\n"
"border-radius: 30px; ")
        self.less_angle1.setText("")
        self.less_angle1.setObjectName("less_angle1")
        self.angle_3 = QtWidgets.QLabel(Main_GUI)
        self.angle_3.setGeometry(QtCore.QRect(840, 570, 80, 35))
        self.angle_3.setMinimumSize(QtCore.QSize(80, 35))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.angle_3.setFont(font)
        self.angle_3.setStyleSheet("border:2px groove gray;\n"
"border-radius:10px;\n"
"padding:2px 4px;")
        self.angle_3.setAlignment(QtCore.Qt.AlignCenter)
        self.angle_3.setObjectName("angle_3")
        self.angle3 = QtWidgets.QLabel(Main_GUI)
        self.angle3.setGeometry(QtCore.QRect(774, 570, 55, 31))
        self.angle3.setMinimumSize(QtCore.QSize(55, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.angle3.setFont(font)
        self.angle3.setAcceptDrops(False)
        self.angle3.setAutoFillBackground(False)
        self.angle3.setStyleSheet("color: rgb(255, 0, 0);")
        self.angle3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.angle3.setLineWidth(0)
        self.angle3.setAlignment(QtCore.Qt.AlignCenter)
        self.angle3.setObjectName("angle3")
        self.angle1 = QtWidgets.QLabel(Main_GUI)
        self.angle1.setGeometry(QtCore.QRect(774, 430, 55, 31))
        self.angle1.setMinimumSize(QtCore.QSize(55, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.angle1.setFont(font)
        self.angle1.setAcceptDrops(False)
        self.angle1.setAutoFillBackground(False)
        self.angle1.setStyleSheet("color: rgb(255, 0, 0);")
        self.angle1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.angle1.setLineWidth(0)
        self.angle1.setAlignment(QtCore.Qt.AlignCenter)
        self.angle1.setObjectName("angle1")
        self.line_9 = QtWidgets.QFrame(Main_GUI)
        self.line_9.setGeometry(QtCore.QRect(757, 650, 345, 3))
        self.line_9.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.control_tool = QtWidgets.QLabel(Main_GUI)
        self.control_tool.setGeometry(QtCore.QRect(760, 660, 345, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.control_tool.setFont(font)
        self.control_tool.setAlignment(QtCore.Qt.AlignCenter)
        self.control_tool.setObjectName("control_tool")
        self.up = QtWidgets.QCheckBox(Main_GUI)
        self.up.setGeometry(QtCore.QRect(780, 700, 80, 80))
        self.up.setStyleSheet("background-color: rgb(255, 0, 0);\n"
"color: rgb(0,0,255);  \n"
"font: 14pt \"AcadEref\";\n"
"border-style: outset;\n"
"border-radius: 30px;")
        self.up.setObjectName("up")
        self.down = QtWidgets.QCheckBox(Main_GUI)
        self.down.setGeometry(QtCore.QRect(1000, 700, 80, 80))
        self.down.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.down.setStyleSheet("background-color: rgb(0, 0, 255);\n"
"color: rgb(255,0,0);  \n"
"font: 14pt \"AcadEref\";\n"
"border-style: outset;\n"
"border-radius: 30px; ")
        self.down.setInputMethodHints(QtCore.Qt.ImhNone)
        self.down.setObjectName("down")
        self.layoutWidget1 = QtWidgets.QWidget(Main_GUI)
        self.layoutWidget1.setGeometry(QtCore.QRect(0, 190, 155, 441))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setContentsMargins(9, 10, 0, 0)
        self.verticalLayout.setSpacing(16)
        self.verticalLayout.setObjectName("verticalLayout")
        self.arm_state = QtWidgets.QLabel(self.layoutWidget1)
        self.arm_state.setMinimumSize(QtCore.QSize(145, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.arm_state.setFont(font)
        self.arm_state.setAlignment(QtCore.Qt.AlignCenter)
        self.arm_state.setObjectName("arm_state")
        self.verticalLayout.addWidget(self.arm_state)
        self.mpu1 = QtWidgets.QLabel(self.layoutWidget1)
        self.mpu1.setMinimumSize(QtCore.QSize(145, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.mpu1.setFont(font)
        self.mpu1.setAlignment(QtCore.Qt.AlignCenter)
        self.mpu1.setObjectName("mpu1")
        self.verticalLayout.addWidget(self.mpu1)
        self.mpu2 = QtWidgets.QLabel(self.layoutWidget1)
        self.mpu2.setMinimumSize(QtCore.QSize(145, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.mpu2.setFont(font)
        self.mpu2.setAlignment(QtCore.Qt.AlignCenter)
        self.mpu2.setObjectName("mpu2")
        self.verticalLayout.addWidget(self.mpu2)
        self.tool = QtWidgets.QLabel(self.layoutWidget1)
        self.tool.setMinimumSize(QtCore.QSize(145, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.tool.setFont(font)
        self.tool.setAlignment(QtCore.Qt.AlignCenter)
        self.tool.setObjectName("tool")
        self.verticalLayout.addWidget(self.tool)
        self.exchange = QtWidgets.QLabel(self.layoutWidget1)
        self.exchange.setMinimumSize(QtCore.QSize(145, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.exchange.setFont(font)
        self.exchange.setAlignment(QtCore.Qt.AlignCenter)
        self.exchange.setObjectName("exchange")
        self.verticalLayout.addWidget(self.exchange)
        self.control = QtWidgets.QCheckBox(Main_GUI)
        self.control.setGeometry(QtCore.QRect(860, 140, 71, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.control.setFont(font)
        self.control.setStyleSheet("QCheckBox{\n"
"    border-radius: 10px\n"
"}\n"
"QCheckBox::indicator:unchecked{\n"
"    image: url(:/close_img/close.png);\n"
"}\n"
"QCheckBox::indicator:checked{\n"
"    image: url(:/open_img/open.png);\n"
"}")
        self.control.setText("")
        self.control.setChecked(False)
        self.control.setTristate(False)
        self.control.setObjectName("control")
        self.control_bar_2 = QtWidgets.QLabel(Main_GUI)
        self.control_bar_2.setGeometry(QtCore.QRect(940, 140, 161, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.control_bar_2.setFont(font)
        self.control_bar_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.control_bar_2.setObjectName("control_bar_2")
        self.limit = QtWidgets.QLineEdit(Main_GUI)
        self.limit.setGeometry(QtCore.QRect(1040, 140, 51, 40))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.limit.setFont(font)
        self.limit.setAlignment(QtCore.Qt.AlignCenter)
        self.limit.setObjectName("limit")

        self.retranslateUi(Main_GUI)
        #self.port_name.setCurrentIndex(-1)
        self.connect.clicked.connect(Main_GUI.connect_arm)
        self.init.clicked.connect(Main_GUI.initialization)
        self.init0.clicked.connect(Main_GUI.initialization)
        self.urgent_stop.clicked.connect(Main_GUI.arm_stop)

        self.port_name.currentTextChanged.connect(Main_GUI.port_imf)
        self.end_tool.currentTextChanged.connect(Main_GUI.use_tool)

        self.up.stateChanged.connect(Main_GUI.tool_state)
        self.down.stateChanged.connect(Main_GUI.tool_state)
        self.control.stateChanged.connect(Main_GUI.gui_control)

        self.add_x.clicked.connect(lambda: Main_GUI.add_point(1))
        self.add_y.clicked.connect(lambda: Main_GUI.add_point(2))
        self.add_z.clicked.connect(lambda: Main_GUI.add_point(3))
        self.less_x.clicked.connect(lambda: Main_GUI.less_point(1))
        self.less_y.clicked.connect(lambda: Main_GUI.less_point(2))
        self.less_z.clicked.connect(lambda: Main_GUI.less_point(3))

        self.add_angle1.clicked.connect(lambda: Main_GUI.add_angle(1))
        self.add_angle2.clicked.connect(lambda: Main_GUI.add_angle(2))
        self.add_angle3.clicked.connect(lambda: Main_GUI.add_angle(3))
        self.less_angle1.clicked.connect(lambda: Main_GUI.less_angle(1))
        self.less_angle2.clicked.connect(lambda: Main_GUI.less_angle(2))
        self.less_angle3.clicked.connect(lambda: Main_GUI.less_angle(3))

        self.pushButton.clicked.connect(Main_GUI.teach)
        self.pushButton_2.clicked.connect(Main_GUI.memory_teach)
        self.pushButton_3.clicked.connect(Main_GUI.execute_script)
        self.pushButton_4.clicked.connect(Main_GUI.check_reboot)
        self.pushButton_5.clicked.connect(Main_GUI.draw)
        self.pushButton_6.clicked.connect(Main_GUI.write)
        self.pushButton_7.clicked.connect(Main_GUI.expand)
        self.pushButton_8.clicked.connect(Main_GUI.open_draw_board)
        self.pushButton_9.clicked.connect(Main_GUI.open_write_board)
        QtCore.QMetaObject.connectSlotsByName(Main_GUI)

    def retranslateUi(self, Main_GUI):
        _translate = QtCore.QCoreApplication.translate
        Main_GUI.setWindowTitle(_translate("Main_GUI", "HG_DR_GUI-V1.1"))
        self.connect.setText(_translate("Main_GUI", "连接"))
        self.init.setText(_translate("Main_GUI", "初始化"))
        self.init0.setText(_translate("Main_GUI", "回零"))
        self.end_tool.setItemText(0, _translate("Main_GUI", "不使用"))
        self.end_tool.setItemText(1, _translate("Main_GUI", "气泵"))
        self.end_tool.setItemText(2, _translate("Main_GUI", "笔"))
        self.urgent_stop.setText(_translate("Main_GUI", "急停"))
        self.pushButton_4.setText(_translate("Main_GUI", "自检重启"))
        self.pushButton_6.setText(_translate("Main_GUI", "写字"))
        self.pushButton_9.setText(_translate("Main_GUI", "打开写板"))
        self.pushButton.setText(_translate("Main_GUI", "示教"))
        self.pushButton_8.setText(_translate("Main_GUI", "打开画板"))
        self.pushButton_7.setText(_translate("Main_GUI", "扩展"))
        self.pushButton_2.setText(_translate("Main_GUI", "记忆示教"))
        self.pushButton_5.setText(_translate("Main_GUI", "画画"))
        self.pushButton_3.setText(_translate("Main_GUI", "执行脚本"))
        self.port_state.setText(_translate("Main_GUI", "未连接串口"))
        self.end_tool_state.setText(_translate("Main_GUI", "未选择末端器具"))
        self.status_bar.setText(_translate("Main_GUI", "状态栏"))
        self.exe_state.setText(_translate("Main_GUI", "执行状态"))
        self.execute_state.setText(_translate("Main_GUI", "未执行"))
        self.control_bar.setText(_translate("Main_GUI", " 操控面板"))
        self.x.setText(_translate("Main_GUI", "X:"))
        self.y.setText(_translate("Main_GUI", "Y:"))
        self.z.setText(_translate("Main_GUI", "Z:"))
        self.point_x.setText(_translate("Main_GUI", "0.0000"))
        self.point_y.setText(_translate("Main_GUI", "0.0000"))
        self.point_z.setText(_translate("Main_GUI", "0.0000"))
        self.angle_2.setText(_translate("Main_GUI", "0.0000"))
        self.angle_1.setText(_translate("Main_GUI", "0.0000"))
        self.angle2.setText(_translate("Main_GUI", "角度二:"))
        self.angle_3.setText(_translate("Main_GUI", "0.000"))
        self.angle3.setText(_translate("Main_GUI", "角度三"))
        self.angle1.setText(_translate("Main_GUI", "角度一:"))
        self.control_tool.setText(_translate("Main_GUI", "控制末端器具"))
        self.up.setText(_translate("Main_GUI", "使能"))
        self.down.setText(_translate("Main_GUI", "不使能"))
        self.arm_state.setText(_translate("Main_GUI", "未开机"))
        self.mpu1.setText(_translate("Main_GUI", "传感器1未知"))
        self.mpu2.setText(_translate("Main_GUI", "传感器2未知"))
        self.tool.setText(_translate("Main_GUI", "末端器具未知"))
        self.exchange.setText(_translate("Main_GUI", "通讯未知"))
        self.control_bar_2.setText(_translate("Main_GUI", "  限位角度"))
        self.limit.setText(_translate("Main_GUI", "5"))

