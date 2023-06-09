from PyQt5.QtGui import *
import glob
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from GUI.Qt_UI.draw_board import Ui_Draw_Board


class MyLabel(QLabel):
    def __init__(self, parent=None):
        super(MyLabel, self).__init__(parent)

        path_file_number = glob.glob(pathname='./draw_data/*.txt')  # 获取当前文件夹下个数
        self.draw_num = len(path_file_number)
        # 画布上全部点   按先后顺序分段存储
        self.point_list = []     # point_list = [setp_list1[], setp_list2[], ```]

        # 当前正在画的点
        self.step_list = []

        # 记录变换
        self.linethickness_list = []
        self.linestyle_list = []
        self.erasersize_list = []
        self.count = 0

        # 鼠标上个位置点
        self.lastPos = QPoint(0, 0)
        # 鼠标当前点
        self.currentPos = QPoint(0, 0)
        self.flag = False

        self.size = QSize(500, 500)
        self.board = QPixmap(self.size)
        self.board.fill(Qt.white)
        self.painter = QPainter()

        self.draw_type = 2

        # 画笔 橡皮大小
        self.linethickness = 1
        self.linestyle = 1
        self.erasersize = 1

        self.linethickness_list.append(self.linethickness)
        self.linestyle_list.append(self.linestyle)
        self.erasersize_list.append(self.erasersize)

        # 默认可以画 捕捉鼠标事件 使用画笔 橡皮   默认使用笔 不使用橡皮
        self.draw = True
        self.use_pen = True
        self.use_eraser = False

        # 默认空白板
        self.empty = True

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
            self.point_list.append(self.step_list[:])
            # print("松开了鼠标")
            self.step_list = []

            self.linethickness_list.append(self.linethickness)
            self.linestyle_list.append(self.linestyle)
            self.erasersize_list.append(self.erasersize)
            self.update()

    # 鼠标移动事件
    '''
    修改
    取点太密集,点太多  虚线和画点效果不明显
    应该改成判断x y 方向的移动距离
    实线： x 3 y 3
    虚线： x 5 y 5
    点：   x 3  y 3
    选择虚线时保存点的地方不应该放在开头  这会直接保存全部点
    画点时应该画一个点 就添加一个(-1, -1)
    '''

    def mouseMoveEvent(self, mouseEvent):

        if self.flag and mouseEvent.buttons() == QtCore.Qt.LeftButton and self.draw:
            # print("鼠标动了")
            self.empty = False
            self.currentPos = mouseEvent.pos()
            self.step_list.append((self.currentPos.x(), self.currentPos.y()))
            self.painter.begin(self.board)
            self.count += 1

            if self.use_pen and self.use_eraser == False:
                self.painter.setPen(QPen(Qt.black, self.linethickness))
            else:
                self.painter.setPen(QPen(Qt.white, self.erasersize))

            if self.linestyle == 1:
                if abs(self.currentPos.x() - self.lastPos.x()) > self.linestyle * self.draw_type or abs(self.currentPos.y() - self.lastPos.y()) > self.linestyle * self.draw_type:
                    self.painter.drawLine(self.lastPos, self.currentPos)
                    self.lastPos = self.currentPos
            if self.linestyle == 2:
                if abs(self.currentPos.x() - self.lastPos.x()) > self.linestyle * self.draw_type +3 or abs(self.currentPos.y() - self.lastPos.y()) > self.linestyle * self.draw_type+3:
                    self.lastPos = self.currentPos
                self.painter.drawLine(self.lastPos, self.currentPos)

            if self.linestyle == 3:
                if abs(self.currentPos.x() - self.lastPos.x()) > self.linestyle * self.draw_type or abs(self.currentPos.y() - self.lastPos.y()) > self.linestyle * self.draw_type:
                    self.painter.drawPoint(self.currentPos)
            self.painter.end()

            self.update()

    # 绘制事件
    def paintEvent(self, paintEvent):
        super(MyLabel,self).paintEvent(paintEvent)
        #
        # painter = QPainter(self)
        # painter.setPen(QPen(Qt.black, self.linethickness, Qt.SolidLine))
        self.painter.begin(self)
        self.painter.drawPixmap(0, 0, self.board)
        self.painter.end()


    def up_LineStyle(self, LineStyle):
        self.linestyle = LineStyle
        # self.linestyle_list.append(LineStyle)
        # print(LineStyle)

    def up_LineThickness(self, LineThickness):
        self.linethickness = LineThickness
        # self.linethickness_list.append(LineThickness)
        # print(LineThickness)

    def up_EraserSize(self, EraserSize):
        self.erasersize = EraserSize
        # self.erasersize_list.append(EraserSize)
        # print(EraserSize)

    def pen_or_eraser(self, use_pen, use_eraser):
        if use_pen and use_eraser == False:
            self.use_pen = True
            self.use_eraser = False
            # print("画笔")
        else:
            self.use_pen = False
            self.use_eraser = True
            # print("橡皮")

    def cancel_previous_step(self):
        if self.point_list:
            clear_point = self.point_list.pop()
            clear_linethickness = self.linethickness_list.pop()

            self.painter.begin(self.board)
            self.painter.setPen(QPen(Qt.white, clear_linethickness))

            for i in range(len(clear_point)-1):
                self.painter.drawLine(clear_point[i][0], clear_point[i][1], clear_point[i+1][0], clear_point[i+1][1])

            self.painter.drawPoint(clear_point[0][0], clear_point[0][1])
            self.painter.drawPoint(clear_point[len(clear_point)-1][0], clear_point[len(clear_point)-1][1])
            self.painter.end()
        elif self.empty == True:
            empty_res = QMessageBox.information(self, "清空提示", "当前画布为空", QMessageBox.Yes)
        else:
            clear_res = QMessageBox.information(self, "清空提示", "已撤销完成,当前操作会清空画布,确定要清空画布？",
                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if clear_res == QMessageBox.Yes:
                self.clear(True)
        self.update()
        if len(self.point_list) == 0 and self.empty == False:
            self.clear(True)
            empty_msg = QMessageBox.information(self, "撤销提示", "已撤销完成", QMessageBox.Yes)

    def clear(self, Exit=False):
        # 清空画板
        if Exit == True:
            self.board.fill(Qt.white)
            self.point_list = []  # .clear()
            self.step_list = []  # .clear()
            self.update()
            self.empty = True

        elif self.empty == False:
            reply1 = QMessageBox.question(self, '是否保存当前绘画', "当前画板不为空，是否保存后再清理？", QMessageBox.Yes | QMessageBox.No,
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
            reply1 = QMessageBox.information(self, '当前画板已为空', "当前画板已为空", QMessageBox.Yes)

    def save_img(self):
        if self.empty:
            empty_msg = QMessageBox.warning(self, '当前画板为空', "当前画板为空", QMessageBox.Yes)
        else:
            draw_img = self.board.toImage()
            # print(type(draw_img))
            draw_img.save('./draw_img/save_img.jpg', "JPG", 100)
            self.draw_num += 1
            f_w = open('./draw_data/draw_' + str(self.draw_num) + '.txt', 'w')
            for i in range(len(self.point_list)):
                for j in range(len(self.point_list[i])):
                    add_point = '{}, {}\n'.format(self.point_list[i][j][0], self.point_list[i][j][1])
                    f_w.write(add_point)
            # self.angle_list.clear()
            f_w.close()
            clear_msg = QMessageBox.question(self, "是否清空画板", "当前画板已保存,是否清空画板?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if clear_msg == QMessageBox.Yes:
                self.clear(True)
            print("保存画作")

    def draw_now(self, draw_now=True):
        self.draw = draw_now


class draw_window(QDialog, Ui_Draw_Board):

    def __init__(self):
        super(draw_window, self).__init__()
        self.setupUi(self)

        self.size = QSize(500, 500)

        # 新建QPixmap作为画板，尺寸为__size
        self.board = QPixmap(self.size)
        self.board.fill(Qt.white)
        self.label_4 = MyLabel(self)

        self.label_4.setGeometry(QRect(350, 100, 500, 500))
        self.label_4.setPixmap(self.board)

        self.LineThickness = 1
        self.LineStyle = 1
        self.EraserSize = 1

        self.use_pen = False
        self.use_eraser = False

        self.setMouseTracking(False)

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
            # self.clear_EditText()
            if self.label_4.empty:
                event.accept()
            else:
                exit_msg = QMessageBox.warning(self, '当前画板为空', "当前画板不为空,是否保存后退出？", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if exit_msg == QMessageBox.Yes:
                    self.label_4.save_img()
                    self.label_4.clear(True)
                else:
                    self.label_4.clear(True)
                    event.accept()

        else:
            event.ignore()

    def ListenComboBox(self):

        self.LineStyle = self.comboBox.currentIndex() + 1
        self.LineThickness = self.comboBox_2.currentIndex() + 1
        self.EraserSize = self.comboBox_3.currentIndex() + 1

        self.label_4.up_LineStyle(self.LineStyle)
        self.label_4.up_LineThickness(self.LineThickness)
        self.label_4.up_EraserSize(self.EraserSize*2)

        print("上帝心态发生了一些变化", self.LineStyle, self.LineThickness, self.EraserSize)

    def StartDraw(self):
        if self.use_pen == False:
            self.use_pen = True
        if self.use_eraser == True:
            self.use_eraser = False
        self.label_4.pen_or_eraser(self.use_pen, self.use_eraser)
        self.label_4.draw_now()

        print("开始画了奥")

    def ClearBoard(self):
        self.label_4.clear()
        print("清理画布")

    def CancelPreviousStep(self):
        self.label_4.cancel_previous_step()
        print("撤销上一步")

    def Finish(self):
        self.use_pen = False
        self.use_eraser = False
        self.label_4.pen_or_eraser(self.use_pen, self.use_eraser)
        self.label_4.draw_now(False)
        print("结束绘画")

    def Exit(self):
            # self.clear_EditText()
        self.close()
        print("退出画板")

    def Save(self):
        self.label_4.save_img()
        print("保存图片")

    def UsePen(self):

        self.use_pen = True
        if self.use_eraser:
            self.use_eraser = False
        self.label_4.pen_or_eraser(self.use_pen, self.use_eraser)
        print("使用画笔")

    def UseEraser(self):

        self.use_eraser = True
        if self.use_pen:
            self.use_pen = False
        self.label_4.pen_or_eraser(self.use_pen, self.use_eraser)
        print("使用橡皮")


