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
	#self.HG_DR_C.move_to_angle(0, 0, 30)
        self.obj_color = rospy.Publisher("object_color", Int64, queue_size=1)
        self.arm_state = rospy.Publisher("robotInitDone", Int64, queue_size=1)
        rospy.Subscriber("object_center", object_result_msg, self.callback)
        rospy.Subscriber("pump_state", Int64, self.control_pump)
        self.start_grasp = True
        self.grasp_high = rospy.get_param('~suck_z')
        self.grasp_objcet_color = rospy.get_param('~object_color')
        self.x_dis = rospy.get_param('~CamToSucker')
        self.y_dis = rospy.get_param('~CamToSucker_deviation')
        self.push_x = rospy.get_param('~drop_off_x')
        self.push_y = rospy.get_param('~drop_off_y')
        self.push_z = rospy.get_param('~drop_off_z')

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
            print("ready to grasp again!!")

    def callback(self, data):
        object_point = data.data
        print("get objcet_center_point :", object_point)
        if self.start_grasp:
            result = self.HG_DR_C.moveAnInterval(object_point[1]-self.x_dis, object_point[0]-self.y_dis, -self.grasp_high)
            time.sleep(2.0)
            #result = self.HG_DR_C.moveAnInterval(0, 0, -self.grasp_high)
            self.HG_DR_C.controlPump(1)
            print("control pump")
            result = self.HG_DR_C.moveAnInterval(0, 0, self.grasp_high)
            time.sleep(2.0)
	    self.HG_DR_C.moveAnInterval(self.push_x, self.push_y, -self.push_x)
            self.HG_DR_C.controlPump(0)
            self.start_grasp = False

    def listener(self):
        while self.start_grasp:
            self.obj_color.publish(self.grasp_objcet_color)
            self.arm_state.publish(8)
        # print("---------------pub data ----------------")
        rospy.spin()
 
if __name__ == '__main__':
    grasp_object_demo = grasp_object()
    grasp_object_demo.listener()

