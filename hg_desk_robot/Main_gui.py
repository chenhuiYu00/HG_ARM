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
import math
# from GUI.Qt_UI.Face_Painting import Ui_Main_GUI
from GUI.memory_teach_gui import memory_window
from GUI.Secondary_interface import draw_window
from GUI.Secondary_interface import write_window
from GUI.Secondary_interface import loader_window
from GUI.Qt_UI.main import Ui_Main_GUI
from SDK.HG_DR_SDK import HG_DR_SDK


class main_window(QtWidgets.QMainWindow, Ui_Main_GUI):

    def __init__(self):
        super(main_window, self).__init__()

        self.setupUi(self)

        self.connect_state = False  # 连接串口判断
        self.first_time = True  # 初始化判断
        self.initialization_time = 0   # 初始化次数
        self.catch_error = False       # 捕捉异常
        self.task_state = "请选择串口连接并进行初始化"

        # 状态栏
        self.label = QLabel()
        self.label.setStyleSheet("font-size:20px;")
        self.label.setText(self.task_state)
        self.status = self.statusBar()
        self.status.addPermanentWidget(self.label)
        self.status.showMessage('当前状态提示:')
        self.status.setStyleSheet("font-size:20px;")

        # 当前位置和角度
        self.x_data = 0.0
        self.y_data = 0.0
        self.z_data = 0.0
        self.angle1 = 0.0
        self.angle2 = 0.0
        self.angle3 = 0.0

        # 默认滑动条数据
        self.angle_move_data = 5
        self.pos_move_data = 10

        self.connect_res = False  # 连接状态
        self.connect_port_name = None  # 连接的串口名
        self.hg_dr_sdk = None  # 初始化SDK

        # 末端器具选择状态 使用状态
        self.tool_name = None
        self.tool_states = False
        self.use_pen = False
        self.use_pump = False

        # 界面控制
        self.control_states = False

    def connect_arm(self):
        if self.connect_res == False:
            if self.connect_port_name:
                HG_DR_SDK.prot_name = self.connect_port_name
                HG_DR_SDK.limit_data = int(self.limit.text())
                self.limit.setReadOnly(True)
                self.hg_dr_sdk = HG_DR_SDK()
                self.connect_res = self.hg_dr_sdk.connectHG_DR()
            if self.connect_res:
                self.port_state.setText("连接成功")
                self.connect.setText("断开")
            else:
                self.port_state.setText("连接失败")
                self.get_warning_msg(2)
        else:
            # self.connect.setText("断开")
            self.get_warning_msg(3)
            self.hg_dr_sdk.disconnectHG_DR()
            self.connect_res = False
            self.connect.setText("连接")
            self.port_state.setText("已断开连接")
            # self.first_time = False

        return self.connect_res
        # print("connect")

    def initialization(self):
        if self.connect_res:
            if self.first_time == False and self.initialization_time == 0:
                # self.hg_dr_sdk.connectHG_DR()
                self.hg_dr_sdk.calibrateJoint()
                #self.hg_dr_sdk.initializeSteppers()
                # self.all_state_thread.start()
                self.task_state = "正在开机"
                self.set_task_state()
                reply = QMessageBox.information(self, '开机初始化结果', '开机初始化成功', QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    print("开机初始化成功")
                    self.task_state = "开机初始化成功"
                    self.set_task_state()
                self.first_time = True
                self.initialization_time += 1
                self.arm_state.setText("开机正常")
                self.mpu1.setText("传感器1正常")
                self.mpu2.setText("传感器2正常")
                self.tool.setText("末端器具未选择")
                self.exchange.setText("通讯正常")
                self.get_angle_pose()

                # self.all_state_thread.start()

            else:
                reply_q = QMessageBox.question(self, '重新初始化', '确认重新初始化吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply_q == QMessageBox.Yes:
                    # self.all_state_thread.terminate()
                    print("------开始重新初始化------")
                    # self.all_state_thread.msleep(100)
                    # self.all_state_thread.start()
                    self.hg_dr_sdk.calibrateJoint()
                    initialization_str = "------第" + str(self.initialization_time) + "次重新初始化成功------"
                    self.task_state = "第" + str(self.initialization_time) + "次重新初始化成功"
                    self.set_task_state()
                    self.arm_state.setText("开机正常")
                    self.mpu1.setText("传感器1正常")
                    self.mpu2.setText("传感器2正常")
                    self.tool.setText("末端器具未选择")
                    self.exchange.setText("通讯正常")
                    self.get_angle_pose()
                    print(initialization_str)
                    self.initialization_time += 1
                    self.first_time = True
        else:
            self.get_warning_msg(2)

    def arm_stop(self):
        if self.hg_dr_sdk:
            self.hg_dr_sdk.controlPerSteppers(0, 0, 0)
            '''
            self.hg_dr_sdk.disconnectHG_DR()
            self.connect_res = False
            self.connect.setText("连接")
            self.port_state.setText("已断开连接")
            self.first_time = False
            print("urgent_stop")
            '''

    def port_imf(self):
        self.connect_port_name = self.port_name.currentText()
        print(self.connect_port_name)
        if self.connect_res == False:
            self.port_state.setText(self.connect_port_name)
        # print("port_imf")

    def use_tool(self):
        tool_num = self.end_tool.currentIndex()
        if tool_num == 0:
            self.tool_name = "未选择末端器具"
            self.tool.setText("末端器具未选择")
            self.use_pen = False
            self.use_pump = False
        elif tool_num == 1:
            self.tool_name = "使用气泵"
            self.tool.setText("末端器具为气泵")
            self.use_pump = True
            if self.use_pen:
                self.use_pen = not self.use_pen
        elif tool_num == 2:
            self.tool_name = "使用笔"
            self.tool.setText("末端器具为笔")
            self.use_pen = True
            if self.use_pump:
                self.use_pump = not self.use_pen
        self.end_tool_state.setText(self.tool_name)
        # print("use_tool")

    def tool_state(self):
        if self.tool_states == False and self.up.isChecked():
            self.tool_states = True
            if self.down.isChecked():
                self.down.setChecked(False)
        if self.tool_states and self.down.isChecked():
            self.tool_states = False
            if self.up.isChecked():
                self.up.setChecked(False)
        if self.tool_states and self.up.isChecked() == False:
            self.tool_states = False
            if self.down.isChecked() == False:
                self.down.setChecked(True)
        if self.use_pump:
            if self.tool_states:
                self.hg_dr_sdk.controlPump(1)
            else:
                self.hg_dr_sdk.controlPump(0)
        # print("tool_state")

    def teach(self):
        if self.first_time:
            load_teach_data = False
            self.task_state = "正在执行示教功能"
            self.set_task_state()
            fname = QFileDialog.getOpenFileName(self, 'Open file', './teach_data/')
            if fname[0]:
                # f = open(fname[0], 'r')
                data = []
                with open(fname[0], 'r+') as f:
                    for line in f.readlines():
                        print(line[:-1].split(','))
                        s = line[:-1].split(',')
                        data.append(s)
                    load_teach_data = True
            if load_teach_data:
                print(data)
                teach_msg = '加载示教数据成功'
                reply = QMessageBox.information(self, '启动示教功能', teach_msg, QMessageBox.Yes)
                if reply:

                    for i in range(len(data)):
                        self.get_angle_pose()
                        print(type(data[i][0]), type(float(data[i][0])), float(data[i][1]))
                        if self.hg_dr_sdk.controlPerSteppers(float(data[i][0]) - self.angle1,
                                                             float(data[i][1]) - self.angle2,
                                                             float(data[i][2]) - self.angle3):
                            self.hg_dr_sdk.controlPump(int(data[i][3]))
                            self.get_angle_pose()
                            time.sleep(1.0)
                    print("开始启动示教功能成功")
                    self.task_state = "执行示教功能成功"
                    self.set_task_state()
            else:
                teach_msg = '加载示教数据失败'
                reply = QMessageBox.information(self, '启动示教功能', teach_msg, QMessageBox.Yes)
                if reply:
                    print("开始启动示教功能失败")
                    self.task_state = "未加载示教数据"
                    self.set_task_state()
        else:
            warning_msg = self.get_warning_msg(1)
        print("teach")

    def memory_teach(self):
        if self.first_time:
            self.task_state = "正在执行记忆示教"
            self.set_task_state()
            memory_teach_msg = '开始记忆示教'
            reply = QMessageBox.information(self, '启动记忆示教', memory_teach_msg, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                print("开始启动记忆示教功能")

            memory_windows.show()
            self.task_state = "退出记忆示教功能"
            self.set_task_state()
        else:
            warning_msg = self.get_warning_msg(1)
        print("memory_teach")

    def check_reboot(self):
        if self.first_time:
            if self.hg_dr_sdk.check_read_mpu():
                self.initialization()
            else:
                self.mpu1.setText("传感器1异常")
                self.mpu2.setText("传感器2异常")
                self.get_warning_msg(4)
            print("check_reboot")
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

    def expand(self):
        # 扩展模块
        # self.hg_dr_sdk.moveAnInterval(0,0,30)
        print("expand")

    # 检测加载数据
    # data_type:
    #           1 - teach_data
    #           2 - write_data
    #           3 - draw_data
    #           4 - script_date
    def check_data(self, data_type):
        pass

    '''
    脚本执行模块
    1. calibrateJoint(None) 校准一关节
    2. init(None) 初始化 
    3. save(baseAngle, rearAngle, frontAngle, x, y, z) 保存
    4. movePoint(x, y, z)　笛卡尔坐标运动
    5. moveInterval(x, y, z)　末端运动
    6. moveAngle(baseAngle, rearAngle, frontAngle)　关节运动
    7. control_pump(pump_state)　控制气泵
    8. control_light(color)　控制RGB灯
    9. delay(time)  延迟,秒
    '''
    def execute_script(self):
        if self.first_time:
            load_script_data = False
            self.task_state = "正在执行脚本"
            self.set_task_state()
            fname = QFileDialog.getOpenFileName(self, 'Open file', './script_data/')
            if fname[0]:
                # f = open(fname[0], 'r')
                data = []
                with open(fname[0], 'r+') as f:
                    for line in f.readlines():
                        # print(line[:-1].split(','))
                        s = line[:-1].split(',')
                        data.append(s)
                    load_script_data = True
            if load_script_data:
                teach_msg = '加载脚本数据成功'
                reply = QMessageBox.information(self, '执行脚本程序', teach_msg, QMessageBox.Yes)
                for i in range(len(data)):
                    # print(data[i])
                    if data[i][0] == "calibrateJoint":
                        self.hg_dr_sdk.calibrateJoint()
                    if data[i][0] == "init":
                        self.hg_dr_sdk.initializeSteppers()
                    if data[i][0] == "save":
                        baseAngle = float(data[i][1])
                        rearAngle = float(data[i][2])
                        frontAngle = float(data[i][3])
                        x = float(data[i][4])
                        y = float(data[i][5])
                        z = float(data[i][6])
                        self.hg_dr_sdk.saveAngleAndPose(baseAngle, rearAngle, frontAngle, x, y, z)
                    if data[i][0] == "movePoint":
                        target_x = float(data[i][1])
                        target_y = float(data[i][2])
                        target_z = float(data[i][3])
                        self.hg_dr_sdk.moveToStation(target_x, target_y, target_z)
                    if data[i][0] == "moveInterval":
                        move_x = float(data[i][1])
                        move_y = float(data[i][2])
                        move_z = float(data[i][3])
                        self.hg_dr_sdk.moveToStation(move_x, move_y, move_z)
                    if data[i][0] == "moveAngle":
                        target_base = float(data[i][1])
                        target_rear = float(data[i][2])
                        target_front = float(data[i][3])
                        self.hg_dr_sdk.move_to_angle(target_base, target_rear, target_front)
                    if data[i][0] == "control_pump":
                        pump_state = int(data[i][1])
                        self.hg_dr_sdk.controlPump(pump_state)
                    if data[i][0] == "control_light":
                        light_color = data[i][1]
                        self.hg_dr_sdk.controlRGBlight(light_color)
                    if data[i][0] == "delay":
                        slepp_time = float(data[i][1])
                        time.sleep(slepp_time)
                self.task_state = "执行脚本成功"
                self.set_task_state()
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

    def gui_control(self):
        angle_11, angle_22 = self.hg_dr_sdk.get_mpu_data()
        print("angle11, angle22: ", angle_11, angle_22)
        if self.first_time:
            self.control_states = not self.control_states
        else:
            self.control.setChecked(False)
            warning_msg = self.get_warning_msg(1)

    def get_angle_pose(self):
        self.angle1, self.angle2, self.angle3, self.x_data, self.y_data, self.z_data = self.hg_dr_sdk.getAngleAndPose()
        self.point_x.setText(str('%.2f' % self.x_data))
        self.point_y.setText(str('%.2f' % self.y_data))
        self.point_z.setText(str('%.2f' % self.z_data))

        self.angle_1.setText(str('%.2f' % self.angle1))
        self.angle_2.setText(str('%.2f' % self.angle2))
        self.angle_3.setText(str('%.2f' % self.angle3))

    # 位置滑动条
    def set_pos_move(self):
        self.pos_move_data = int(self.pos_slider.value())
        self.pos_data.setText(str(self.pos_move_data))

    # 角度滑动条
    def set_angle_move(self):
        self.angle_move_data = int(self.angle_slider.value())
        self.angle_data.setText(str(self.angle_move_data))


    def add_point(self, num):
        points = [self.x_data, self.y_data, self.z_data]
        if self.control_states:
            if num == 1:
                self.x_data += self.pos_move_data
                self.point_x.setText(str('%.2f' % self.x_data))
                points[num-1] += self.pos_move_data
            if num == 2:
                self.y_data = self.y_data + self.pos_move_data
                self.point_y.setText(str('%.2f' % self.y_data))
                points[num - 1] += self.pos_move_data
            if num == 3:
                self.z_data = self.z_data + self.pos_move_data
                self.point_z.setText(str('%.2f' % self.z_data))
                points[num - 1] += self.pos_move_data

            # if self.control_states:
            self.hg_dr_sdk.moveToStation(points[0], points[1], points[2])
            self.get_angle_pose()

    def less_point(self, num=1):
        points1 = [self.x_data, self.y_data, self.z_data]
        if self.control_states:
            if num == 1:
                self.x_data -= self.pos_move_data
                self.point_x.setText((str('%.2f' % self.x_data)))
                points1[num - 1] -= self.pos_move_data
            if num == 2:
                self.y_data = self.y_data - self.pos_move_data
                self.point_y.setText(str('%.2f' % self.y_data))
                points1[num - 1] -= self.pos_move_data
            if num == 3:
                self.z_data = self.z_data - self.pos_move_data
                self.point_z.setText(str('%.2f' % self.z_data))
                points1[num - 1] -= self.pos_move_data

            # if self.control_states:
            self.hg_dr_sdk.moveToStation(points1[0], points1[1], points1[2])

    def add_angle(self, num=1):
        # points2 = [self.angle1, self.angle2, self.angle3]
        points2 = [0.0, 0.0, 0.0]
        if self.control_states:
            # rear_angle, front_angle = self.hg_dr_sdk.get_mpu_data()
            if num == 1:
                self.angle1 += self.angle_move_data
                self.angle_1.setText(str('%.2f' % self.angle1))
                points2[num - 1] = self.angle_move_data  # self.angle1
            if num == 2:
                self.angle2 += self.angle2 + self.angle_move_data
                self.angle_2.setText(str('%.2f' % self.angle2))
                points2[num - 1] = self.angle_move_data  # self.angle2
            if num == 3:
                self.angle3 += self.angle3 + self.angle_move_data
                self.angle_3.setText(str('%.2f' % self.angle3))
                points2[num - 1] = self.angle_move_data  # self.angle3

            # if self.control_states:
            #     print((points2[0], points2[1], points2[2]))
            # move_X, move_Y, move_Z = self.hg_dr_sdk.angle_to_point(points2[0]*(math.pi/180),
            #                                                        points2[1]*(math.pi/180),
            #                                                        points2[2]*(math.pi/180))
            # self.hg_dr_sdk.moveToStation(move_X, move_Y, move_Z)
            self.hg_dr_sdk.controlPerSteppers(points2[0], points2[1], points2[2])
            self.get_angle_pose()
            # rear_angle_now, front_angle_now = self.hg_dr_sdk.get_mpu_data()
            # print("current move angle:", rear_angle_now - rear_angle, front_angle_now - front_angle)

    def less_angle(self, num=1):
        # points3 = [self.angle1, self.angle2, self.angle3]
        points3 = [0.0, 0.0, 0.0]
        if self.control_states:
            if num == 1:
                self.angle1 -= self.angle_move_data
                self.angle_1.setText(str('%.2f' % self.angle1))
                points3[num - 1] = -self.angle_move_data  # self.angle1
            if num == 2:
                self.angle2 -= self.angle_move_data
                self.angle_2.setText(str('%.2f' % self.angle2))
                points3[num - 1] = -self.angle_move_data  # self.angle2
            if num == 3:
                self.angle3 -= self.angle_move_data
                self.angle_3.setText(str('%.2f' % self.angle3))
                points3[num - 1] = -self.angle_move_data  # self.angle3
            # if self.control_states:
            if self.hg_dr_sdk.controlPerSteppers(points3[0], points3[1], points3[2]):
            # move_X, move_Y, move_Z = self.hg_dr_sdk.angle_to_point(points3[0] * (math.pi / 180),
            #                                                        points3[1] * (math.pi / 180),
            #                                                        points3[2] * (math.pi / 180))
            # self.hg_dr_sdk.moveToStation(move_X, move_Y, move_Z)
                self.get_angle_pose()

    def renew_data(self):
        self.get_angle_pose()


    def set_task_state(self):
        self.label.setText(self.task_state)

    def get_warning_msg(self, num):
        warning_msg = {
            1: "Warning: 请先初始化后再进行该操作!",
            2: "Warning: 请先选择正确的机械臂串口！",
            3: "Warning: 当前串口已成功连接机械臂, 确认断开吗？",
            4: "Warning: 传感器异常, 请检查传感器连接并重启",
            5: "其他警告"
        }
        warning_title = {
            1: "未初始化",
            2: "未选择连接机械臂的串口",
            3: "是否选择断开",
            4: "其他"
        }
        QMessageBox.warning(self, warning_title.get(num), warning_msg.get(num), QMessageBox.Yes)
        return warning_msg.get(num)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    window = main_window()

    window.setWindowIcon(QIcon('./logo/arm.png'))
    window.show()

    memory_windows = memory_window()
    memory_windows.setWindowIcon(QIcon('./logo/arm.png'))

    draw_windows = draw_window()
    draw_windows.setWindowIcon(QIcon('./logo/arm.png'))

    write_windows = write_window()
    write_windows.setWindowIcon(QIcon('./logo/arm.png'))

    sys.exit(app.exec_())