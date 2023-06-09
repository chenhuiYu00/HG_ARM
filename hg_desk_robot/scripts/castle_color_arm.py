#!/usr/bin/python2
# -*- coding:utf8 -*-

import time
import math
import json
import rospy
from std_msgs.msg import Int32, Int64
from sensor_msgs.msg import Image

from HG_DR_SDK import HG_DR_SDK
from object_detect.msg import object_result_msg

class grasp_object:

    def __init__(self):

        self.id = 0
        self.x, self.y, self.side =0,0,0
        self.pump_state = 0
        rospy.init_node('listener', anonymous=True)

        # # 识别物体的中心坐标
        rospy.Subscriber("object_center", object_result_msg, self.arm_move_control)

        # # 订阅机械臂控制模式
        rospy.Subscriber("control_test", Int64, self.control_data)

        # # 控制气泵
        #rospy.Subscriber("usb_cam/image_raw", Image, self.control_pump)

        # # 手动控制气泵开闭
        rospy.Subscriber("pump_control", Int32, self.pump_control_data)

        self.control_state_data_pub = rospy.Publisher("control_arm", Int64, queue_size=1)

        self.HG_DR_C = HG_DR_SDK()

        # 连接机械臂
        self.HG_DR_C.connectHG_DR()
        # 机械臂归零
        self.HG_DR_C.calibrateJoint()
        self.HG_DR_C.moveAnInterval(-80, -70, 100)

        self.pump_state = 0
        self.control_pump(0)
        self.count = 0
        while(1):
                
            	if self.id == 1:
                    if self.count == 0:
                        # 像素坐标系相对于机械臂坐标系变换
                        x = 85*(self.y - 239.5)/self.side - 60  #60
                        y = -85*(self.x - 319.5)/self.side + 8  #17.5
                        z = 0 #162
                        time.sleep(1)
                        self.HG_DR_C.moveAnInterval(x, y, z)
                        time.sleep(1)
                        #self.pump_state = 1
                        #self.control_pump(1)
                        #time.sleep(3)
                        #print(self.HG_DR_C.get_pump_state())
                        self.count = self.count + 1
                    #self.id = 2
                elif self.id == 2:
                      if self.count == 1:
                          self.id = 0
                          time.sleep(1)
                          self.count = self.count + 1
                          # 第一次夾取後復位
                          if self.count == 2:
                              self.HG_DR_C.moveAnInterval(-145, -10, -125)
                              time.sleep(1)
                              self.HG_DR_C.calibrateJoint()
                              time.sleep(1)
                              self.HG_DR_C.moveAnInterval(-80, -70, 100)
                              time.sleep(1)
                              self.count = 0


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

 
if __name__ == '__main__':
    grasp_object_demo = grasp_object()
    #grasp_object_demo.listener()

