#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import paho.mqtt.client as mqtt
from collections import OrderedDict
import random
import ast
import json

#from ruamel import yaml
# sudo pip install ruamel.yaml

class arm_mqtt_control():
    def __init__(self):
        # self.MQTTHOST = '192.0.30.132'	# 服务器ip
        # self.MQTTPORT = 50001	# 服务器端口
        self.mqttClient = mqtt.Client()
        # #   Mqtt连接
        # self.on_mqtt_connect()
        # #   订阅mqtt话题
        # self.on_subscribe()

        
    # 连接MQTT服务器
    def on_mqtt_connect(self, MQTTHOST, MQTTPORT):
        self.mqttClient.connect(MQTTHOST, MQTTPORT, 60)
        self.mqttClient.loop_start()
        print('连接成功')
        self.on_subscribe()
        return True

    # publish mqtt 消息
    def on_publish(self, topic, payload, qos):
        self.mqttClient.publish(topic, payload, qos)


    # 对mqtt订阅消息处理函数
    def on_message_come(self, lient, userdata, msg):
	# python3 bytes转str
        self.sub_msg = json.loads(msg.payload)
        print(self.sub_msg)
        self.castlex_feedback = self.sub_msg

    # mqtt subscribe 消息
    def on_subscribe(self):
        self.mqttClient.subscribe("/castlex_arm_msg", 0)
        self.mqttClient.on_message = self.on_message_come  # 消息到来处理函数


    # 向机械臂发送请求装货指令
    def arm_castlex_mqtt_send(self, data):
        self.feedback_data, self.castlex_color_x, self.castlex_color_y, self.castlex_color_s = None, None, None, None 
        castlex_data = data
        param = json.dumps(castlex_data)
        self.on_publish("/castlex_arm_feedback_msg", payload = param, qos=0)
        
    
    def arm_castlex_mqtt_read(self):
        self.castlex_feedback = None
        while(self.castlex_feedback == None):
            pass
        if (self.castlex_feedback != None):
            qw0_0 = self.castlex_feedback
            return qw0_0
     
    
    

# if __name__ == '__main__':
#     try:
#         arm()
#         rospy.spin()

#     except rospy.ROSInterruptException:
#         rospy.loginfo("Navigation finished.")
