#!/usr/bin/python
# -*- coding:utf8 -*-
import os
import sys
import time
import math
import json
import tty, termios
import roslib
roslib.load_manifest('hg_desk_robot')
import rospy  


from std_msgs.msg import Int32
from HG_DR_SDK import HG_DR_SDK
from HG_DR_KI import HG_DR_KI

HG_DR_C = HG_DR_SDK()
HG_DR_C.connectHG_DR()
HG_DR_C.calibrateJoint()


move_step = 20

def keyboardLoop():  
    #初始化  
    rospy.init_node('key_controller')  
    rate = rospy.Rate(rospy.get_param('~hz', 1))  
    #读取按键循环  
    while not rospy.is_shutdown():  
        fd = sys.stdin.fileno()  
        old_settings = termios.tcgetattr(fd)  
        #不产生回显效果  
        old_settings[3] = old_settings[3] & ~termios.ICANON & ~termios.ECHO  
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)  
  
        if ch == 'w' or ch == 'W':  
            print("forward")
	    HG_DR_C.moveAnInterval(move_step,0,0)
        elif ch == 's' or ch == 'S':  
            print("back") 
	    HG_DR_C.moveAnInterval(-move_step,0,0)
        elif ch == 'a' or ch == 'A':  
            print("left") 
	    HG_DR_C.moveAnInterval(0,-move_step,0)
        elif ch == 'd' or ch == 'D':  
            print("right")  
	    HG_DR_C.moveAnInterval(0,move_step,0)
        elif ch == 'i' or ch == 'I':
            print("down")
	    HG_DR_C.moveAnInterval(0,0,-move_step)
        elif ch == 'u' or ch == 'U':
            print("up")
	    HG_DR_C.moveAnInterval(0,0,move_step)
	elif ch == 't' or ch == 'T':
	    HG_DR_C.controlPump(1)
	    print("open")
	elif ch == 'y' or ch == 'Y':
	    HG_DR_C.controlPump(0)
	    print("close")
	elif ch == 'f' or ch == 'F':
	    move_fast()
	elif ch == 'l' or ch == 'L':
	    move_slow()
	elif ch == 'q' or ch == 'Q':
	    print("exit")
	    exit()
        else:  
            stop_robot()  

        rate.sleep()  
        #停止机器人  
        stop_robot()

def move_fast():
    global move_step
    if move_step < 60:
        move_step += 10
    else:
	pass
    print(move_step)

def move_slow():
    global move_step
    if move_step < 10:
        pass
    else:
	move_step -= 10
    print(move_step)

def stop_robot():
    HG_DR_C.moveAnInterval(0,0,0)  
    print("stop")


if __name__ == '__main__':  
    try:  
        keyboardLoop()  
    except rospy.ROSInterruptException:  
        pass 
