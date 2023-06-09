import glob
from PyQt5.QtGui import *
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from GUI.Qt_UI.write_board import Ui_Dialog
import json

class write_label(QLabel):
    def __init__(self, parent=None):
        super(write_label, self).__init__(parent)

        self.painter = QPainter()

        write_file_number = glob.glob(pathname='./write_data/*.txt')  # 获取当前文件夹下个数
        self.write_num = len(write_file_number)

        self.count = 0
        self.write_list = []
        self.step_list = []
        self.preview_data = []

        self.get_point_type = 1

        # 鼠标上个位置点
        self.lastPos = QPoint(0, 0)
        # 鼠标当前点
        self.currentPos = QPoint(0, 0)
        self.flag = False
        self.empty = True
        self.draw = True
        self.previewing = False
        self.write_mode = 1

        self.size = QSize(500, 500)
        self.board = QPixmap(self.size)
        self.board.fill(Qt.white)
        # self.painter = None

    # 鼠标点击事件
    def mousePressEvent(self, mouseEvent):
        if mouseEvent.buttons() == QtCore.Qt.LeftButton and self.draw:
            self.flag = True
            self.empty = False
            self.currentPos = mouseEvent.pos()
            self.lastPos = self.currentPos
            # print("摁下来鼠标")

    # 鼠标释放事件
    def mouseReleaseEvent(self, event):
        if self.draw and self.step_list:
            self.flag = False
            mouse_up = (-1, -1)
            self.step_list.append(mouse_up)
            self.write_list.append(self.step_list[:])
            # print("松开了鼠标")
            self.step_list.clear()
            # self.update()

    '''
    取点方式改成判断x y方向移动距离
    连笔 x y 方向差3
    多笔 x y 方向差2
    后续考虑添加使用笔画拼接的方式按笔画拼接字
    (横竖撇那弯钩.......)
    '''
    def mouseMoveEvent(self, mouseEvent):

        self.painter.begin(self.board)
        self.painter.setPen(QPen(Qt.black, 5))

        if self.flag and mouseEvent.buttons() == QtCore.Qt.LeftButton and self.draw:
            # print("鼠标动了")

            self.count += 1
            self.currentPos = mouseEvent.pos()
            if abs(self.currentPos.x() - self.currentPos.x()) >= (self.write_mode + self.get_point_type) or abs(self.currentPos.y() - self.lastPos.y()) >= (self.write_mode + self.get_point_type):
                self.step_list.append((self.currentPos.x(), self.currentPos.y()))
                self.painter.drawLine(self.lastPos, self.currentPos)
                self.lastPos = self.currentPos
            self.update()
        self.painter.end()

    # 重写绘制事件
    def paintEvent(self, paintEvent):
        super(write_label, self).paintEvent(paintEvent)
        # self.painter = QPainter(self)
        self.painter.begin(self)
        self.painter.setPen(QPen(Qt.black, 5))
        self.painter.drawPixmap(0, 0, self.board)
        self.painter.end()

    def Cancel_previousStep(self):
        if self.write_list:
            clear_list = self.write_list.pop()
            self.painter.begin(self.board)
            self.painter.setPen(QPen(Qt.white, 5))

            for i in range(len(clear_list) - 1):
                if (clear_list[i][0] and clear_list[i][1]) == -1 or (clear_list[i+1][0] and clear_list[i+1][1]) == -1:
                    continue
                self.painter.drawLine(clear_list[i][0], clear_list[i][1], clear_list[i + 1][0],
                                      clear_list[i + 1][1])

            self.painter.drawLine(clear_list[0][0], clear_list[0][1], clear_list[1][0], clear_list[1][1])

            self.painter.end()
            self.update()
        elif self.empty == True:
            empty_res = QMessageBox.information(self, "清空提示", "当前写字板为空", QMessageBox.Yes)
        else:
            clear_res = QMessageBox.information(self, "清空提示", "已撤销完成,当前操作会清空画布,确定要清空画布？",
                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if clear_res == QMessageBox.Yes:
                self.clear(True)

        if len(self.write_list) == 0 and self.empty == False:
            self.clear(True)
            empty_msg = QMessageBox.information(self, "撤销提示", "已撤销完成", QMessageBox.Yes)

    def clear(self, Exit=False):

        if Exit == True or self.previewing == True:
            self.board.fill(Qt.white)
            self.write_list.clear()
            self.step_list.clear()
            self.preview_data.clear()
            self.update()
            self.empty = True

        elif self.empty == False:
            empty_msg = QMessageBox.question(self, "是否保存当前手写字", "当前写字板不为空,是否保存后再清理？",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if empty_msg == QMessageBox.Yes:
                self.save_write_img()
                self.clear(True)
            else:
                self.clear(True)
        else:
            reply1 = QMessageBox.information(self, '当前写字板已为空', "当前写字板已为空", QMessageBox.Yes)

    def save_write_img(self):
        if self.empty:
            empty_msg = QMessageBox.information(self, '当前写字板为空', "当前写字板为空", QMessageBox.Yes)
        else:
            write_img = self.board.toImage()

            write_img.save('./write_img/save_img.jpg', "JPG", 100)
            self.write_num += 1
            f_w = open('./write_data/write_' + str(self.write_num) + '.txt', 'w')
            for i in range(len(self.write_list)):
                for j in range(len(self.write_list[i])):
                    add_point = '{}, {}\n'.format(self.write_list[i][j][0], self.write_list[i][j][1])
                    f_w.write(add_point)

            f_w.close()
            clear_msg = QMessageBox.question(self, "是否清空写字板", "当前书写已保存,是否清空写字板?", QMessageBox.Yes | QMessageBox.No,
                                             QMessageBox.Yes)
            if clear_msg == QMessageBox.Yes:
                self.clear(True)
            print("保存书法作品")

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
        '''
        从文件中读取数据
        '''
        alread_data = QFileDialog.getOpenFileName(self, "Open file", './write_data/')
        load_data_res = False

        if alread_data[0]:
            f = open(alread_data[0], 'r')
            if self.preview_data:
                self.preview_data.clear()
            with f as file_to_read:
                while True:
                    lines = file_to_read.readline()
                    if not lines:
                        break
                    item = [i for i in lines.split(",")]
                    point_x = json.loads(item[0])
                    point_y = json.loads(item[1])

                    self.preview_data.append([int(point_x), int(point_y)])
            load_data_res = True
            self.write_list.append(self.preview_data[:])

        if load_data_res == True:
            load_msg = "加载数据成功,是否选择预览？"
            load_res = QMessageBox.question(self, "数据加载", load_msg, QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)
            if load_res == QMessageBox.Yes:
                self.preview()
        else:
            QMessageBox.warning(self, "加载失败", "没有正确加载数据", QMessageBox.Yes)
        # print("加载数据成功")

    def preview(self):
        if self.preview_data:
            self.painter.begin(self.board)
            self.painter.setPen(QPen(Qt.black, 5))
            self.previewing = True
            self.empty = False
            for i in range(len(self.preview_data) - 1):
                point1 = self.preview_data[i]
                point2 = self.preview_data[i+1]
                if (point1[0] and point1[1]) == -1 or (point2[0] and point2[1]) == -1:
                    # print(point2)
                    continue
                self.painter.drawLine(point1[0], point1[1], point2[0], point2[1])

            self.painter.end()
            self.update()
        else:
            QMessageBox.warning(self, "预览失败", "没有加载数据无法预览", QMessageBox.Yes)

    def write_now(self, write_now=True):
        self.draw = write_now

    def get_write_mode(self, write_mode=1):
        self.write_mode = write_mode


class write_window(QDialog, Ui_Dialog):

    def __init__(self):
        super(write_window, self).__init__()
        self.setupUi(self)

        self.size = QSize(500, 500)

        # 新建QPixmap作为画板，尺寸为__size
        self.board = QPixmap(self.size)
        self.board.fill(Qt.white)
        self.label = write_label(self)

        self.label.setGeometry(QRect(330, 110, 500, 500))
        self.label.setPixmap(self.board)

        # self.write_mode = 1

        # 重写键盘捕捉

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
                    self.label.save_write_img()
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
        self.label.get_write_mode(write_mode)
        print(write_mode)

    def input_find(self):
        self.label.input_find()
        # print("输入查找")

    def load_already_data(self):
        self.label.load_already_data()
        # print("加载已有数据")

    def preview(self):
        self.label.preview()
        # print("预览")

    def save_write(self):
        self.label.save_write_img()
        # print("保存")

    def clear_board(self):
        self.label.clear()
        # print("清空写字板")

    def exit_board(self):
        self.close()
        # print("退出写字板")

    def start_write(self):
        self.label.write_now(True)
        print("开始写字")

    def Cancel_previousStep(self):
        self.label.Cancel_previousStep()
        print('撤销上一步')

    def finish_write(self):
        self.label.write_now(False)
        print("结束书写")