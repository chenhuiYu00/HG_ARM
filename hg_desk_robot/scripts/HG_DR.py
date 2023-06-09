# -*- coding:utf8 -*-
#!/usr/bin/python
'''
HG_DR-version-1.0
create by cjw
date: 2020/8/1
'''

import serial
import time
import threading
import sys
import ctypes
import chardet


_max_trys = 3

CMD_READY = 0
CMD_STEPS = 1
CMD_EXEC_QUEUE = 2
CMD_GET_ACCELS = 3
CMD_SWITCH_TO_ACCEL_REPORT_MODE = 4
CMD_CALIBRATE_JOINT = 5
CMD_EMERGENCY_STOP = 6
CMD_SET_COUNTERS = 7
CMD_GET_COUNTERS = 8
CMD_LASER_ON = 9
CMD_PUMP_ON = 10
CMD_VALVE_ON = 11
CMD_BOARD_VERSION = 12
CMD_SET_COLOR = 13
CMD_GET_GYRO = 14
CMD_GET_STATUS = 15

class HG_DR:

    def __init__(self, comport, rate):
        self._lock = threading.Lock()
        self._comport = comport
        self._rate = rate
        self._port = None
        self._crc = 0xffff

    # 连接arudino 波特率默认115200
    def Open(self, timeout=0.1):
        self._port = serial.Serial(self._comport, baudrate=self._rate,
                                   timeout=timeout, interCharTimeout=0.01)
    # 断开连接
    def Close(self):
        self._port.close()

    # 恢复校验码
    def _crc_clear(self):
        self._crc = 0xffff

    # 更新校验码。
    def _crc_update(self, data):
        self._crc = self._crc ^ (data << 8)
        for bit in range(0, 8):
            if (self._crc&0x8000) == 0x8000:
                self._crc = ((self._crc << 1) ^ 0x1021)
            else:
                self._crc = self._crc << 1

    def _readchecksumword(self):
        data = self._port.read(2)
        # data.encode("ascii")
        if len(data) == 2:
            # print(type(data[0].encode("utf8")))
            # print(data[0] << 8)
            crc = (ord(data[0]) << 8) | ord(data[1])
            return (1,crc)
        return (0,0)

    # 读1个字节，8位。
    def _readbyte(self):
        data = self._port.read(1)
        if len(data):
            val = ord(data)
            self._crc_update(val)
            return (1, val)
        return (0, 0)

    # 读2个字节，16位。
    def _readint(self):
        val1 = self._readbyte()
        if val1[0]:
            val2 = self._readbyte()
            if val2[0]:
                return (1, val1[1] << 8 | val2[1])
        return (0, 0)

    # 读取4个字节，16位。
    def _readlong(self):
        val1 = self._readbyte()
        if val1[0]:
            val2 = self._readbyte()
            if val2[0]:
                val3 = self._readbyte()
                if val3[0]:
                    val4 = self._readbyte()
                    if val4[0]:
                        return (1, val1[1] << 24 | val2[1] << 16 | val3[1] << 8 | val4[1])
        return (0, 0)

    def _readslong(self):
        val = self._readlong()
        if val[0]:
            if val[1] & 0x80000000:
                return (val[0], val[1] - 0x100000000)
            return (val[0], val[1])
        return (0, 0)

    # 发送命令代号，然后读取一个1字节数
    def _read1(self, cmd):
        trys = _max_trys
        while trys:
            self._port.flushInput()
            self._sendcommand(cmd)
            val1 = self._readbyte()
            if val1[0]:
                crc = self._readchecksumword()
                if crc[0]:
                    if self._crc & 0xFFFF != crc[1] & 0xFFFF:
                        raise Exception('crc differs', self._crc, crc)
                        return (0, 0)
                    return (1, val1[1])
            trys -= 1
        # raise Exception("couldn't get response in time for", _max_trys, 'times')
        return (1, 1)

    # 发送命令代号，然后读取一个4字节数
    def _read4(self, cmd):
        trys = _max_trys
        while trys:
            self._port.flushInput()
            self._sendcommand(cmd)
            val1 = self._readlong()
            if val1[0]:
                crc = self._readchecksumword()
                if crc[0]:
                    if self._crc & 0xFFFF != crc[1] & 0xFFFF:
                        return (0, 0)
                    return (1, val1[1])
            trys -= 1
        return (0, 0)

    # 发送命令代号，然后读取一个4字节数和一个1字节数
    def _read4_1(self, cmd):
        trys = _max_trys
        while trys:
            self._port.flushInput()
            self._sendcommand(cmd)
            val1 = self._readslong()
            if val1[0]:
                val2 = self._readbyte()
                if val2[0]:
                    crc = self._readchecksumword()
                    if crc[0]:
                        if self._crc & 0xFFFF != crc[1] & 0xFFFF:
                            return (0, 0)
                        return (1, val1[1], val2[1])
            trys -= 1
        return (0, 0)

    # 发送命令代号，然后读取六个2字节数
    def _read222222(self, cmd):
        trys = _max_trys
        while trys:
            self._port.flushInput()
            self._sendcommand(cmd)
            val1 = self._readint()
            if val1[0]:
                val2 = self._readint()
                if val2[0]:
                    val3 = self._readint()
                    if val3[0]:
                        val4 = self._readint()
                        if val4[0]:
                            val5 = self._readint()
                            if val5[0]:
                                val6 = self._readint()
                                if val6[0]:
                                    crc = self._readchecksumword()
                                    if crc[0]:
                                        if self._crc & 0xFFFF != crc[1] & 0xFFFF:
                                            return (0, 0)
                                    return (1, val1[1], val2[1], val3[1], val4[1], val5[1], val6[1])
            trys -= 1
        return (0, 0)

    # 写1个字节
    def _writebyte(self, val):
        self._crc_update(val & 0xFF)
        self._port.write(chr(val & 0xFF))
        # print(chr(val & 0xFF))

    # 写2个字节
    def _writeword(self, val):
        self._writebyte((val >> 8) & 0xFF)
        self._writebyte(val & 0xFF)

    # 写4个字节
    def _writelong(self, val):
        self._writebyte((val >> 24) & 0xFF)
        self._writebyte((val >> 16) & 0xFF)
        self._writebyte((val >> 8) & 0xFF)
        self._writebyte(val & 0xFF)

    # 写检查
    def _writechecksum(self):
        self._writeword(self._crc & 0xFFFF)
        val = self._readbyte()
        if val[0]:
            return True
        return False

    # 发送命令代号
    def _sendcommand(self, command):
        self._crc_clear()
        self._crc_update(command)
        self._port.write(chr(command).encode())
        return

    # 只发送命令代号
    def _write0(self, cmd):
        while trys:
            self._sendcommand(cmd)
            if self._writechecksum():
                return True
            trys = trys - 1
        return False

    # 发送命令代号，并写一个1字节数
    def _write1(self, cmd, val):
        trys = _max_trys
        while trys:
            self._sendcommand(cmd)
            self._writebyte(val)
            if self._writechecksum():
                return True
            trys = trys - 1
        return False

    # 发送命令代号，并写一个2字节数
    def _write2(self, cmd, val):
        trys = _max_trys
        while trys:
            self._sendcommand(cmd)
            self._writeword(val)
            if self._writechecksum():
                return True
            trys = trys - 1
        return False

    # 发送命令代号，并写一个4字节数
    def _write4(self, cmd, val):
        trys = _max_trys
        while trys:
            self._sendcommand(cmd)
            self._writelong(val)
            if self._writechecksum():
                return True
            trys = trys - 1
        return False

    # 发送命令代号，并写三个1字节数
    def _write111(self, cmd, val1, val2, val3):
        trys = _max_trys
        while trys:
            self._sendcommand(cmd)
            self._writebyte(val1)
            self._writebyte(val2)
            self._writebyte(val3)
            if self._writechecksum():
                return True
            trys = trys - 1
        return False

    # 发送命令代号，并写一个1字节和一个4字节数
    def _write14(self, cmd, val1, val2):
        trys = _max_trys
        while trys:
            self._sendcommand(cmd)
            self._writebyte(val1)
            self._writelong(val2)
            if self._writechecksum():
                return True
            trys = trys - 1
        return False

    # 发送命令代号，写四个1字节数和一个两字节数，读一个1字节数
    def _write11121read1(self, cmd, val1, val2, val3, val4, val5):
        trys = _max_trys
        while trys:
            self._sendcommand(cmd)
            self._writebyte(val1)
            self._writebyte(val2)
            self._writebyte(val3)
            self._writeword(val4)
            self._writebyte(val5)
            self._writeword(self._crc & 0xFFFF)
            self._port.flushInput()
            self._crc_clear()
            ret = self._readbyte()
            if ret[0]:
                crc = self._readchecksumword()
                if crc[0]:
                    if self._crc & 0xFFFF != crc[1] & 0xFFFF:
                        raise Exception('crc differs', self._crc, crc)
                        return (0, 0)
                    return (1, ret[1])
            trys = trys - 1
        return (0, 0)

    # 发送命令代号，写4个2字节数和一个1字节数，读一个1字节数
    def _write22221read1(self, cmd, val1, val2, val3, val4, val5):
        trys = _max_trys
        while trys:
            self._sendcommand(cmd)
            self._writeword(val1)
            self._writeword(val2)
            self._writeword(val3)
            self._writeword(val4)
            self._writebyte(val5)
            self._writeword(self._crc & 0xFFFF)
            self._port.flushInput()
            self._crc_clear()
            ret = self._readbyte()
            if ret[0]:
                crc = self._readchecksumword()
                if crc[0]:
                    if self._crc & 0xFFFF != crc[1] & 0xFFFF:
                        raise Exception('crc differs', self._crc, crc)
                        return (0, 0)
                    return (1, ret[1])
            trys = trys - 1
        return (0, 0)

    # 电机驱动函数，驱动三个步进电机
    def Steps(self, j1, j2, j3, ticks, j1dir, j2dir, j3dir, deferred):
        # print('j1=', j1)
        # print('j2=', j2)
        # print('j3=', j3)
        # print('ticks=', ticks)
        # print('j1dir=', j1dir)
        # print('j2dir=', j2dir)
        # print('j3dir=', j3dir)
        control = ((j1dir & 0x01) << 1) | ((j2dir & 0x01) << 2) | ((j3dir & 0x01) << 3);
        if deferred:
            control |= 0x01
        self._lock.acquire()
        result = self._write22221read1(CMD_STEPS, j1, j2, j3, ticks, control)
        self._lock.release()
        # print(result)
        return result

    # 封装电机驱动函数step（），只需输入三个电机的转动角度。
    def controlSteppers(self, j1Angle, j2Angle, j3Angle):
        # ticks = int(32000*1.37)  #180
        ticks = 54400#int(32000 * 1.4)  # 180 1.4
        # ticks = 32000   #180
        # ticks = 16000   #90
        # ticks = 8000   #45
        deferred = False
        # 对值进行分割整合
        if j1Angle > 0.02:
            j1dir = 1
            j1 = int(round(180 / abs(j1Angle)))
        elif -0.02 <= j1Angle <= 0.02:
            j1dir = 1
            j1 = 32000
        else:
            j1dir = 0
            j1 = int(round(180 / abs(j1Angle)))

        if j2Angle > 0.02:
            j2dir = 1
            j2 = int(round(180 / abs(j2Angle)))
        elif -0.02 <= j2Angle <= 0.02:
            j2dir = 1
            j2 = 32000
        else:
            j2dir = 0
            j2 = int(round(180 / abs(j2Angle)))

        if j3Angle > 0.02:
            j3dir = 1
            j3 = int(round(180 / abs(j3Angle)))
        elif -0.02 <= j3Angle <= 0.02:
            j3dir = 1
            j3 = 32000
        else:
            j3dir = 0
            j3 = int(round(180 / abs(j3Angle)))

        result = self.Steps(j1, j2, j3, ticks, j1dir, j2dir, j3dir, deferred)

        return result

    def ExecQueue(self):
        '''
        Executes deferred commands.
        '''
        self._lock.acquire()
        result = self._write0(CMD_EXEC_QUEUE)
        self._lock.release()
        return result

    # 发送准备命令，让dobot处于准备状态
    def isReady(self):
        '''
        Checks whether the controller is up and running.
        '''
        self._lock.acquire()
        result = self._read1(CMD_READY)
        self._lock.release()
        # Check for magic number.
        # return [result[0], result[1] == 0x40]
        return [result[0], result[1]]

    def calibrateJoint(self):
        self._lock.acquire()
        result = self._read1(CMD_CALIBRATE_JOINT)
        self._lock.release()
        return result

    # 获取两个加速度计的值
    def GetAccels(self):
        self._lock.acquire()
        result = self._read222222(CMD_GET_ACCELS)
        self._lock.release()
        #　print(len(result))000
        # 后臂的加速度计值
        if len(result) < 6:
            print("not mpu data", len(result))
            time.sleep(1.0)
            # self.reset()
            # self.GetAccels()
            # return False
        else:
            rearAccel_X = float(ctypes.c_int16(result[1]).value) / 100
            rearAccel_Y = float(ctypes.c_int16(result[2]).value) / 100
            rearAccel_Z = float(ctypes.c_int16(result[3]).value) / 100
            # 前臂的加速度计值
            frontAccel_X = float(ctypes.c_int16(result[4]).value) / 100
            frontAccel_Y = float(ctypes.c_int16(result[5]).value) / 100
            frontAccel_Z = float(ctypes.c_int16(result[6]).value) / 100

            return [result[0], rearAccel_X, rearAccel_Y, rearAccel_Z, frontAccel_X, frontAccel_Y, frontAccel_Z]

    # 获取角速度
    def GetGyros(self):
        self._lock.acquire()
        result = self._read222222(CMD_GET_GYRO)
        self._lock.release()
        # print(len(result))
        if len(result) < 6:
            return False
        else:
            rearGyro_X = float(ctypes.c_int16(result[1]).value) / 100
            rearGyro_Y = float(ctypes.c_int16(result[2]).value) / 100
            rearGyro_Z = float(ctypes.c_int16(result[3]).value) / 100

            frontGyro_X = float(ctypes.c_int16(result[4]).value) / 100
            frontGyro_Y = float(ctypes.c_int16(result[5]).value) / 100
            frontGyro_Z = float(ctypes.c_int16(result[6]).value) / 100

            return [result[0], rearGyro_X, rearGyro_Y, rearGyro_Z, frontGyro_X, frontGyro_Y, frontGyro_Z]

    # 判断运动是否结束
    def GetMoveStatus(self):
        result = self._read1(CMD_GET_STATUS)
        print(result)
        if result[0]:
            return True
        else:
            return False

    # 控制气泵
    def controlPump(self, state):
        self._lock.acquire()
        result = self._write1(CMD_PUMP_ON, state)
        self._lock.release()
        return result

    # 设置提示灯颜色
    def setColor(self, redValue, greenValue, blueValue):
        self._lock.acquire()
        result = self._write111(CMD_SET_COLOR, redValue, greenValue, blueValue)
        self._lock.release()
        return result

    def reset(self):
        #		self._lock.acquire()
        i = 0
        while i < 5:
            self._port.flushInput()
            self._port.read(1)
            i += 1
            print("reset------------clear data-----------")
        self._crc_clear()
