# -*- coding:utf8 -*-
#!/usr/bin/python
import sys
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import serial
import serial.tools.list_ports
import time
from GUI.Qt_UI.Face_Painting import Ui_Main_GUI
from GUI.memory_teach_gui import memory_window
from GUI.Secondary_interface import draw_window
from GUI.Secondary_interface import write_window
from GUI.Secondary_interface import loader_window
# from GUI.Qt_UI.main import Ui_Main_GUI
from SDK.HG_DR_SDK import HG_DR_SDK


class mywindow(QtWidgets.QMainWindow, Ui_Main_GUI):

    def __init__(self):
        super(mywindow, self).__init__()

        self.setuUi(self)
        self.count = 0

        self.logo = QPixmap('./logo/logo.jpeg')
        # self.label.setStyleSheet("border: 2px solid red")
        self.label.setPixmap(self.logo)
        self.label.setScaledContents(True)

        self.all_state_thread = all_thread()
        self.all_state_thread.all_thread_signal.connect(self.update_state)

        self.angle1_now = 0.0
        self.angle2_now = 0.0
        self.angle3_now = 0.0

        self.angle1_data = 0.0
        self.angle2_data = 0.0
        self.angle3_data = 0.0

        self.first_time = False
        self.initialization_time = 0

        self.catch_error = False
        self.task_state = "成功启动GUI界面, 请首先进行初始化"

        self.label = QLabel()
        self.label.setText(self.task_state)
        self.status = self.statusBar()
        self.status.addPermanentWidget(self.label)
        self.status.showMessage('当前状态提示:')
        self.status.setStyleSheet("font-size:20px;")

        self.prot_name = None
        self.hg_dr_sdk = None

    def initialization(self):

        if self.prot_name:
            HG_DR_SDK.prot_name = self.prot_name
            self.hg_dr_sdk = HG_DR_SDK()
            if self.first_time == False and self.initialization_time == 0:
                self.hg_dr_sdk.connectHG_DR()
                self.hg_dr_sdk.initializeSteppers()
                # self.all_state_thread.start()
                self.task_state = "正在开机"
                reply = QMessageBox.information(self, '开机初始化结果', '开机初始化成功', QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    print("开机初始化成功")
                    self.task_state = "开机初始化成功"
                self.first_time = True
                self.initialization_time += 1
                self.all_state_thread.start()

            else:
                reply_q = QMessageBox.question(self, '重新初始化', '确认重新初始化吗？', QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
                if reply_q == QMessageBox.Yes:
                    self.all_state_thread.terminate()
                    print("------开始重新初始化------")
                    self.all_state_thread.msleep(100)
                    self.all_state_thread.start()
                    initialization_str = "------第" + str(self.initialization_time) + "次重新初始化成功------"
                    self.task_state = "第"+str(self.initialization_time)+"次重新初始化成功"
                    print(initialization_str)
                    self.initialization_time += 1
        else:
            self.get_warning_msg(2)
            # QMessageBox.warning(self, '未选择连接的串口', '请选择连接的串口', QMessageBox.Yes)

    def teach(self):
        if self.first_time:
            load_teach_data = False
            self.task_state = "正在执行示教功能"
            fname = QFileDialog.getOpenFileName(self, 'Open file', './teach_data/')
            if fname[0]:
                f = open(fname[0], 'r')
                with f:
                    data = f.read()
                    print(data)
                    load_teach_data = True
            if load_teach_data:
                teach_msg = '加载示教数据成功'
                reply = QMessageBox.information(self, '启动示教功能', teach_msg, QMessageBox.Yes)
                if reply:
                    print("开始启动示教功能成功")
                    self.task_state = "执行示教功能成功"
            else:
                teach_msg = '加载示教数据失败'
                reply = QMessageBox.information(self, '启动示教功能', teach_msg, QMessageBox.Yes)
                if reply:
                    print("开始启动示教功能失败")
                    self.task_state = "未加载示教数据"
        else:
            warning_msg = self.get_warning_msg(1)

    def memory_teach(self):
        if self.first_time:
            self.task_state = "正在执行记忆示教"
            memory_teach_msg = '开始记忆示教'
            reply = QMessageBox.information(self, '启动记忆示教', memory_teach_msg, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                print("开始启动记忆示教功能")

            memory_windows.exec_()
            self.task_state = "退出记忆示教功能"
        else:
            warning_msg = self.get_warning_msg(1)

    def get_angle(self):
        if self.first_time:
            self.task_state = "正在获取关节角度"
            self.angle1_now = self.angle1_data
            self.angle2_now = self.angle2_data
            self.angle3_now = self.angle3_data
            print("获取关节角度成功,当前关节角度分别为：", self.angle1_now, self.angle2_now, self.angle3_now)
            self.task_state = '获取关节角度成功'
            return self.angle1_now, self.angle2_now, self.angle3_now
        else:
            warning_msg = self.get_warning_msg(1)

    def draw_demo(self):
        if self.first_time:
            self.task_state = "正在执行画画Demo"
            print("开始启动画画Demo")
        else:
            warning_msg = self.get_warning_msg(1)

    def write_demo(self):
        if self.first_time:
            self.task_state = "正在执行写字Demo"
            # self.lineEdit_7.setText(self.task_state)
            print("开始启动写字Demo")

            self.task_state = "执行写字Demo完成"
        else:
            warning_msg = self.get_warning_msg(1)

    def draw(self):
        if self.first_time:
            self.task_state = "正在执行画画功能"
            loader_window.change_mode = 3
            loader_window_gui = loader_window()
            loader_window_gui.setWindowIcon(QIcon('./logo/arm.png'))
            loader_window_gui.exec_()
            self.task_state = "执行画画程序完毕"
            # print("开始启动画画功能")
        else:
            warning_msg = self.get_warning_msg(1)

    def write(self):
        if self.first_time:
            self.task_state = "正在执行写字功能"
            loader_window.change_mode = 4
            loader_window_gui = loader_window()
            loader_window_gui.setWindowIcon(QIcon('./logo/arm.png'))
            loader_window_gui.exec_()
            self.task_state = "执行写字程序完毕"
            # demo_msg = "正在执行写字功能"
            # reply = QMessageBox.information(self, '启动写字功能', demo_msg, QMessageBox.Yes)
            # if reply == QMessageBox.Yes:
            #     print("开始启动写字功能")
        else:
            warning_msg = self.get_warning_msg(1)

    def open_draw_board(self):
        self.task_state = "打开画板"
        draw_windows.exec_()
        self.task_state = "关闭画板"

        print("打开画板")

    def open_write_board(self):
        self.task_state = "打开写字板"
        write_windows.exec_()
        self.task_state = "关闭写字板"
        print("打开写字板")

    def update_state(self):

        self.angle1_data, self.angle2_data, self.angle3_data = self.hg_dr_sdk.get_angle()

        self.angle1.setText(str(self.angle1_data))
        self.angle2.setText(str(self.angle2_data))
        self.angle3.setText(str(self.angle3_data))
        # print(self.angle1_data, self.angle2_data, self.angle3_data)
        memory_windows.angle_update(self.angle1_data, self.angle2_data, self.angle3_data)

        self.label.setText(self.task_state)
        color = self.hg_dr_sdk.get_color_num()
        if color == 1:
            self.arm_state.setText("机械臂出错")
            self.label_9.setStyleSheet("background-color: rgb(255, 0, 0);")
        elif color == 4:
            self.arm_state.setText("机械臂静止")
            self.label_9.setStyleSheet("background-color: rgb(0, 255, 0);")
        elif color == 6:
            self.arm_state.setText("机械臂运动")
            self.label_9.setStyleSheet("background-color: rgb(0, 0, 255);")

        memory_windows.angle_update(self.angle1_data, self.angle2_data, self.angle3_data)

        if self.hg_dr_sdk.get_pump_state() == False:
            self.pump_state.setText('不吸气')

        else:
            self.pump_state.setText('吸气')

    def get_warning_msg(self, num):
        warning_msg = {
            1: "Warning: 请先初始化后再进行该操作!",
            2: "Warning: 请先选择对应的机械臂串口！",
            3: "其他警告"
        }
        warning_title = {
            1: "未初始化",
            2: "未选择连接机械臂的串口",
            3: "其他"
        }
        QMessageBox.warning(self, warning_title.get(num), warning_msg.get(num), QMessageBox.Yes)
        return warning_msg.get(num)

    def port_check(self):
        self.Com_Dict = {}
        port_list = list(serial.tools.list_ports.comports())
        self.comboBox.clear()
        for port in port_list:
            self.Com_Dict["%s" % port[0]] = "%s" % port[1]
            self.comboBox.addItem(port[0])
        if len(self.Com_Dict) == 0:
            self.label_7.setText(" 无串口")

    def port_imf(self):
        # 显示选定的串口的详细信息
        imf_s = self.comboBox.currentText()
        if imf_s != "":
            self.label_7.setText(self.Com_Dict[self.comboBox.currentText()])
            self.prot_name = imf_s

class all_thread(QThread):

    all_thread_signal = pyqtSignal(int)

    def __init__(self):
        super(all_thread, self).__init__()
        self.thread_working = True

    def __del__(self):

        self.thread_working = False
        self.wait()

    def run(self):
        while self.thread_working == True:
            self.all_thread_signal.emit(1)
            self.msleep(100)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    window = mywindow()

    window.setWindowIcon(QIcon('./logo/arm.png'))
    window.show()

    memory_windows = memory_window()
    memory_windows.setWindowIcon(QIcon('./logo/arm.png'))

    draw_windows = draw_window()
    draw_windows.setWindowIcon(QIcon('./logo/arm.png'))

    write_windows = write_window()
    write_windows.setWindowIcon(QIcon('./logo/arm.png'))

    sys.exit(app.exec_())