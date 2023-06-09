#!/usr/bin/python
# -*- coding:utf8 -*-
'''
HG_DR_SDK-version-1.0
date: 2021/3/26
'''

import time
import math
import json
import rospy
from std_msgs.msg import Int32, Int64
from HG_DR_SDK import HG_DR_SDK
from HG_DR_KI import HG_DR_KI
from object_detect.msg import object_result_msg


class grasp_object:
    def __init__(self):
        rospy.init_node('listener', anonymous=True)
        port_name = rospy.get_param("~port_name", "/dev/ttyACM0")
        HG_DR_SDK.prot_name = port_name
        self.HG_DR_C = HG_DR_SDK()
        self.HG_DR_C.connectHG_DR()
        self.HG_DR_C.calibrateJoint()
	self.HG_DR_C.move_to_angle(0, 20, 5)
        self.move_time = 0
        self.target_x, self.target_y, self.target_side = 0.0, 0.0, None
        rospy.Subscriber("grasp_target", Int32, self.callback)
        self.grasp_state = rospy.Publisher("grasp_state", Int32, queue_size=1)
        self.obj_color_pub = rospy.Publisher("object_color", Int64, queue_size=1)
        self.robot_ready_pub = rospy.Publisher("robotInitDone", Int64, queue_size=1)
        # # 识别物体的中心坐标
        rospy.Subscriber("object_center", object_result_msg, self.arm_move_control)
        self.start_grasp = True
        rospy.spin()

    def arm_move_control(self, data):
        self.target_x = data.data[0]
        self.target_y = data.data[1]
        self.target_side = data.data[2]

    def control_pump(self, data):
        if data.data == 1:
            self.HG_DR_C.controlPump(1)
            time.sleep(1.0)
            print("Pump start!!")
        if data.data == 0:
            self.HG_DR_C.controlPump(0)
            time.sleep(1.0)
            print("Pump end!!")
        if data.data == 2:
            self.start_grasp = True
            self.HG_DR_C.calibrateJoint()
            print("ready to grasp again!!")

    def robot_move(self, move_type):
        time.sleep(5.0)
        x = 69 * (self.target_y - 239.5) / self.target_side - 50
        y = -85 * (self.target_x - 319.5) / self.target_side + 2  

        if move_type == 1:
            if self.move_time == 0:
                    self.HG_DR_C.moveAnInterval(x, y, 0)
                    self.move_time += 1
                    time.sleep(2.0)
            else:
                if self.move_time == 1:
                    self.move_time += 1
            if self.move_time == 2:
                self.HG_DR_C.moveAnInterval(x, y, 0)
                self.HG_DR_C.moveAnInterval(0, 0, -137)
                self.HG_DR_C.moveAnInterval(0, 0, -30)
                self.id = 0
                # self.HG_DR_C.moveAnInterval(0, 0, -65)
                # time.sleep(2)
                self.HG_DR_C.controlPump(1)
                time.sleep(2)
                self.HG_DR_C.moveAnInterval(0, 0, 45)   # 吸取完之后往上
                self.HG_DR_C.move_to_angle(90, 15, 45)  # 移动到中间角度
                self.HG_DR_C.moveAnInterval(-80, 40, -50)   # 放到货仓里
                self.HG_DR_C.controlPump(0)                 # 关闭气泵
                self.HG_DR_C.moveAnInterval(80, -40, 50)    # 从货仓出来
            #self.HG_DR_C.move_to_angle(90, 15, 45)
                self.HG_DR_C.move_to_angle(0, 20, 5)        #  回到识别位置
                self.move_time = 0
                self.grasp_state.publish(1) # 发送放置完成信号
            else:
                self.robot_move(1)

        if move_type == 2:
            if self.move_time == 0:
                    self.HG_DR_C.moveAnInterval(x, y, 0)
                    self.move_time += 1
                    time.sleep(2.0)
            else:
                if self.move_time == 1:
                    self.move_time += 1
            if self.move_time == 2:
                self.HG_DR_C.moveAnInterval(x, y, 0)
                self.HG_DR_C.moveAnInterval(0, 0, -137)
                self.HG_DR_C.moveAnInterval(0, 0, -30)
                self.id = 0
                # self.HG_DR_C.moveAnInterval(0, 0, -65)
                # time.sleep(2)
                self.HG_DR_C.controlPump(1)
                time.sleep(2)
                self.HG_DR_C.moveAnInterval(0, 0, 45)
                self.HG_DR_C.move_to_angle(90, 15, 45)
                self.HG_DR_C.moveAnInterval(-80, 40, -50)
                self.HG_DR_C.controlPump(0)
                self.HG_DR_C.moveAnInterval(80, -40, 50)
		        #self.HG_DR_C.move_to_angle(90, 15, 45)
                self.HG_DR_C.move_to_angle(0, 20, 5)
                self.move_time = 0
                self.grasp_state.publish(1)
            else:
                self.robot_move(2)

        if move_type == 3:
            if self.move_time == 0:
                    self.HG_DR_C.moveAnInterval(x, y, 0)
                    self.move_time += 1
                    time.sleep(2.0)
            else:
                if self.move_time == 1:
                    self.move_time += 1
            if self.move_time == 2:
                self.HG_DR_C.moveAnInterval(x, y, 0)
                self.HG_DR_C.moveAnInterval(0, 0, -137)
                self.HG_DR_C.moveAnInterval(0, 0, -30)
                self.id = 0
            # self.HG_DR_C.moveAnInterval(0, 0, -65)
                # time.sleep(2)
                self.HG_DR_C.controlPump(1)
                time.sleep(2)
                self.HG_DR_C.moveAnInterval(0, 0, 45)
                self.HG_DR_C.move_to_angle(90, 15, 45)
                self.HG_DR_C.moveAnInterval(-80, 40, -50)
                self.HG_DR_C.controlPump(0)
                self.HG_DR_C.moveAnInterval(80, -40, 50)
                #self.HG_DR_C.move_to_angle(90, 15, 45)
                self.HG_DR_C.move_to_angle(0, 20, 5)
                self.move_time = 0
                self.grasp_state.publish(1)
            else:
                self.robot_move(3)

        if move_type == 4:
            if self.move_time == 0:
                    self.HG_DR_C.moveAnInterval(x, y, 0)
                    self.move_time += 1
                    time.sleep(2.0)
                    print("--------------", self.move_time)
            else:
                if self.move_time == 1:
                    self.move_time += 1
            if self.move_time == 2:
		self.HG_DR_C.moveAnInterval(x, y, 0)
                self.HG_DR_C.moveAnInterval(0, 0, -137)
                self.HG_DR_C.moveAnInterval(0, 0, -30)
                self.id = 0
                # self.HG_DR_C.moveAnInterval(0, 0, -65)
		        # time.sleep(2)
                self.HG_DR_C.controlPump(1)
                time.sleep(2)
                self.HG_DR_C.moveAnInterval(0, 0, 45)
                self.HG_DR_C.move_to_angle(90, 15, 45)
                self.HG_DR_C.moveAnInterval(-80, 40, -50)
                self.HG_DR_C.controlPump(0)
                self.HG_DR_C.moveAnInterval(80, -40, 50)
		        #self.HG_DR_C.move_to_angle(90, 15, 45)
                self.HG_DR_C.move_to_angle(0, 20, 5)
                self.move_time = 0
                self.grasp_state.publish(1)
            else:
                self.robot_move(4)

    def callback(self, data):
        print("grasp obj nub is:", data.data)
        if data.data == 1:  # 红苹果
            self.obj_color_pub.publish(6)
            self.robot_ready_pub.publish(8)
            time.sleep(2.0)
            self.robot_move(1)
        if data.data == 2:  # 橙子
            self.obj_color_pub.publish(5)
            self.robot_ready_pub.publish(8)
            time.sleep(2.0)
            self.robot_move(2)
        if data.data == 3:  # 青苹果
            self.obj_color_pub.publish(2)
            self.robot_ready_pub.publish(8)
            time.sleep(2.0)
            self.robot_move(3)
        if data.data == 4:  # 芒果
            self.obj_color_pub.publish(3)
            self.robot_ready_pub.publish(8)
            time.sleep(2.0)
            self.robot_move(4)

if __name__ == '__main__':
    grasp_object_demo = grasp_object()

