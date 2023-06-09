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

rospy.init_node('listener', anonymous=True)
port_name = rospy.get_param("~port_name", "/dev/ttyACM0")
HG_DR_SDK.prot_name = port_name
HG_DR_C = HG_DR_SDK()
HG_DR_C.connectHG_DR()

def callback(data):
    state = int(data.data)
    print(state)
    result= HG_DR_C.controlPump(state)
	
    
def listener():
    rospy.Subscriber("pump_state", Int32, callback)
    rospy.spin()
 
if __name__ == '__main__':
    listener()

