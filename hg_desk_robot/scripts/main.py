#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from HG_DR_SDK import HG_DR_SDK
from rpi_function import rpi_function
from arm_mqtt_control import arm_mqtt_control
import rospy

rospy.init_node('main', log_level=rospy.INFO)

# ************arm_control**********
# dr = HG_DR_SDK()
# dr.connectHG_DR()
# dr.calibrateJoint()
# dr.moveAnInterval(20.5, 20.5, 20.5)
# dr.moveToStation(180, 60, 130)
# dr.controlPump(1)
# rospy.sleep(6)
# dr.controlPump(0)

# ************castle_control**********
cf = rpi_function()
color_x, color_y = cf.Color_coor_detect(1,219,148,255,170,90,0)
print(color_x, color_y)
color_x, color_y, ss = cf.Color_cen_detect(1,219,148,255,170,90,0)
print(color_x, color_y, ss)

# ************arm_mqtt_control**********
# qq = arm_mqtt_control()
# xx = qq. on_mqtt_connect("192.168.170.160", 50001)
# print(xx)
# xx = qq.arm_castlex_mqtt_read()
# print(xx)
# qq.arm_castlex_mqtt_send("执行完毕")
