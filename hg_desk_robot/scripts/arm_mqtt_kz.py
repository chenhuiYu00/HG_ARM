#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import rospy

import paho.mqtt.client as mqtt
from collections import OrderedDict
import random
import ast
import json

from HG_DR_SDK import HG_DR_SDK
from castle_function import castle_function
#from ruamel import yaml
# sudo pip install ruamel.yaml

class arm():
    def __init__(self):
        rospy.init_node('arm_node', anonymous=False)
        #mqtt_host = rospy.get_param("~mqtt_host", "192.0.20.59")
        #mqtt_prot = rospy.get_param("~mqtt_port", "50000")
        self.MQTTHOST = '192.0.30.132'	# 服务器ip
        self.MQTTPORT = 50001	# 服务器端口
        self.mqttClient = mqtt.Client()
        #   Mqtt连接
        self.on_mqtt_connect()
        #   订阅mqtt话题
        self.on_subscribe()
        self.HG_HG1=HG_DR_SDK()
        self.HG_HG2=castle_function()
        #   初始化
        self.arm = False
        self.sub_msg = None
        #   初始化ros节点 
        rospy.on_shutdown(self.shutdown)

        self.rate = rospy.Rate(50)
        rospy.spin()
        while(1):
            pass
    
    #   发布Mqtt信息
    def mqtt_pub(self, data): 
        # print(self.sub_msg)
        if (data == 1):
            self.on_publish("/castlex_arm_feedback_msg", payload = self.arm_castlex_cmd1(), qos=0)
            time.sleep(1)
        elif (data == 0):
            self.on_publish("/castlex_arm_feedback_msg", payload = self.arm_castlex_cmd2(), qos=0)
            time.sleep(1)

        
    # 连接MQTT服务器
    def on_mqtt_connect(self):
        self.mqttClient.connect(self.MQTTHOST, self.MQTTPORT, 60)
        self.mqttClient.loop_start()
        print('连接成功')

    # publish mqtt 消息
    def on_publish(self, topic, payload, qos):
        self.mqttClient.publish(topic, payload, qos)

    # 对mqtt订阅消息处理函数
    def on_message_come(self, lient, userdata, msg):
	# python3 bytes转str
        self.sub_msg = json.loads(msg.payload)
        print(self.sub_msg)
        if self.sub_msg[0] == "Color_cen_detect":        #颜色识别
            if len(self.sub_msg) == 8:
                sen_data = []
                to_1 = self.sub_msg[1]
                to_2 = self.sub_msg[2]
                to_3 = self.sub_msg[3]
                to_4 = self.sub_msg[4]
                to_5 = self.sub_msg[5]
                to_6 = self.sub_msg[6]
                to_7 = self.sub_msg[7]
                sen_data[0] = "Current command completed"
                sen_data[1], sen_data[2], sen_data[3] = self.HG_HG2.Color_cen_detect(to_1, to_2, to_3, to_4, to_5, to_6, to_7)
                #  返回识别坐标
                self.on_publish("/castlex_arm_feedback_msg", payload = json.dumps(sen_data), qos=0)
            else:
                self.mqtt_pub(0)
        elif self.sub_msg[0] == "moveAnInterval":         #相对坐标
            if len(self.sub_msg) == 4:
                to_1 = self.sub_msg[1]
                to_2 = self.sub_msg[2]
                to_3 = self.sub_msg[3]
                self.HG_HG1.moveAnInterval(to_1, to_2, to_3)
                self.mqtt_pub(1)
            else:
                self.mqtt_pub(0)
        elif self.sub_msg[0] == "moveToStation":          #基坐标
            if len(self.sub_msg) == 4:
                to_1 = self.sub_msg[1]
                to_2 = self.sub_msg[2]
                to_3 = self.sub_msg[3]
                self.HG_HG1.moveToStation(to_1, to_2, to_3)
                self.mqtt_pub(1)
            else:
                self.mqtt_pub(0)
        elif self.sub_msg[0] == "connectHG_DR":           #机械臂连接
            if len(self.sub_msg) == 1:
                self.HG_HG1.connectHG_DR()
                self.mqtt_pub(1)
            else:
                self.mqtt_pub(0)
        elif self.sub_msg[0] == "calibrateJoint":         #初始化
            if len(self.sub_msg) == 1:
                self.HG_HG1.calibrateJoint()
                self.mqtt_pub(1)
            else:
                self.mqtt_pub(0)
        elif self.sub_msg[0] == "controlPump":            #气泵
            if len(self.sub_msg) == 2:
                to_1 = self.sub_msg[1]
                self.HG_HG1.controlPump(to_1)
                self.mqtt_pub(1)
            else:
                self.mqtt_pub(0)
        else:
            self.mqtt_pub(0)
            
  

    # mqtt subscribe 消息
    def on_subscribe(self):
        self.mqttClient.subscribe("/castlex_arm_msg", 0)
        self.mqttClient.on_message = self.on_message_come  # 消息到来处理函数

    # 向castlex回复当前指令完成
    def arm_castlex_cmd1(self):
        arm_data = "Current command completed"
        param = json.dumps(arm_data)
        return param

    # 向castlex回复当前指令完成
    def arm_castlex_cmd2(self):
        arm_data = ["Input error",0]
        param = json.dumps(arm_data)
        return param

    def shutdown(self):
        rospy.loginfo("Stopping the robot...")
        # Cancel any active goals
        rospy.sleep(2)
        

if __name__ == '__main__':
    try:
        arm()
        rospy.spin()

    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation finished.")
