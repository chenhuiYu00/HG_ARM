#!/usr/bin/python
# -*- coding:utf8 -*-

import time
import math
import json
import rospy
import socket
import threading
from std_msgs.msg import Int32, String
from HG_DR_SDK import HG_DR_SDK
from HG_DR_KI import HG_DR_KI

from object_detect.msg import object_result_msg

class iot_grasp():
    def __init__(self):
        rospy.init_node('listener', anonymous=True)
        rospy.Subscriber("grasp_state", Int32, self.test)
        self.grasp_pub = rospy.Publisher("grasp_target", Int32, queue_size=1)
        self.grasp_state = 0
        # 通讯设置
        self.host_ip = rospy.get_param('~host_ip', "192.168.3.8")
        self.host_port = rospy.get_param('~host_port', "50001")
        self.client, self.address = None, None

        self.Socket_Server = socket.socket()

        self.Socket_Server.bind((self.host_ip, int(self.host_port)))
        # 监听
        self.Socket_Server.listen(10)

        self.msg_recv_thr = threading.Thread(target=self.socket_data)
        self.msg_recv_thr.start()

    def test(self, data):
        if data.data == 1:
            self.grasp_state = data.data
            self.grasp_success()
            print("grasp ok")

    # 回复OK
    def reply_ok(self):
        self.client.sendall('OK')
        return True

    # 接受数据
    def get_client_msg(self):
        while True:
            try:
                msg = self.client.recv(7)
            except:
                self.client.close()
                print("当前端口: %s 连接已断开\n" % self.address[1])
                break
            if len(msg):
                print("服务端接收: %s" % msg)
                print("读取完成")
                self.reply_ok()
                if (msg[0:5] == "fruit"):
                    self.grasp_pub.publish(int(msg[-1]))
            else:
                self.client.close()
                print("当前端口: %s 连接已断开\n" % self.address[1])
                break

    def socket_data(self):
        while True:
            # 接收客户端连接
            print("等待连接....\n")
            self.client, self.address = self.Socket_Server.accept()
            print("新连接")
            print("IP is %s" % self.address[0])
            print("port is %d\n" % self.address[1])
            self.get_client_msg()

    # 抓取完成状态sss
    def grasp_success(self):
        self.client.sendall("SUCCESS")


if __name__ == '__main__':
    iot_grasp()
