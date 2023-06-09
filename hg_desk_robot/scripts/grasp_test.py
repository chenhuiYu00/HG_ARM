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

        rospy.on_shutdown(self.cleanup)
        self.id = 0
        self.x, self.y, self.side =0,0,0
        rospy.init_node('listener', anonymous=True)

        # # 识别物体的中心坐标
        rospy.Subscriber("object_center", object_result_msg, self.arm_move_control)

        # # 订阅气泵状态
        rospy.Subscriber("control_test", Int64, self.control_data)



        self.HG_DR_C = HG_DR_SDK()

        # 连接机械臂
        self.HG_DR_C.connectHG_DR()
        #   机械臂归零
        self.HG_DR_C.calibrateJoint()
        self.HG_DR_C.moveAnInterval(0, 0, 120)
        # time.sleep(3)

           
        # self.obj_color = rospy.Publisher("object_color", Int64, queue_size=1)

        # #   发布机械臂初始化完成话题
        # self.arm_state = rospy.Publisher("robotInitDone", Int64, queue_size=1)



        # self.start_grasp = True
        # # 机械臂抓取高度
        # self.grasp_high = rospy.get_param('~suck_z')

        # # 相机相对于爪子的x偏移量
        # self.x_dis = rospy.get_param('~CamToSucker')
        # # 相机相对于爪子的y偏移量
        # self.y_dis = rospy.get_param('~CamToSucker_deviation')

        # # 机械臂放置x坐标
        # self.push_x = rospy.get_param('~drop_off_x')
        # # 机械臂放置y坐标
        # self.push_y = rospy.get_param('~drop_off_y')
        # # 机械臂放置z坐标
        # self.push_z = rospy.get_param('~drop_off_z')

        # self.HG_DR_C.moveAnInterval(20, 20, 0)


        while(1):
                #print(self.x, self.y, self.side)
            	if self.id == 1:
                    x = 85*(self.y - 239.5)/self.side - 50
                    y = -85*(self.x - 319.5)/self.side + 2
                    print(x,y)
                    self.HG_DR_C.moveAnInterval(x, y, -68)
                    self.id = 0
                    #self.HG_DR_C.moveAnInterval(0, 0, -65)
                    self.HG_DR_C.controlPump(1)
                    time.sleep(1)
                    self.HG_DR_C.moveAnInterval(-x, -y, 68)
                    self.HG_DR_C.controlPump(0)

        #break
		#rospy.spin()


    #   机械臂控制
    def arm_move_control(self, data):
        self.x = data.data[0]
        self.y = data.data[1]
        self.side = data.data[2]

    #   机械臂控制
    def control_data(self, data):
        self.id = data.data

    #   控制气泵
    def control_pump(self, data):
        #   打开气泵
        if data.data == 1:
            self.HG_DR_C.controlPump(1)
            time.sleep(1.0)
            print("Pump start!!")
        # 关闭气泵
        if data.data == 0:
            self.HG_DR_C.controlPump(0)
            time.sleep(1.0)
            print("Pump end!!")
        # 参数初始化
        if data.data == 2:
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

