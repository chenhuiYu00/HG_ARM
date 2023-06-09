#!/usr/bin/env python
# -*- coding: utf-8 -*-

import roslib
import time
import rospy
from geometry_msgs.msg import Pose, Point, Quaternion, Twist
from std_msgs.msg import Float32MultiArray, Int32, Float32, Int64
from sensor_msgs.msg import Image, CompressedImage

import paho.mqtt.client as mqtt
from collections import OrderedDict
import random
import ast
import json

#from ruamel import yaml
# sudo pip install ruamel.yaml

class arm():
    def __init__(self):
        rospy.init_node('arm_node', anonymous=False)
        mqtt_host = rospy.get_param("~mqtt_host", "192.0.20.59")
        mqtt_prot = rospy.get_param("~mqtt_port", "50000")
        self.MQTTHOST = mqtt_host	# 服务器ip
        self.MQTTPORT = mqtt_prot	# 服务器端口
        self.mqttClient = mqtt.Client()
        #   Mqtt连接
        self.on_mqtt_connect()
        #   订阅mqtt话题
        self.on_subscribe()

        self.action, self.control_state_data = False, 0
        self.castlex, self.arm = False, False
        self.sub_name, self.sub_dir, self.sub_action, self.sub_feedback, self.sub_msg = None, None, None, None, None
        #   初始化ros节点
        
        rospy.on_shutdown(self.shutdown)

        # 机械臂话题
        rospy.Subscriber('/grasp_state', Int32, self.arm_grasp_state)
        self.arm_target = rospy.Publisher("grasp_target", Int32, queue_size=1)
        rospy.Subscriber('/control_arm', Int64, self.control_state)
        self.robotInitDone_pub = rospy.Publisher("robotInitDone", Int64, queue_size=1)
        self.control_pub = rospy.Publisher("control_test", Int64, queue_size=1)
        #   订阅图像话题
        rospy.Subscriber('/usb_cam/image_raw', Image, self.mqtt_data)
        rospy.Subscriber('/usb_cam/image_raw/compressed', CompressedImage, self.mqtt_pub)

        self.rate = rospy.Rate(50)
        rospy.spin()
    
    def control_state(self, data):
        self.control_state_data = data.data


    def arm_grasp_state(self, data):
        if data.data == 1:
            self.arm = True

    def mqtt_data(self, pose):
        if self.sub_action == "loading complete" and self.sub_feedback == 1:
            self.arm = False
        if self.sub_action == "loading" and self.sub_feedback == 0:
            self.castlex = True
        elif self.sub_action == "loading" and self.sub_feedback == 1:
            self.castlex = False
        if self.action:
            if self.control_state_data == 0:
                self.robotInitDone_pub.publish(8)
                time.sleep(5)
                self.control_pub.publish(1)
                time.sleep(3)
                self.control_state_data = -1
            elif self.control_state_data == 1:
                print("done")
                self.action = False
                self.arm = True
                self.control_state_data = 0
            
    #   发布Mqtt信息
    def mqtt_pub(self, data): 
        # print(self.sub_msg)
        if (self.castlex):
            self.on_publish("/castlex_arm_msg", self.arm_castlex_reply(), 0)
            self.action = True
            time.sleep(1)
        if self.arm:
            self.on_publish("/castlex_arm_msg", self.arm_castlex_cmd(), 0)
            time.sleep(1)
        
    # 连接MQTT服务器
    def on_mqtt_connect(self):
        self.mqttClient.connect(self.MQTTHOST, self.MQTTPORT, 60)
        self.mqttClient.loop_start()

    # publish mqtt 消息
    def on_publish(self, topic, payload, qos):
        #print("pub msg: %s to %s" % (payload, topic))
        self.mqttClient.publish(topic, payload, qos)

    # 对mqtt订阅消息处理函数
    def on_message_come(self, lient, userdata, msg):
	# python3 bytes转str
        self.sub_msg = json.loads(msg.payload.encode('utf-8'))#str(msg.payload, 'utf-8')
	print(self.sub_msg)
	    # python3 str转字典
        #self.sub_msg = ast.literal_eval(self.sub_msg)
        if len(self.sub_msg) == 5:
            self.sub_name, self.sub_dir, self.sub_action, self.sub_feedback = self.sub_msg['name'], self.sub_msg['dir'], self.sub_msg['ation'], self.sub_msg['feedback']
        else:
            pass

    # mqtt subscribe 消息
    def on_subscribe(self):
        self.mqttClient.subscribe("/castlex_arm_msg", 0)
        self.mqttClient.on_message = self.on_message_come  # 消息到来处理函数

    # 向机械臂发送请求装货指令
    def arm_castlex_reply(self):
        json_dict = OrderedDict()
        json_dict["name"] = "arm"
        json_dict["dir"] = "castlex"
        json_dict["ation"] = "loading"
        json_dict["error"] = "null"
        json_dict["feedback"] = 1
        param = json.dumps(json_dict)
        return param

    # 向机械臂回复收到装货完成指令
    def arm_castlex_cmd(self):
        json_dict = OrderedDict()
        json_dict["name"] = "arm"
        json_dict["dir"] = "castlex"
        json_dict["ation"] = "loading complete"
        json_dict["error"] = "null"
        json_dict["feedback"] = 0
        param = json.dumps(json_dict)
        return param

    def shutdown(self):
        rospy.loginfo("Stopping the robot...")
        self.runing = 0 
        # Cancel any active goals
        self.ac.cancel_goal()
        rospy.sleep(2)
        

if __name__ == '__main__':
    try:
        arm()
        rospy.spin()

    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation finished.")
