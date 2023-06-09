#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
from castle_function import castle_function
from HG_DR_SDK import HG_DR_SDK

class castle_cs:

    def __init__(self):
        rospy.init_node('castlex_cs_node', anonymous=False)
        #x = castle_function().rgb2hsv(203, 0, 0)
        #rospy.loginfo(x)
        #x = castle_function().rgb2hsv(255, 100, 106)
        #rospy.loginfo(x)
        #castle_function().Move_Color(179, 255, 255, 0, 155, 203)
        #castle_function().Move_Color(179, 155, 255, 0, 255, 203)
        castle_function().Move_Color(1, 106, 100, 255, 0, 0, 203)


if __name__ == '__main__':
    try:
        castle_cs()
        rospy.spin()

    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation finished.")
