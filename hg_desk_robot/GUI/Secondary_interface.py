# -*- coding:utf8 -*-
#!/usr/bin/python

from PyQt5.QtGui import *
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import GUI.Qt_UI.draw_board
from GUI.Qt_UI.write_board import Ui_Dialog
from GUI.Qt_UI.draw import Ui_loader
import serial
import serial.tools.list_ports
import glob
import json
from SDK.HG_DR_SDK import HG_DR_SDK
'''
重写QLabel
相同参数共用, 不同参数写入不同初始化函数中
根据不同模式调用不同初始化函数
共用相似的函数, 函数内部相关实现根据模式判断
'''

class Secondary_interface(QLabel):

    # 模式选择 根据模式调用不同初始化函数
    label_mode = 0

    # 共用参数写出来, 不同参数写到不同初始化函数中
    def __init__(self, parent=None):
        super(Secondary_interface, self).__init__(parent)

        # 写入文件的列表
        # 列表的数据由多个step_list组成
        self.point_list = []

        # 单次列表, 存储一笔的点
        self.step_list = []

        # 撤销列表
        self.clear_list = []

        # 预览数据
        self.preview_data = []

        # 鼠标摁下判断 默认为空
        self.flag = False

        # 鼠标移动  默认为对
        self.mouse_move = True

        # label默认为空
        self.empty = True

        # 是否预览 默认为否
        self.previewing = False

        # 选择模式判断
        self.load_mode = Secondary_interface.label_mode
        print(self.load_mode)
        # 鼠标上个位置点
        self.lastPos = QPoint(0, 0)

        # 鼠标当前点
        self.currentPos = QPoint(0, 0)

        # 初始化画板参数
        self.size = QSize(500, 500)
        self.board = QPixmap(self.size)
        self.board.fill(Qt.white)
        self.painter = QPainter()

        if self.load_mode == 1:
            self.DrawInit()
            self.data_dir = './draw_data/'
            self.img_dir = './draw_img/'
            self.path_file_num = glob.glob(pathname='./draw_data/*.txt')
            self.file_total = len(self.path_file_num)
        elif self.load_mode == 2:
            self.data_dir = './write_data/'
            self.path_file_num = glob.glob(pathname='./write_data/*.txt')
            self.file_total = len(self.path_file_num)
            self.img_dir = './write_img/'
            self.WriteInit()
        elif self.load_mode == 3:
            self.LoaderInit()
            self.data_dir = './draw_data/'
            self.img_dir = './draw_img/'
        elif self.load_mode == 4:
            self.LoaderInit()
            self.data_dir = './write_data/'
            self.img_dir = './write_img/'

    # 画图初始化函数
    def DrawInit(self):
        # 大小
        self.draw_type = 2

        # 默认实线 画笔 橡皮大小
        self.linethickness = 1
        self.linestyle = 1
        self.erasersize = 1

        # 记录笔和橡皮参数的变换
        self.linethickness_list = []
        self.linestyle_list = []
        self.erasersize_list = []

        # 使用画笔 橡皮   默认使用笔 不使用橡皮
        self.use_pen = True
        self.use_eraser = False

    # 写字初始化函数
    def WriteInit(self):

        self.write_file_num = glob.glob(pathname='./write_data/*.txt')  # 获取当前文件夹下个数
        self.write_file_total = len(self.write_file_num)

        self.get_point_type = 1

        # 书写风格 连笔 - 2  多笔 - 1 默认多笔
        self.write_mode = 1

    # 装载初始化
    def LoaderInit(self):

        self.min_x = 501
        self.min_y = 501
        self.max_x = 0
        self.max_y = 0
        self.rect_X = 0
        self.rect_Y = 0
        self.rect_W = 0
        self.rect_H = 0

        self.loader_mouse_move = False


    # 重写鼠标点击
    def mousePressEvent(self, mouseEvent):
        if mouseEvent.buttons() == QtCore.Qt.LeftButton and self.mouse_move:
            self.flag = True
            self.empty = False
            if self.load_mode == 3 or self.load_mode == 4:
                self.loader_mouse_move = False
                self.lastPos = mouseEvent.pos()
            else:
                self.currentPos = mouseEvent.pos()
                self.lastPos = self.currentPos

    # 重写鼠标释放
    def mouseReleaseEvent(self, event):
        if self.load_mode == 3 or self.load_mode == 4:
            self.currentPos = event.pos()
        elif self.mouse_move and self.step_list:
            self.flag = False
            mouse_up = (-1, -1)
            self.step_list.append(mouse_up)
            self.point_list.append(self.step_list[:])
            self.step_list = []
            if self.load_mode == 1:
                self.linethickness_list.append(self.linethickness)
                self.linestyle_list.append(self.linestyle)
                self.erasersize_list.append(self.erasersize)
            self.update()

    # 重写鼠标移动
    def mouseMoveEvent(self, mouseEvent):

        if self.flag and mouseEvent.buttons() == QtCore.Qt.LeftButton and self.mouse_move:
            if self.load_mode == 3 or self.load_mode == 4:
                self.loader_mouse_move = True
                self.currentPos = mouseEvent.pos()
            else:
                self.currentPos = mouseEvent.pos()
                # self.step_list.append((self.currentPos.x(), self.currentPos.y()))
                self.painter.begin(self.board)

                if self.load_mode == 1:
                    if self.use_pen and self.use_eraser == False:
                        self.painter.setPen(QPen(Qt.black, self.linethickness))
                    else:
                        self.painter.setPen(QPen(Qt.white, self.erasersize))

                    if self.linestyle == 1:
                        if abs(self.currentPos.x() - self.lastPos.x()) > self.linestyle * self.draw_type or abs(self.currentPos.y() - self.lastPos.y()) > self.linestyle * self.draw_type:
                            self.painter.drawLine(self.lastPos, self.currentPos)
                            self.step_list.append((self.currentPos.x(), self.currentPos.y()))
                            self.lastPos = self.currentPos



                    if self.linestyle == 2:
                        if abs(self.currentPos.x() - self.lastPos.x()) > self.linestyle * self.draw_type +3 or abs(self.currentPos.y() - self.lastPos.y()) > self.linestyle * self.draw_type+3:
                            self.step_list.append((self.currentPos.x(), self.currentPos.y()))
                            self.painter.drawLine(self.lastPos, self.currentPos)
                            self.lastPos = self.currentPos
                    if self.linestyle == 3:
                        if abs(self.currentPos.x() - self.lastPos.x()) > self.linestyle * self.draw_type or abs(self.currentPos.y() - self.lastPos.y()) > self.linestyle * self.draw_type:
                            self.step_list.append((self.currentPos.x(), self.currentPos.y()))
                            self.painter.drawPoint(self.currentPos)
                elif self.load_mode == 2:
                    self.painter.setPen(QPen(Qt.black, 5))
                    if abs(self.currentPos.x() - self.lastPos.x()) >= (self.write_mode + self.get_point_type) or abs(
                            self.currentPos.y() - self.lastPos.y()) >= (self.write_mode + self.get_point_type):
                        self.step_list.append((self.currentPos.x(), self.currentPos.y()))
                        self.painter.drawLine(self.lastPos, self.currentPos)
                        self.lastPos = self.currentPos
                self.painter.end()
                self.update()

    # 重写QPainter
    def paintEvent(self, paintEvent):
        super(Secondary_interface,self).paintEvent(paintEvent)
        self.painter.begin(self)
        self.painter.setPen(QPen(Qt.black, 5))
        self.painter.drawPixmap(0, 0, self.board)
        if self.load_mode == 3 or self.load_mode == 4:
            self.painter.setPen(QPen(Qt.black, 2))
            self.rect_X = min(self.lastPos.x(), self.currentPos.x())
            self.rect_Y = min(self.lastPos.y(), self.currentPos.y())
            self.rect_W = abs(self.lastPos.x() - self.currentPos.x())
            self.rect_H = abs(self.lastPos.y() - self.currentPos.y())
            if self.mouse_move == True:
                self.painter.drawRect(self.rect_X, self.rect_Y, self.rect_W, self.rect_H)
            self.update()

        self.painter.end()

    # 共用函数 撤销上一步
    def cancel_previous_step(self):
        if self.point_list:
            clear_list = self.point_list.pop()
            clear_linethickness = 5
            if self.load_mode == 1:
                clear_linethickness = self.linethickness_list.pop()

            self.painter.begin(self.board)
            self.painter.setPen(QPen(Qt.white, clear_linethickness))

            for i in range(len(clear_list) - 1):
                if (clear_list[i][0] and clear_list[i][1]) == -1 or (clear_list[i+1][0] and clear_list[i+1][1]) == -1:
                    continue
                self.painter.drawLine(clear_list[i][0], clear_list[i][1],
                                      clear_list[i+1][0], clear_list[i+1][1])
            self.painter.drawPoint(clear_list[0][0], clear_list[0][1])
            self.painter.drawPoint(clear_list[len(clear_list) - 1][0], clear_list[len(clear_list) - 1][1])
            self.painter.end()
        elif self.empty == True:
            QMessageBox.information(self, "清空提示", "当前画布为空", QMessageBox.Yes)
        else:
            clear_res = QMessageBox.information(self, "清空提示", "已撤销完成,当前操作会清空画布,确定要清空画布？",
                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if clear_res == QMessageBox.Yes:
                self.clear(True)
        self.update()
        if len(self.point_list) == 0 and self.empty == False:
            self.clear(True)
            QMessageBox.information(self, "撤销提示", "已撤销完成", QMessageBox.Yes)

    # 共用函数 清空画板
    def clear(self, Exit=True):
        if Exit == True:
            self.board.fill(Qt.white)
            self.point_list = []  # .clear()
            self.step_list = []  # .clear()
            self.update()
            self.empty = True

        elif self.empty == False:
            reply1 = QMessageBox.question(self,
                                          '是否保存当前绘画',
                                          "当前画板不为空，是否保存后再清理？",
                                          QMessageBox.Yes | QMessageBox.No,
                                          QMessageBox.Yes)
            if reply1 == QMessageBox.Yes:
                self.save_img()
                self.clear(True)
            else:
                self.board.fill(Qt.white)
                self.point_list = []  # .clear()
                self.step_list = []  # .clear()
                self.update()
                self.empty = True
        else:
            QMessageBox.information(self, '当前画板已为空', "当前画板已为空", QMessageBox.Yes)

    def save_img(self):
        if self.empty:
            QMessageBox.warning(self, '当前画板为空', "当前画板为空", QMessageBox.Yes)
        else:
            save_img = self.board.toImage()
            self.file_total += 1
            save_img.save(self.img_dir + 'img_' +
                          str(self.file_total) +
                          '.jpg', "JPG", 100)

            f_w = open(self.data_dir + 'img_' +
                       str(self.file_total) +
                       '.txt', 'w')
            for i in range(len(self.point_list)):
                for j in range(len(self.point_list[i])):
                    add_point = '{}, {}\n'.format(self.point_list[i][j][0],
                                                  self.point_list[i][j][1])
                    f_w.write(add_point)
            f_w.close()
            clear_msg = QMessageBox.question(self, "是否清空画板", "当前画板已保存,是否清空画板?", QMessageBox.Yes | QMessageBox.No,
                                             QMessageBox.Yes)
            if clear_msg == QMessageBox.Yes:
                self.clear(True)

    def preview(self, offect_x=0, offect_y=0, change_size_x=1.0, change_size_y=1.0):
        if self.preview_data:
            self.painter.begin(self.board)
            self.painter.setPen(QPen(Qt.black, 5))
            self.previewing = True
            self.empty = False
            for i in range(len(self.preview_data) - 1):
                point1 = self.preview_data[i]
                point2 = self.preview_data[i + 1]
                if (point1[0] and point1[1]) == -1 or (point2[0] and point2[1]) == -1:
                    continue
                self.painter.drawLine((point1[0] + offect_x), (point1[1] + offect_y),
                                      (point2[0] + offect_x), (point2[1] + offect_y))

            self.painter.end()
            self.update()
        else:
            QMessageBox.warning(self, "预览失败", "没有加载数据无法预览", QMessageBox.Yes)

    def load_already_data(self):
        alread_data = QFileDialog.getOpenFileName(self, "Open file", self.data_dir)
        load_data_res = False

        if alread_data[0]:
            f = open(alread_data[0], 'r')
            if self.preview_data:
                self.preview_data = []  # .clear()
            with f as file_to_read:
                while True:
                    lines = file_to_read.readline()
                    if not lines:
                        break
                    item = [i for i in lines.split(",")]
                    point_x = json.loads(item[0])
                    point_y = json.loads(item[1])

                    if (self.load_mode == 3 or self.load_mode == 4) and (point_x and point_y) >= 0:
                        self.min_x = min(point_x, self.min_x)
                        self.min_y = min(point_y, self.min_y)

                        self.max_x = max(point_x, self.max_x)
                        self.max_y = max(point_y, self.max_y)

                    self.preview_data.append([int(point_x), int(point_y)])
            load_data_res = True
            self.point_list.append(self.preview_data[:])

        if load_data_res == True:
            load_msg = "加载数据成功,是否选择预览？"
            load_res = QMessageBox.question(self, "数据加载", load_msg, QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)
            if load_res == QMessageBox.Yes:
                self.preview()
        else:
            QMessageBox.warning(self, "加载失败", "没有正确加载数据", QMessageBox.Yes)
        # print("加载数据成功")

    def choose_size_position(self):

        change_size_x = self.rect_W / (self.max_x - self.min_x)
        change_size_y = self.rect_H / (self.max_y - self.min_y)
        x = self.rect_X - self.min_x
        y = self.rect_Y - self.min_y
        self.clear()
        self.preview(x, y, change_size_x, change_size_y)

    def set_mouse_move(self, mode=True):
        self.mouse_move = mode


class draw_window(QDialog, GUI.Qt_UI.draw_board.Ui_Draw_Board):

    def __init__(self):
        super(draw_window, self).__init__()
        self.setupUi(self)

        Secondary_interface.label_mode = 1
        self.label_4 = Secondary_interface(self)
        self.label_4.setGeometry(QRect(350, 100, 500, 500))
        self.label_4.setPixmap(self.label_4.board)

    def keyPressEvent(self, event):

        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self,
                                               '画板',
                                               "是否要退出画板？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            if self.label_4.empty:
                event.accept()
            else:
                exit_msg = QMessageBox.warning(self, '当前画板为空', "当前画板不为空,是否保存后退出？", QMessageBox.Yes | QMessageBox.No,
                                               QMessageBox.Yes)
                if exit_msg == QMessageBox.Yes:
                    self.label_4.save_img()
                    self.label_4.clear(True)
                else:
                    self.label_4.clear(True)
                    event.accept()

        else:
            event.ignore()

    def ListenComboBox(self):

        self.label_4.linestyle = self.comboBox.currentIndex() + 1
        self.label_4.linethickness = self.comboBox_2.currentIndex() + 1
        self.label_4.erasersize = self.comboBox_3.currentIndex() + 1

    def StartDraw(self):

        if self.label_4.use_pen == False:
            self.label_4.use_pen = True
        if self.label_4.use_eraser == True:
            self.label_4.use_eraser = False
        self.label_4.set_mouse_move()

    def ClearBoard(self):
        self.label_4.clear()

    def CancelPreviousStep(self):
        self.label_4.cancel_previous_step()

    def Finish(self):
        self.label_4.use_pen = False
        self.label_4.use_eraser = False
        self.label_4.set_mouse_move(False)

    def Exit(self):
        self.close()

    def Save(self):
        self.label_4.save_img()

    def UsePen(self):
        self.label_4.use_pen = True
        if self.label_4.use_eraser:
            self.label_4.use_eraser = False

    def UseEraser(self):
        self.label_4.use_eraser = True
        if self.label_4.use_pen:
            self.label_4.use_pen = False


class write_window(QDialog, Ui_Dialog):

    def __init__(self):
        super(write_window, self).__init__()
        self.setupUi(self)

        Secondary_interface.label_mode = 2
        self.label = Secondary_interface(self)
        self.label.setGeometry(QRect(330, 110, 500, 500))
        self.label.setPixmap(self.label.board)

    def keyPressEvent(self, event):

        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def closeEvent(self, QCloseEvent):
        write_reply = QtWidgets.QMessageBox.question(self,
                                               '写字板',
                                               "是否要退出写字板？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if write_reply == QtWidgets.QMessageBox.Yes:
            # self.clear_EditText()
            if self.label.empty:
                QCloseEvent.accept()
            else:
                exit_msg = QMessageBox.warning(self, '当前写字板不为空', "当前写字板不为空,是否保存后退出？", QMessageBox.Yes | QMessageBox.No,
                                               QMessageBox.Yes)
                if exit_msg == QMessageBox.Yes:
                    print("保存后退出")
                    self.label.save_img()
                    self.label.clear(True)
                else:
                    self.label.clear(True)
                    print("直接退出")
                    QCloseEvent.accept()

        else:
            QCloseEvent.ignore()
        return

    def ListenComboBox(self):
        write_mode = self.comboBox.currentIndex() + 1
        self.label.write_mode = write_mode
        print(self.label.write_mode)

    def input_find(self):
        find_msg = QMessageBox.question(self, "输入查找", "请输入需要查找的字", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if find_msg == QMessageBox.Yes:
            print("弹出输入界面")
            find_res = True

            if find_msg == True:
                load_msg = QMessageBox.question(self, "已成功加载数据，是否选择预览？", QMessageBox.Yes | QMessageBox.No)
                if load_msg == QMessageBox.Yes:
                    print("预览成功")

    def load_already_data(self):
        self.label.load_already_data()

    def preview(self):
        self.label.preview()

    def save_write(self):
        self.label.save_img()

    def clear_board(self):
        self.label.clear()

    def exit_board(self):
        self.close()

    def start_write(self):
        self.label.set_mouse_move(True)

    def Cancel_previousStep(self):
        self.label.cancel_previous_step()

    def finish_write(self):
        self.label.set_mouse_move(False)


class loader_window(QDialog, Ui_loader):

    change_mode = 0
    current_prot_name = '/dev/ttyACM0'
    def __init__(self):
        super(loader_window, self).__init__()
        self.setupUi(self)

        Secondary_interface.label_mode = loader_window.change_mode
        HG_DR_SDK.prot_name = loader_window.current_prot_name
        self.execute_sdk = HG_DR_SDK()
        self.execute_sdk.connectHG_DR()

        self.label = Secondary_interface(self)
        self.label.setGeometry(QRect(200, 20, 500, 500))
        self.label.setPixmap(self.label.board)

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
            if self.label.empty == False:
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
        self.execute_sdk.moveToStation(259.48, 0, 85.32)
        self.execute_sdk.moveAnInterval(0, 0, 30)
        pen_down = False
        first_point = False
        for i in range(len(self.label.point_list[0])):

            # 移动到第一笔开头 落笔
            if not first_point:
                first_move_x = 259.48 - self.label.point_list[0][0][0]
                first_move_y = 0 - self.label.point_list[0][0][1]
                self.execute_sdk.moveAnInterval(first_move_x, first_move_y, 0)
                self.execute_sdk.moveAnInterval(0, 0, -30)
                first_point = not first_point
                pen_down = True
                continue

            # 笔没落下 移动到下一笔起点落笔
            if not pen_down:
                move_x = self.label.point_list[0][i][0] - self.label.point_list[0][i-1][0]
                move_y = self.label.point_list[0][i][1] - self.label.point_list[0][i-1][1]
                self.execute_sdk.moveAnInterval(move_x, move_y, 0)
                self.execute_sdk.moveAnInterval(0, 0, -30)
                pen_down = True
                continue

            # 下一笔 抬笔
            if self.label.point_list[0][i][0] == -1 or self.label.point_list[0][i][1] == -1:
                self.execute_sdk.moveAnInterval(0, 0, 30)
                pen_down = False
                continue

            if pen_down:
                pen_move_x = self.label.point_list[0][i][0] - self.label.point_list[0][i-1][0]
                pen_move_y = self.label.point_list[0][i][1] - self.label.point_list[0][i-1][1]
                self.execute_sdk.moveAnInterval(pen_move_x, pen_move_y, 0)

    def clear_preview(self):
        self.label.clear()

class CustomComboBox(QComboBox):
    popupAboutToBeShown = pyqtSignal()

    def __init__(self, parent=None):
        super(CustomComboBox, self).__init__(parent)

    def mousePressEvent(self, QMouseEvent):  # 这个是重写鼠标点击事件
        self.clear()
        self.showPopup()
        # self.popupAboutToBeShown.emit()
        # print("click")
    # 重写showPopup函数
    def showPopup(self):
        # 先清空原有的选项
        # self.insertItem(0, "请选择串口号")
        # index = 1
        Com_Dict = {}
        port_list = list(serial.tools.list_ports.comports())
        if port_list:
            for port in port_list:
                Com_Dict["%s" % port[0]] = "%s" % port[1]
                self.addItem(port[0])
        else:
            self.insertItem(0, "未检测到串口")
        # self.popupAboutToBeShown.emit()
        QComboBox.showPopup(self)
        # self.popupAboutToBeShown.emit()