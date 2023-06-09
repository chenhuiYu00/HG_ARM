#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import time
from actionlib_msgs.msg import *
from std_msgs.msg import Float32, Int32, Int64, Int32MultiArray, Float32MultiArray, Bool, String
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu, Image, RegionOfInterest

import cv2
import numpy as np
import math as m
from cv_bridge import CvBridge, CvBridgeError
from object_detect.msg import object_result_msg
#from playsound import playsound
import math
import json

class rpi_function:

    def __init__(self):
        
        #初始化
        self.iot_bz = False
        self.ul_bz, self.sp_bz = None, None
        self.id_cargo_data, self.Face_id_data = None, None




    #颜色控制  mod:颜色模式，mod == 0:hsv, mod == 1:rgb
    def Color_coor_detect(self, mod, h_hsv_h, h_hsv_s, h_hsv_v, l_hsv_h, l_hsv_s, l_hsv_v):
        self.mod = mod
        self.tag1 = 0
        self.tagf = 0
        self.high_Color = np.array([h_hsv_h, h_hsv_s, h_hsv_v])
        self.low_Color = np.array([l_hsv_h, l_hsv_s, l_hsv_v])
        rospy.on_shutdown(self.cleanup)
        self.bridge = CvBridge()
        #self.HG_DR_C = HG_DR_SDK()
        # 连接机械臂
        #self.HG_DR_C.connectHG_DR()
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
            #self.pub.publish(self.center_ob)
            #time.sleep(1)
            #发布机器臂移动
            #self.control_pub.publish(1)
            x = 85*(self.center_ob[1] - 239.5)/self.center_ob[2] - 60  #60
            y = -85*(self.center_ob[0] - 319.5)/self.center_ob[2] + 8  #17.5
        else:
            x, y = None, None
        return x, y

    #颜色控制(返回面积)  mod:颜色模式，mod == 0:hsv, mod == 1:rgb
    def Color_cen_detect(self, mod, h_hsv_h, h_hsv_s, h_hsv_v, l_hsv_h, l_hsv_s, l_hsv_v):
        self.mod = mod
        self.tag1 = 0
        self.tagf = 0
        self.high_Color = np.array([h_hsv_h, h_hsv_s, h_hsv_v])
        self.low_Color = np.array([l_hsv_h, l_hsv_s, l_hsv_v])
        rospy.on_shutdown(self.cleanup)
        self.bridge = CvBridge()
        #self.HG_DR_C = HG_DR_SDK()
        # 连接机械臂
        #self.HG_DR_C.connectHG_DR()
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
            #self.pub.publish(self.center_ob)
            #time.sleep(1)
            #发布机器臂移动
            #self.control_pub.publish(1)
            x = 85*(self.center_ob[1] - 239.5)/self.center_ob[2] - 60  #60
            y = -85*(self.center_ob[0] - 319.5)/self.center_ob[2] + 8  #17.5
        else:
            x, y = None, None
            self.area = None
        return x, y, self.area

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
        # mod == 0:hsv, mod == 1:rgb
        if self.mod == 0:
            mask = cv2.inRange(self.hsv, self.low_Color, self.high_Color)
            Color = cv2.bitwise_and(self.hsv, self.hsv,mask=mask)
            Color = cv2.cvtColor(Color, cv2.COLOR_HSV2BGR)
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
            self.area = abs(p1x-p3x)*abs(p1y-p3y)
        return center

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
