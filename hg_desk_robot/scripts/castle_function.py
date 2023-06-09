#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import time
import ast
import roslib
import actionlib
from actionlib_msgs.msg import *
#from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

from geometry_msgs.msg import Pose, Point, Quaternion, Twist
from std_msgs.msg import Float32, Int32, Int64, Int32MultiArray, Float32MultiArray, Bool
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu, Image, RegionOfInterest

import cv2
import numpy as np
import math as m
from cv_bridge import CvBridge, CvBridgeError
from object_detect.msg import object_result_msg
from HG_DR_SDK import HG_DR_SDK

import math
import json

class castle_function:

    def __init__(self):
        
        #初始化
        self.iot_bz = False
        self.ul_bz, self.sp_bz = None, None
        #订阅物联网是否启动
        rospy.Subscriber("/iot_control_state", Bool, self.iot_control_state)
        rospy.Subscriber("/spray_kill", Int32, self.sp_state)
        rospy.Subscriber("/ultraviolet_disinfection", Int32, self.ul_state)
        self.iot_data = Int32MultiArray()
        #物联网
        self.iot_pub = rospy.Publisher("/iot_control", Int32MultiArray, queue_size=1)
        #货舱控制
        #self.Curtain_pub = rospy.publisher('/Warehouse_control', Int32, queue_size=1)
        #喷雾消杀
        self.spray_kill_pub = rospy.Publisher("/spray_kill", Int32, queue_size=1)
        #紫外消杀
        self.ultraviolet_disinfectionl_pub = rospy.Publisher("/ultraviolet_disinfection", Int32, queue_size=1)


    #导航到目标点
    def Target_point(self, Target_x, Target_y, Target_w):

        # 订阅move_base服务器的消息
        self.ac = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        rospy.loginfo("Waiting for move_base action server...")
        self.ac.wait_for_server(rospy.Duration(60))
        rospy.loginfo("Connected to move base server")

        # 初始化goal为MoveBaseGoal类型
        goal = MoveBaseGoal()
        # 使用map的frame定义goal的frame id
        goal.target_pose.header.frame_id = 'map'
        # 设置时间戳
        goal.target_pose.header.stamp = rospy.Time.now()
        # 设置目标位置
        goal.target_pose.pose.position.x = Target_x
        goal.target_pose.pose.position.y = Target_y
        goal.target_pose.pose.orientation.w = Target_w
        rospy.loginfo("Sending goal")
        # 机器人移动
        self.move(goal)

    def move(self, goal):
        self.ac.send_goal(goal)
        # 设定5分钟的时间限制
        finished_within_time = self.ac.wait_for_result(rospy.Duration(300))
        # 如果5分钟之内没有到达，放弃目标
        if not finished_within_time:
            self.ac.cancel_goal()
            rospy.loginfo("Timed out achieving goal")
        else:
            state = self.ac.get_state()
            if state == GoalStatus.SUCCEEDED:
                #   发布导航成功的flag
                rospy.loginfo("You have reached the goal!")

    def shutdown(self):
        rospy.loginfo("Stopping the robot...")
        self.runing = 0
        # Cancel any active goals
        self.ac.cancel_goal()
        rospy.sleep(2)

    #灯1
    def Light1(self, data):
        self.iot_bz = False
        rate = rospy.Rate(10)
        while not self.iot_bz:
         self.iot_data.data = [1,data]
         self.Light1_data = self.iot_data
         self.iot_pub.publish(self.Light1_data)
         rospy.loginfo(self.Light1_data)
         rate.sleep()

    #灯2
    def Light2(self, data):
        self.iot_bz = False
        rate = rospy.Rate(10)
        while not self.iot_bz:
         self.iot_data.data = [2,data]
         self.Light2_data = self.iot_data
         self.iot_pub.publish(self.Light2_data)
         rospy.loginfo(self.Light2_data)
         rate.sleep()
    #灯3
    def Light3(self, data):
        self.iot_bz = False
        rate = rospy.Rate(10)
        while not self.iot_bz:
         self.iot_data.data = [3,data]
         self.Light3_data = self.iot_data
         self.iot_pub.publish(self.Light3_data)
         rospy.loginfo(self.Light3_data)
         rate.sleep()

    #窗帘
    def Curtain(self, data):
        self.iot_bz = False
        rate = rospy.Rate(10)
        while not self.iot_bz:
         self.iot_data.data = [6,data]
         self.Curtain_data = self.iot_data
         self.iot_pub.publish(self.Curtain_data)
         rospy.loginfo(self.Curtain_data)
         rate.sleep()

    #物联网标志
    def iot_control_state(self, iot_state):
        self.iot_bz = iot_state.data

    #喷雾消杀
    def spray_kill(self, data):
        rate = rospy.Rate(10)
        while not self.sp_bz:
         self.spray_kill_pub.publish(data)
         rospy.loginfo('sp')
         rospy.loginfo(data)
         if self.sp_bz == 0 or self.sp_bz == 1:
             break
         rate.sleep()

    #sp标志
    def sp_state(self, sp_state):
        self.sp_bz = sp_state.data

    #紫外消杀
    def ultraviolet_disinfectionl(self, data):
        rate = rospy.Rate(10)
        while not self.ul_bz:
         self.ultraviolet_disinfectionl_pub.publish(data)
         rospy.loginfo('ul')
         rospy.loginfo(data)
         if self.ul_bz == 0 or self.ul_bz == 1:
             break
         rate.sleep()

    #ul标志
    def ul_state(self, ul_state):
        self.ul_bz = ul_state.data

    #颜色控制
    def Move_Color(self, mod, h_hsv_b, h_hsv_s, h_hsv_v, l_hsv_h, l_hsv_s, l_hsv_v):
        self.mod = mod
        self.tag1 = 0
        self.tagf = 0
        self.high_Color = np.array([h_hsv_b, h_hsv_s, h_hsv_v])
        self.low_Color = np.array([l_hsv_h, l_hsv_s, l_hsv_v])
        rospy.on_shutdown(self.cleanup)
        self.bridge = CvBridge()
        self.HG_DR_C = HG_DR_SDK()
        # 连接机械臂
        self.HG_DR_C.connectHG_DR()
        # 创建cv_bridge话题
        # 创建图像发布话题
        self.image_pub = rospy.Publisher("cv_bridge_image", Image, queue_size=1)
        # 创建识别物体中心坐标的发布话题
        self.pub = rospy.Publisher('object_center', object_result_msg, queue_size=10)
        self.control_pub = rospy.Publisher("control_test", Int64, queue_size=1)   
        
        rate = rospy.Rate(10) # 发布频率为10hz

        self.pub1 = rospy.Publisher('DetectDone', Int64, queue_size=10)   

        rospy.loginfo("object_detect is started.. \n Please subscribe the ROS image.")
        #   机械臂初始化位姿成功时，进行图像识别
        #time.sleep(1)
        self.image_sub = rospy.Subscriber("/usb_cam/image_raw", Image, self.image_callback, queue_size=1)
        # 延时1s
        time.sleep(1)

        #   发布识别成功的信号
        if self.tag1 == 2 and self.center_ob != [0, 0] and self.tagf != 1 and self.side_judge:
            self.pub1.publish(self.tag1)
            time.sleep(1)
            self.pub.publish(self.center_ob)
            time.sleep(1)
            #发布机器臂移动
            self.control_pub.publish(1)

