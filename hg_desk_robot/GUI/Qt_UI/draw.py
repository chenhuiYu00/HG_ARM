# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'draw.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_loader(object):
    def setupUi(self, loader):
        loader.setObjectName("loader")
        loader.resize(729, 541)
        self.label = QtWidgets.QLabel(loader)
        self.label.setGeometry(QtCore.QRect(200, 20, 500, 500))
        self.label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label.setAutoFillBackground(True)
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label.setWordWrap(False)
        self.label.setOpenExternalLinks(False)
        self.label.setObjectName("label")
        self.layoutWidget = QtWidgets.QWidget(loader)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 21, 152, 426))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setMinimumSize(QtCore.QSize(150, 80))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_4 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_4.setMinimumSize(QtCore.QSize(150, 80))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout.addWidget(self.pushButton_4)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(150, 80))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.pushButton_5 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_5.setMinimumSize(QtCore.QSize(150, 80))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout.addWidget(self.pushButton_5)
        self.pushButton_3 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_3.setMinimumSize(QtCore.QSize(150, 80))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)

        self.retranslateUi(loader)
        self.pushButton.clicked.connect(loader.load_data)
        self.pushButton_2.clicked.connect(loader.choose_size_position)
        self.pushButton_3.clicked.connect(loader.execute)
        self.pushButton_4.clicked.connect(loader.preview)
        self.pushButton_5.clicked.connect(loader.clear_preview)
        QtCore.QMetaObject.connectSlotsByName(loader)

    def retranslateUi(self, loader):
        _translate = QtCore.QCoreApplication.translate
        loader.setWindowTitle(_translate("loader", "装载"))
        self.label.setText(_translate("loader", "TextLabel"))
        self.pushButton.setText(_translate("loader", "加载已有数据"))
        self.pushButton_4.setText(_translate("loader", "预览"))
        self.pushButton_2.setText(_translate("loader", "选择位置和大小"))
        self.pushButton_5.setText(_translate("loader", "清除当前预览"))
        self.pushButton_3.setText(_translate("loader", "执行"))

        self.pushButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_5.setFocusPolicy(QtCore.Qt.NoFocus)