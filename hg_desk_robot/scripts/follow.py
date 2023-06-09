#!/usr/bin/python
# -*- coding:utf8 -*-

import time
import math
import json
import rospy

from std_msgs.msg import Int32, String
from HG_DR_SDK import HG_DR_SDK
from HG_DR_KI import HG_DR_KI

from object_detect.msg import object_result_msg


HG_DR_C = HG_DR_SDK()
HG_DR_C.connectHG_DR()
HG_DR_C.calibrateJoint()
# arm_state: 1-ready  2-run
pub = rospy.Publisher('arm_state', Int32, queue_size=1)

def callback(data):
    pub.publish(2)
    if data.data == 'left':
        HG_DR_C.moveAnInterval(0,-20,0)	
	print("left")
    if data.data == 'right':
	HG_DR_C.moveAnInterval(0,20,0)
	print("right")
    if data.data == 'forward':
        HG_DR_C.moveAnInterval(20,0,0)
	print("forward")
    if data.data == 'back':
    	HG_DR_C.moveAnInterval(-20,0,0)
	print("back")
    time.sleep(2.0)
    pub.publish(1)
    
def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("object_direction",  String, callback)
    pub.publish(1)
    rospy.spin()
 
if __name__ == '__main__':
    listener()