#####################      获取物体的中心坐标回调函数　　   ######################
    def image_callback(self, data):
        # 使用cv_bridge将ROS的图像数据转换成OpenCV的图像格式
        try:
            self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")     
            frame = np.array(self.cv_image, dtype=np.uint8)
            self.frame_rgb = frame
        except CvBridgeError as e:
            print (e)

        # 将图像从RGB转成灰度图
        self.gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
        #　将图像从RGB转成HSV
        self.hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 

        #  识别物体并获取其像素中心坐标
        morph = self.Get_contour_Color()
        self.Color = self.Get_Color()

        points = self.Find_contour_Color(morph)
        if len(points) == 2:
            pass
        else:
            self.px = 0 # 初始化px的值
            self.px = self.pxPoint(points)
            self.mask = self.Draw_contour(points)

            # 显示处理的图像
            cv2.imshow("mask", self.mask)
            cv2.imshow("color", self.Color)
            cv2.waitKey(1)

            # 边长判断
            self.side_judge = ((50 <= self.px and self.px <= 520) and (50 <= self.st[0] and self.st[0] <= 520) and (50 <= self.st[1] and self.st[1] <= 520))

            # 过滤不在范围内的颜色噪点(设定识别的边长阈值),物体在图像中的像素边长
            if self.side_judge:
                center_x, center_y = self.Get_center(points)
                if self.px == 0:
                    self.tagf = 1
                else:
                    self.center_ob = [center_x, center_y, self.px]
                    #print(self.center_ob)
                    self.tag1 = 2
                    self.image_pub.publish(self.bridge.cv2_to_imgmsg(self.cv_image, "bgr8"))                
            else:
                pass

    #   获取颜色的阈值范围
    def Get_Color(self):
        if self.mod == 0:
            mask = cv2.inRange(self.hsv, self.low_Color, self.high_Color)
            Color = cv2.bitwise_and(self.hsv, self.hsv,mask=mask)
        elif self.mod == 1:
            mask = cv2.inRange(self.frame_rgb, self.low_Color, self.high_Color)
            Color = cv2.bitwise_and(self.frame_rgb, self.frame_rgb,mask=mask)
        return Color


    #将区域进行二值化处理 
    def Get_contour_Color(self):
        #change to gray
        Color = self.Get_Color()
        Color_gray = cv2.cvtColor(Color, cv2.COLOR_BGR2GRAY)
        
        #binaryzation
        _, thresh = cv2.threshold(Color_gray, 10, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        img_morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, (3,3))
        return img_morph

    #获取中心区域轮廓及坐标 
    def Find_contour_Color(self,frame):
        img_cp = self.Get_contour_Color()
        _, cnts, _ = cv2.findContours(img_cp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(cnts) == 0:
            img_boxpoints = (0, 0)
        else:
            cnt_second = sorted(cnts, key=cv2.contourArea, reverse=True)[0] #当没有检测到图像的时候报错，要修改
            box =cv2.minAreaRect(cnt_second)    #生成最小外接矩形
            img_boxpoints = np.int0(cv2.boxPoints(box))  #返回最小外接矩形4 个顶点
            # print img_boxpoints
        return img_boxpoints

    #绘制轮廓
    def Draw_contour(self,points):
        mask = np.zeros(self.gray.shape,np.uint8)
        if len(points) == 0:
            pass
        else:
            cv2.drawContours(mask,[points],-1,255,2)
        return mask

    #获取中心位置
    def Get_center(self,points):
        # global center
        if len(points) == 0:
            cen_tag = 0
            center = (0, 0)
        else:
            cen_tag = 1
            p1x,p1y = points[0,0],points[0,1]
            p3x,p3y = points[2,0],points[2,1]
            center_x,center_y = (p1x+p3x)/2,(p1y+p3y)/2
            center = (center_x,center_y)
        return center

    #绘制中心点
    def Draw_center(self,center,mask):
        # global mask1        
        if cen_tag == 0:
            pass
        else:
            cv2.circle( mask,center,1,(255,255,255),2)


############################    计算像素与实际距离之比     ##############################################     
    def pxPoint(self, data):
        self.st = []
        for i in range(0, 4):
            if i <= 2:
                s = m.sqrt((data[i][0] - data[i+1][0])**2 + (data[i][1] - data[i+1][1])**2)
                self.st = np.append(self.st, s)
            else:
                s = m.sqrt((data[i][0] - data[0][0])**2 + (data[i][1] - data[0][1])**2)
                self.st = np.append(self.st, s)
        sum = 0

        if  self.st[0] >  self.st[1]:
            self.s = self.st[0]
        else:
            self.s = self.st[1]

        return self.s

    def cleanup(self):
        print ("Shutting down vision node.")
        cv2.destroyAllWindows()

