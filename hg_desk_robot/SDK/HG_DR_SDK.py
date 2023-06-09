# -*- coding:utf8 -*-
#!/usr/bin/python
'''
HG_DR_SDK-version-1.0
create by cjw, python2
date: 2020/8/1
'''

import time
import math
import json
from SDK.HG_DR import HG_DR
from SDK.HG_DR_KI import HG_DR_KI

class HG_DR_SDK:

    # 根据GUI界面选择传参，初始化
    prot_name = '/dev/ttyACM0'
    limit_data = 5

    def __init__(self):

        # self.connect_prot = HG_DR_SDK.prot_name
        # print(self.connect_prot+'3')
        self.connect_state = False

        self.HG_DR = HG_DR(HG_DR_SDK.prot_name, 115200)
        self.Kinematics = HG_DR_KI(debug=False)
        self.currBaseAngle = 0
        self.currRearAngle = 0
        self.currFrontAngle = 0

        self.color_num = 0

        self.pump_state = False
        self.test_pump = 0

        self.angle1 = 0.0
        self.angle2 = 0.0
        self.angle3 = 0.0

        self.limit_angle = HG_DR_SDK.limit_data

        # 卡尔曼滤波参数
        self.dt = 20 * 0.005  # 滤波采样时间
        self.Q_angle = 0.5
        self.Q_gyro = 0.5
        self.R_angle = 0.5
        self.C_0 = 1

        self.kalman_angle1 = 0.0
        self.P = [[1, 0], [0, 1]]
        self.Pdot = [0, 0, 0, 0]
        self.q_bias = 0.0
        self.angle_err = None
        self.PCt_0 = None
        self.PCt_1 = None
        self.E = None
        self.K_0 = None
        self.K_1 = None
        self.t_0 = None
        self.t_1 = None

        self.kalman_angle2 = 0.0
        self.P_1 = [[1, 0], [0, 1]]
        self.Pdot_1 = [0, 0, 0, 0]
        self.q_bias_1 = 0.0
        self.angle_err_1 = None
        self.PCt_0_1 = None
        self.PCt_1_1 = None
        self.E_1 = None
        self.K_0_1 = None
        self.K_1_1 = None
        self.t_0_1 = None
        self.t_1_1 = None

    # 连接机械臂，建立起机械臂通讯
    def connectHG_DR(self, portName='/dev/ttyACM0', timeout=0.1):
        # self.HG_DR = HG_DR(portName, 115200)
        if self.connect_state:
            print("current state is connect!!!")
        else:
            self.HG_DR.Open(timeout)
            time.sleep(1)
            successes = 0
            i = 0
            while True:
                ret = self.HG_DR.isReady()
                if ret[0] and ret[1]:
                    successes += 1
                if successes > 10:
                    print("HG_DR connect successfully and HG_DR is ready!")
                    self.controlRGBlight('green')
                    self.connect_state = True
                    return True
                    # break
                if i > 100:
                    print("HG_DR connect failed!")
                    self.controlRGBlight('red')
                    raise Exception('Comm problem')
                    return False

    # 断开机械臂通讯连接
    def disconnectHG_DR(self):
        self.HG_DR.Close()
        self.connect_state = False
        print("The serial communication of HG_DR is closed")

    # 重新标定/初始化
    def calibrateJoint(self):
        ret = self.HG_DR.calibrateJoint()
        print(ret)

        if ret[1]:
            time.sleep(10)
            self.initializeSteppers()
        else:
            print("Failed calibrateJoint!!!")
        print(ret)

    # 初始化机械臂位姿
    def initializeSteppers(self, setX=259.48, setY=0, setZ=85.32):
        adjust = 0
        attempts = 10
        for adjust in range(1, 3):
            rearAngle, frontAngle = self.get_mpu_data()

            currBaseAngle = 0
            currRearAngle = rearAngle
            currFrontAngle = frontAngle
            print("---------------current angle: ", currBaseAngle, currRearAngle, currFrontAngle)

            lastBaseAngle, lastRearAngle, lastFrontAngle = self.Kinematics.anglesFromCoordinates(setX, setY, setZ)

            lastBaseAngle = math.degrees(lastBaseAngle)
            lastRearAngle = math.degrees(lastRearAngle)
            lastFrontAngle = math.degrees(lastFrontAngle)
            print("---------------last angle: ", lastBaseAngle, lastRearAngle, lastFrontAngle)

            setBaseAngle = lastBaseAngle - currBaseAngle
            setRearAngle = lastRearAngle - currRearAngle #- (lastRearAngle - currRearAngle)
            setFrontAngle = -(lastFrontAngle - currFrontAngle)

            print("---------------init move angle: ", setBaseAngle, setRearAngle, setFrontAngle)
            if -0.5 < setRearAngle < 0.5:
                setRearAngle = 0.0
                if -0.5 < setFrontAngle < 0.5:
                    setFrontAngle = 0.0
                    # print("setBaseAngle=", setBaseAngle,
                    #       "setRearAngle=", setRearAngle,
                    #       "setFrontAngle=", setFrontAngle)
                    # break

            print("setBaseAngle=", setBaseAngle, "setRearAngle=", setRearAngle, "setFrontAngle=", setFrontAngle)
            # setBaseAngle, setRearAngle, setFrontAngle = self.soft_limit(setBaseAngle, setRearAngle, setFrontAngle)
            self.HG_DR.controlSteppers(setBaseAngle, setRearAngle, setFrontAngle)
            self.HG_DR.controlPump(0)
            print("adjust=", adjust)

            # time.sleep(3)

        if adjust < 10:
            print("initializeStepper successes!")
            self.controlRGBlight('green')
        # return True
        else:
            print("initializeStepper failed!")
            self.controlRGBlight('orange')
        # return False

        currBaseAngle = lastBaseAngle
        currRearAngle = lastRearAngle
        currFrontAngle = lastFrontAngle
        currX = setX
        currY = setY
        currZ = setZ

        self.saveAngleAndPose(currBaseAngle, currRearAngle, currFrontAngle, currX, currY, currZ)
        currentangle1, currentangle2 = self.get_mpu_data()
        print("-------move current angle: ", currentangle1, currentangle2)
        self.move_check(currRearAngle, currFrontAngle, 2)

    # 保存当前机械臂关节轴角度和空间位置
    def saveAngleAndPose(self, currBaseAngle, currRearAngle, currFrontAngle, currX, currY, currZ):
        dic = {'currBaseAngle': currBaseAngle, 'currRearAngle': currRearAngle, 'currFrontAngle': currFrontAngle,
                'currX': currX, 'currY': currY, 'currZ': currZ} 
        js = json.dumps(dic)
        file = open('currAngleStationSave.txt', 'w')
        file.write(js)
        file.close()

        self.angle1 = currBaseAngle
        self.angle2 = currRearAngle
        self.angle3 = currFrontAngle

    #获取当前机械臂关节轴角度和空间位置
    def getAngleAndPose(self):
        file = open('currAngleStationSave.txt', 'r')
        js = file.read()
        dic = json.loads(js)
        currBaseAngle = dic['currBaseAngle']
        currRearAngle = dic['currRearAngle']
        currFrontAngle = dic['currFrontAngle']
        currX = dic['currX']
        currY = dic['currY']
        currZ = dic['currZ']
        file.close()
        return currBaseAngle, currRearAngle, currFrontAngle, currX, currY, currZ

    # 驱使机械臂末端运动到指定的笛卡尔坐标
    def moveToStation(self, setX, setY, setZ):
        self.controlRGBlight('blue')
        currBaseAngle, currRearAngle, currFrontAngle, currX, currY, currZ = self.getAngleAndPose()

        print("currBaseAngle=", currBaseAngle, "currRearAngle=", currRearAngle, "currFrontAngle=", currFrontAngle)

        lastBaseAngle, lastRearAngle, lastFrontAngle = self.Kinematics.anglesFromCoordinates(setX, setY, setZ)

        lastBaseAngle = math.degrees(lastBaseAngle)
        lastRearAngle = math.degrees(lastRearAngle)
        lastFrontAngle = math.degrees(lastFrontAngle)

        print("lastBaseAngle=", lastBaseAngle, "lastRearAngle=", lastRearAngle, "lastFrontAngle=", lastFrontAngle)

        setBaseAngle = lastBaseAngle - currBaseAngle
        setRearAngle = lastRearAngle - currRearAngle
        setFrontAngle = -(lastFrontAngle - currFrontAngle)

        print("setBaseAngle=", setBaseAngle, "setRearAngle=", setRearAngle, "setFrontAngle=", setFrontAngle)

        setBaseAngle, setRearAngle, setFrontAngle = self.soft_limit(setBaseAngle, setRearAngle, setFrontAngle)
        ret = self.HG_DR.controlSteppers(setBaseAngle, setRearAngle, setFrontAngle)

        currBaseAngle = lastBaseAngle
        currRearAngle = lastRearAngle
        currFrontAngle = lastFrontAngle
        currX = setX
        currY = setY
        currZ = setZ

        self.saveAngleAndPose(currBaseAngle, currRearAngle, currFrontAngle, currX, currY, currZ)

        # time.sleep(3)
        if ret:
            res = self.move_check(currRearAngle, currFrontAngle, 1)
        if res:
            self.controlRGBlight('green')
        return True

    # 让机械臂末端走一段距离
    def moveAnInterval(self, intervalX, intervalY, intervalZ):

        currBaseAngle, currRearAngle, currFrontAngle, currX, currY, currZ = self.getAngleAndPose()

        lastX = currX + intervalX
        lastY = currY + intervalY
        lastZ = currZ + intervalZ

        ret = self.moveToStation(lastX, lastY, lastZ)

        return ret

    def move_to_angle(self, baseAngle, rearAngle, fronAngle):
        current_base, current_rear, current_front, current_x, current_y, current_z = self.getAngleAndPose()
        base_dis = baseAngle - current_base
        rear_dis = rearAngle - current_rear
        front_dis = fronAngle - current_front
        self.controlPerSteppers(base_dis, rear_dis, front_dis)
        return True

    def controlPerSteppers(self, setBaseAngle, setRearAngle, setFrontAngle):
        self.controlRGBlight('blue')
        angle1, angle2, angle3, x, y, z = self.getAngleAndPose()
        setBaseAngle, setRearAngle, setFrontAngle = self.soft_limit(setBaseAngle, setRearAngle, setFrontAngle)
        ret = self.HG_DR.controlSteppers(setBaseAngle, setRearAngle, -setFrontAngle)
        current_x, current_y, current_z = self.Kinematics.coordinatesFromAngles(angle1 + setBaseAngle,
                                                                                angle2 + setRearAngle,
                                                                                angle3 + setFrontAngle)
        self.saveAngleAndPose(angle1+setBaseAngle, angle2+setRearAngle, angle3+setFrontAngle, current_x, current_y, current_z)
        # if self.HG_DR.GetMoveStatus():
        #     print("move end")
        # time.sleep(3.0)
        if ret:
            res = self.move_check(angle2+setRearAngle, angle3+setFrontAngle, 2)
        if res:
            self.controlRGBlight('green')
        return True

    # 门型模式点位运动
    def jumpAngle(self, setX, setY, setZ, beforeRaiseHeight, afterLandHeight):
        self.moveAnInterval(0, 0, beforeRaiseHeight)
        self.moveToStation(setX, setY, setZ+afterLandHeight)
        self.moveToStation(setX, setY, setZ)

    # 控制气泵
    def controlPump(self, state):
        result=self.HG_DR.controlPump(state)
        self.pump_state = not self.pump_state
        return result

    # 指示灯颜色设置，输入颜色或者对应的数值
    def controlRGBlight(self, colorNum):
        list = [['red', 1], ['orange', 2], ['yellow', 3], ['green', 4], ['cyan', 5], ['blue', 6], ['purple', 7]]
        if colorNum in list[0]:
            self.HG_DR.setColor(255, 0, 0)
            self.color_num = 1
            print("The indicator light is red!!!")
        elif colorNum in list[1]:
            self.HG_DR.setColor(245, 250, 0)
            self.color_num = 2
            print("The indicator light is orange!!!")
        elif colorNum in list[2]:
            self.HG_DR.setColor(200, 250, 255)
            self.color_num = 3
            print("The indicator light is yellow!!!")
        elif colorNum in list[3]:
            self.HG_DR.setColor(0, 255, 0)
            self.color_num = 4
            print("The indicator light is green!!!")
        elif colorNum in list[4]:
            self.HG_DR.setColor(50, 120, 170)
            self.color_num = 5
            print("The indicator light is cyan!!!")
        elif colorNum in list[5]:
            self.HG_DR.setColor(0, 0, 255)
            self.color_num = 6
            print("The indicator light is blue!!!")
        elif colorNum in list[6]:
            self.HG_DR.setColor(128, 0, 255)
            self.color_num = 7
            print("The indicator light is purple!!!")
        else:
            print("ColorNum is error!!! and the indicator light is error!!!")

    def get_color_num(self):
        return self.color_num

    def get_pump_state(self):
        return self.pump_state

    def get_angle(self):
        return self.angle1, self.angle2, self.angle3

    # mpu1,卡尔曼滤波
    def Angle1_Kalman_Filter(self, angle1_data, gyro1_data):
        self.kalman_angle1 += (gyro1_data - self.q_bias) * self.dt
        self.angle_err = angle1_data - self.kalman_angle1
        self.Pdot[0] = self.Q_angle - self.P[0][1] - self.P[1][0]
        self.Pdot[1] = - self.P[1][1]
        self.Pdot[2] = - self.P[1][1]
        self.Pdot[3] = self.Q_gyro
        self.P[0][0] += self.Pdot[0] * self.dt
        self.P[0][1] += self.Pdot[1] * self.dt
        self.P[1][0] += self.Pdot[2] * self.dt
        self.P[1][1] += self.Pdot[3] * self.dt
        self.PCt_0 = self.C_0 * self.P[0][0]
        self.PCt_1 = self.C_0 * self.P[1][0]
        self.E = self.R_angle + self.C_0 * self.PCt_0
        self.K_0 = self.PCt_0 / self.E
        self.K_1 = self.PCt_1 / self.E
        self.t_0 = self.PCt_0
        self.t_1 = self.C_0 * self.P[0][1]
        self.P[0][0] -= self.K_0 * self.t_0
        self.P[0][1] -= self.K_0 * self.t_1
        self.P[1][0] -= self.K_1 * self.t_0
        self.P[1][1] -= self.K_1 * self.t_1
        self.kalman_angle1 += self.K_0 * self.angle_err  # 最优角度
        self.q_bias += self.K_1 * self.angle_err
        angle_dot = gyro1_data - self.q_bias  # 最优角速度
        return self.kalman_angle1

    # mpu2,卡尔曼滤波
    def Angle2_Kalman_Filter(self, angle2_data, gyro2_data):

        self.kalman_angle2 += (gyro2_data - self.q_bias_1) * self.dt
        self.angle_err_1 = angle2_data - self.kalman_angle2
        self.Pdot_1[0] = self.Q_angle - self.P_1[0][1] - self.P_1[1][0]
        self.Pdot_1[1] = - self.P_1[1][1]
        self.Pdot_1[2] = - self.P_1[1][1]
        self.Pdot_1[3] = self.Q_gyro
        self.P_1[0][0] += self.Pdot_1[0] * self.dt
        self.P_1[0][1] += self.Pdot_1[1] * self.dt
        self.P_1[1][0] += self.Pdot_1[2] * self.dt
        self.P_1[1][1] += self.Pdot_1[3] * self.dt
        self.PCt_0_1 = self.C_0 * self.P_1[0][0]
        self.PCt_1_1 = self.C_0 * self.P_1[1][0]
        self.E_1 = self.R_angle + self.C_0 * self.PCt_0_1
        self.K_0_1 = self.PCt_0_1 / self.E_1
        self.K_1_1 = self.PCt_1_1 / self.E_1
        self.t_0_1 = self.PCt_0_1
        self.t_1_1 = self.C_0 * self.P_1[0][1]
        self.P_1[0][0] -= self.K_0_1 * self.t_0_1
        self.P_1[0][1] -= self.K_0_1 * self.t_1_1
        self.P_1[1][0] -= self.K_1_1 * self.t_0_1
        self.P_1[1][1] -= self.K_1_1 * self.t_1_1
        self.kalman_angle2 += self.K_0_1 * self.angle_err_1  # 最优角度
        self.q_bias_1 += self.K_1_1 * self.angle_err_1
        angle_dot = gyro2_data - self.q_bias_1  # 最优角速度
        return self.kalman_angle2

    # 检查当前能否读取陀螺仪数据
    def check_read_mpu(self):
        current_data = self.HG_DR.GetAccels()
        get_times = 10
        # if not current_data:
        #     time.sleep(10.0)
        while not current_data:
            get_times -= 1
            time.sleep(0.5)
            current_data = self.HG_DR.GetAccels()
            if get_times < 0:
                # break
                return False
        return True

    # 获取陀螺仪数据
    def get_mpu_data(self):
        adjust = 0
        attempts = 10
        rearAngle = 0
        frontAngle = 0
        rear_list = []
        front_list = []
        # 取10次均值
        if self.check_read_mpu():
            for adjust in range(1, 6):
                while attempts:
                    getAccels = self.HG_DR.GetAccels()
                    # time.sleep(1.0)
                    # getGyros = self.HG_DR.GetGyros()
                    if getAccels:   # getAccels[0]
                        rearAccel_X = getAccels[1]
                        rearAccel_Y = getAccels[2]
                        rearAccel_Z = getAccels[3]
                        frontAccel_X = getAccels[4]
                        frontAccel_Y = getAccels[5]
                        frontAccel_Z = getAccels[6]

                        # rearGyro_X = getGyros[1]fd
                        # rearGyro_Y = getGyros[2]
                        # rearGyro_Z = getGyros[3]
                        # frontGyro_X = getGyros[4]
                        # frontGyro_Y = getGyros[5]
                        # frontGyro_Z = getGyros[6]

                        print("Successfully obtain accelerometer data!!!")
                        break
                    else:
                        print("Failed obtain accelerometer data!!!")
                        self.controlRGBlight('red')
                    attempts -= 1

                current_rearAngle = 90 + (math.atan2(rearAccel_Y, rearAccel_Z) * 180.0) / math.pi
                current_frontAngle = (math.atan2(frontAccel_Y, frontAccel_Z) * 180.0) / math.pi

                print("get now angle : ", current_rearAngle, current_frontAngle)

                # current_rearGyro = -rearGyro_Y / 131.0
                # current_frontGyro = -frontGyro_Y / 131.0
                rear_list.append(current_rearAngle)
                front_list.append(current_frontAngle)
                # time.sleep(1.0)
                # 加入卡尔曼滤波
                # rearAngle += current_rearAngle  # self.Angle1_Kalman_Filter(current_rearAngle, current_rearGyro)
                # frontAngle += current_frontAngle  # self.Angle1_Kalman_Filter(current_frontAngle, current_frontGyro)
            rear_list.sort()
            front_list.sort()

            rearAngle = sum(rear_list[1:4])
            frontAngle = sum(front_list[1:4])
            print("get current angle : ", rearAngle/3, frontAngle/3)
            return rearAngle/3, frontAngle/3
        else:
            print("get mpu data fail, return current angle!!!!!")
            return self.angle2, self.angle3

    # angle1: -135 - 135; angle2 :  -35 - 95; angle3: 5 - 85
    def soft_limit(self, target_angle1, target_angle2, target_angle3):

        current_angle1, current_angle2, current_angle3, current_x, current_y, current_z = self.getAngleAndPose()
        #now_angle2, now_angle3 = self.get_mpu_data()

        target_angle1 += current_angle1
        target_angle2 += current_angle2
        target_angle3 += current_angle3

        if target_angle1 > (135 - self.limit_angle):
            target_angle1 = (135 - self.limit_angle)

        if target_angle1 < (-135 + self.limit_angle):
            target_angle1 = (-135 + self.limit_angle)

        if target_angle2 > (95 - self.limit_angle):
            target_angle2 = (95 - self.limit_angle)

        if target_angle2 < (-35 + self.limit_angle):
            target_angle2 = (-35 + self.limit_angle)

        if target_angle3 > (85 - self.limit_angle):
            target_angle3 = (85 - self.limit_angle)

        if target_angle3 < (5 + self.limit_angle):
            target_angle3 = (5 + self.limit_angle)

        return target_angle1 - current_angle1, target_angle2 - current_angle2, target_angle3 - current_angle3

    # 运动角度检测,　type表示运动方式, 1-笛卡尔　2-关节角度
    def move_check(self, target_RearAngle, target_FrontAngle, move_type):
        if self.HG_DR.GetMoveStatus():
            current_rearAngle, current_frontAngle = self.get_mpu_data()
            rearAngle_dis = target_RearAngle - current_rearAngle
            frontAngle_dis = target_FrontAngle - current_frontAngle
            print("-------------angle move dis = :", rearAngle_dis, frontAngle_dis)
            if abs(rearAngle_dis) > 3 or abs(frontAngle_dis) > 3:
                self.Angle_compensation(0, rearAngle_dis, frontAngle_dis, move_type)
            else:
                return True
        else:
            print("arm move now")

    # 角度反馈补偿，　运动结束后再check
    def Angle_compensation(self, compensation_angle1, compensation_angle2, compensation_angle3, move_type):
        if move_type == 1:
            compensation_angle2 = compensation_angle2
            compensation_angle3 = -compensation_angle3
        elif move_type == 2:
            compensation_angle3 = -compensation_angle3
        else:
            pass
        ret = self.HG_DR.controlSteppers(compensation_angle1, compensation_angle2, compensation_angle3)
        if ret:
            BaseAngle, RearAngle, FrontAngle, c_x, c_y, c_z = self.getAngleAndPose()
            self.move_check(RearAngle, FrontAngle, move_type)
