from PyQt5.QtGui import *
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from GUI.Qt_UI.draw import Ui_loader
import glob
import json

class draw_gui(QLabel):
    def __init__(self, parent=None):
        super(draw_gui, self).__init__(parent)

        self.painter = QPainter()

        self.open_file = None
        # self.write_list = []
        self.preview_data = []

        # 鼠标上个位置点
        self.lastPos = QPoint(0, 0)
        # 鼠标当前点
        self.currentPos = QPoint(0, 0)
        self.flag = False
        self.empty = True
        self.draw = True
        self.previewing = False
        self.mouse_move = False
        self.write_mode = 1

        self.size = QSize(500, 500)
        self.board = QPixmap(self.size)
        self.board.fill(Qt.white)

        self.min_x = 501
        self.min_y = 501
        self.max_x = 0
        self.max_y = 0
        self.rect_X = 0
        self.rect_Y = 0
        self.rect_W = 0
        self.rect_H = 0

    def mousePressEvent(self, mouseEvent):
        if mouseEvent.buttons() == QtCore.Qt.LeftButton and self.draw:
            self.flag = True
            self.empty = False
            self.mouse_move = False
            self.lastPos = mouseEvent.pos()

    def mouseReleaseEvent(self, event):
            self.currentPos = event.pos()

    def mouseMoveEvent(self, mouseEvent):

        if self.flag and mouseEvent.buttons() == QtCore.Qt.LeftButton and self.draw:
            self.mouse_move = True
            self.currentPos = mouseEvent.pos()

    def paintEvent(self, paintEvent):
        super(draw_gui, self).paintEvent(paintEvent)
        self.painter.begin(self)
        self.painter.setPen(QPen(Qt.black, 2))
        self.painter.drawPixmap(0, 0, self.board)
        self.rect_X = min(self.lastPos.x(), self.currentPos.x())
        self.rect_Y = min(self.lastPos.y(), self.currentPos.y())
        self.rect_W = abs(self.lastPos.x() - self.currentPos.x())
        self.rect_H = abs(self.lastPos.y() - self.currentPos.y())
        if self.mouse_move == True:
            self.painter.drawRect(self.rect_X, self.rect_Y, self.rect_W, self.rect_H)
        self.update()
        self.painter.end()

    def load_already_data(self):
        alread_data = QFileDialog.getOpenFileName(self, "Open file", self.open_file)
        load_data_res = False

        if alread_data[0]:
            f = open(alread_data[0], 'r')
            if self.preview_data:
                self.preview_data = []
                # self.preview_data.clear()
            with f as file_to_read:
                while True:
                    lines = file_to_read.readline()
                    if not lines:
                        break
                    item = [i for i in lines.split(",")]
                    point_x = json.loads(item[0])
                    point_y = json.loads(item[1])
                    if (point_x and point_y) >= 0:
                        self.min_x = min(point_x, self.min_x)
                        self.min_y = min(point_y, self.min_y)

                        self.max_x = max(point_x, self.max_x)
                        self.max_y = max(point_y, self.max_y)
                    self.preview_data.append([int(point_x), int(point_y)])
            load_data_res = True
            # self.write_list.append(self.preview_data[:])

        if load_data_res == True:
            load_msg = "加载数据成功"
            load_res = QMessageBox.information(self, "数据加载", load_msg, QMessageBox.Yes, QMessageBox.Yes)

        else:
            QMessageBox.warning(self, "加载失败", "没有正确加载数据", QMessageBox.Yes)
        # print("加载数据成功")

    def preview(self, offect_x=0, offect_y=0, change_size_x=1.0, change_size_y=1.0):
        if self.preview_data:
            self.painter.begin(self.board)
            self.painter.setPen(QPen(Qt.black, 2))
            self.previewing = True
            self.empty = False
            for i in range(len(self.preview_data) - 1):
                point1 = self.preview_data[i]
                point2 = self.preview_data[i+1]
                if (point1[0] and point1[1]) == -1 or (point2[0] and point2[1]) == -1:
                    continue

                self.painter.drawLine((point1[0]+offect_x), (point1[1] + offect_y),
                                      (point2[0]+offect_x), (point2[1] + offect_y))

            self.painter.end()
            self.update()
        else:
            QMessageBox.warning(self, "预览失败", "没有加载数据无法预览", QMessageBox.Yes)

    def choose_size_position(self):

        change_size_x = self.rect_W / (self.max_x - self.min_x)
        change_size_y = self.rect_H / (self.max_y - self.min_y)
        x = self.rect_X - self.min_x
        y = self.rect_Y - self.min_y
        self.clear()
        self.preview(x, y, change_size_x, change_size_y)

    def clear(self):
        self.board.fill(Qt.white)
        self.update()

    def get_file_name(self, button_num):
        if button_num == 1:
            self.open_file = './write_data/'
        if button_num == 2:
            self.open_file = './draw_data/'


class draw_gui_win(QDialog, Ui_loader):

    def __init__(self):
        super(draw_gui_win, self).__init__()
        self.setupUi(self)

        self.button_mode = None
        self.empty = True
        self.previewing = False
        self.preview_data = []

        self.size = QSize(500, 500)

        self.board = QPixmap(self.size)
        self.board.fill(Qt.white)
        self.label = draw_gui(self)

        self.label.setGeometry(QRect(200, 20, 500, 500))
        self.label.setPixmap(self.board)
    def keyPressEvent(self, event):

        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def closeEvent(self, QCloseEvent):
        write_reply = QtWidgets.QMessageBox.question(self,
                                               '退出装载',
                                               "是否要退出装载程序？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if write_reply == QtWidgets.QMessageBox.Yes:
            # self.clear_EditText()

            self.label.clear()
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()

    def load_data(self):
        self.label.load_already_data()

    def choose_size_position(self):
        self.label.choose_size_position()

    def preview(self):
        self.label.preview()

    def execute(self):
        print("执行死刑")

    def clear_preview(self):
        self.label.clear()

    def get_mode(self, mode):
        # self.button_mode = mode
        self.label.get_file_name(mode)
