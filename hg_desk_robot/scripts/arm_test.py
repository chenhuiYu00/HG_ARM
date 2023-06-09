#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from HG_DR_SDK import HG_DR_SDK
import rospy
from time import *
rospy.init_node('arm_test', log_level=rospy.INFO)




dr = HG_DR_SDK()
dr.connectHG_DR()
dr.calibrateJoint()
# dr.moveAnInterval(20.5, 20.5, 20.5)
dr.moveToStation(180, 50, 230)
dr.controlPump(1)
sleep(5)
dr.controlPump(0)


