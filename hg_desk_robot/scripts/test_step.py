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

from std_msgs.msg import Int32
from HG_DR_SDK import HG_DR_SDK
from HG_DR_KI import HG_DR_KI

from object_detect.msg import object_result_msg

rospy.init_node('listener', anonymous=True)
port_name = rospy.get_param("~port_name", "/dev/ttyACM0")
HG_DR_SDK.prot_name = port_name
HG_DR_C = HG_DR_SDK()
HG_DR_C.connectHG_DR()
HG_DR_C.calibrateJoint()

def callback(data):
    if data.data == 1:
	#HG_DR_C.controlPump(1)
	time.sleep(1.0)
        HG_DR_C.move_to_angle(90, 30, 15)
	HG_DR_C.moveAnInterval(-80, 0, 0)
	#HG_DR_C.controlPump(0)
	HG_DR_C.moveAnInterval(80, 0, 0)
	HG_DR_C.move_to_angle(0, 45, 45)
def listener():
    rospy.Subscriber("step_move",  Int32, callback)
    rospy.spin()
 
if __name__ == '__main__':
    listener()



