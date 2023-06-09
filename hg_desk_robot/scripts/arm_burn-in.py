#!/usr/bin/python2
# -*- coding:utf8 -*-

import time
import math
import json
import rospy
from std_msgs.msg import Int32, Int64
from sensor_msgs.msg import Image

from HG_DR_SDK import HG_DR_SDK
from HG_DR_KI import HG_DR_KI
from object_detect.msg import object_result_msg

class grasp_object:

    def __init__(self):

        rospy.on_shutdown(self.cleanup)
        self.id = 0
        self.x, self.y, self.side =0,0,0
        self.pump_state = 0
        rospy.init_node('listener', anonymous=True)

        # # 识别物体的中心坐标
        rospy.Subscriber("object_center", object_result_msg, self.arm_move_control)

        # # 订阅机械臂控制模式
        rospy.Subscriber("control_test", Int64, self.control_data)

        # # 手动控制气泵开闭
        rospy.Subscriber("pump_control", Int32, self.pump_control_data)

        self.jqbkz_pub = rospy.Publisher("jqbkz", Int64, queue_size=1)  # 发布

        self.control_state_data_pub = rospy.Publisher("control_arm", Int64, queue_size=1)

        self.HG_DR_C = HG_DR_SDK()

        # 连接机械臂
        self.HG_DR_C.connectHG_DR()
        #   机械臂归零
        self.HG_DR_C.calibrateJoint()
        self.HG_DR_C.moveAnInterval(20, 0, 110)
        self.pump_state = 0
        self.control_pump(0)
        self.count = 0
        i = 0
        while(1):
            
            if i ==  0:
                x, y, z = 10, 100, -130
                i = i + 1
            elif i == 1:
                x, y, z = 10, 0, -140
                i = i + 1
            elif i == 2:
                x, y, z = -20, -90, -130
                i = 0

            time.sleep(1)

            self.HG_DR_C.moveAnInterval(x, y, z)
            time.sleep(1)

            self.pump_state = 1
            self.control_pump(1)
            time.sleep(3)
            print(self.HG_DR_C.get_pump_state())

            self.HG_DR_C.moveAnInterval(0, 0, 60)
            time.sleep(1)
            self.HG_DR_C.moveAnInterval(-x, -y, -z-60)
            time.sleep(1)
            self.pump_state = 0
            self.control_pump(0)
            time.sleep(3)
            print(self.HG_DR_C.get_pump_state())

            self.HG_DR_C.moveAnInterval(x, y, z)
            time.sleep(1)
            self.HG_DR_C.moveAnInterval(0, 0, 60)
            time.sleep(1)
            self.HG_DR_C.moveAnInterval(-x, -y, -z-60)
            time.sleep(1)

            # 第一次夾取後復位
            self.HG_DR_C.moveAnInterval(-175, -10, -110)
            time.sleep(1)
            self.HG_DR_C.calibrateJoint()
            self.HG_DR_C.moveAnInterval(20, 0, 110)
            time.sleep(1)





    #   机械臂控制
    def arm_move_control(self, data):
        self.x = data.data[0]
        self.y = data.data[1]
        self.side = data.data[2]

    #   机械臂控制
    def control_data(self, data):
        self.id = data.data

    #   监听气泵控制状态
    def pump_control_data(self, data):
        self.pump_state = data.data

    #   控制气泵
    def control_pump(self, data):
        #   打开气泵
        if self.pump_state == 1:
            result = self.HG_DR_C.controlPump(1)
            time.sleep(0.1)
            print("Pump start!!", result)
        # 关闭气泵
        elif self.pump_state == 0:
            self.HG_DR_C.controlPump(0)
            time.sleep(0.1)
            print("Pump end!!")
        # 参数初始化
        elif self.pump_state == 2:
            self.start_grasp = True
            print("ready to grasp again!!")


    #   根据识别坐标完成机械臂的控制
    def callback(self, data):
        object_point = data.data
        print("get objcet_center_point :", object_point)
        if self.start_grasp:
            #   先走xy坐标
            result = self.HG_DR_C.moveAnInterval(object_point[1]-self.x_dis, object_point[0]-self.y_dis, 0)
            time.sleep(2.0)
            #   再走z坐标（往下）
            result = self.HG_DR_C.moveAnInterval(0, 0, -self.grasp_high)
            #   控制气泵闭合（吸取）
            self.HG_DR_C.controlPump(1)
            print("control pump")
            #   走z坐标（往上）
            result = self.HG_DR_C.moveAnInterval(0, 0, self.grasp_high)
            time.sleep(2.0)
            #   放置物资
            self.HG_DR_C.moveAnInterval(self.push_x, self.push_y, -self.push_x)
             #   控制气泵松开
            self.HG_DR_C.controlPump(0)
            self.start_grasp = False

    def listener(self):
        while self.start_grasp:
            self.arm_state.publish(8)
        # print("---------------pub data ----------------")
        rospy.spin()
 
    def cleanup(self):
        print("Shutting down vision node.")
        # cv2.destroyAllWindows()

if __name__ == '__main__':
    grasp_object_demo = grasp_object()
    #grasp_object_demo.listener()

