# -*- coding:utf8 -*-
#!/usr/bin/python

import serial
import time
import threading
import sys
import ctypes

class test:
    def __int__(self, comport="/dev/ttyUSB0", rate=115200):
        self._lock = threading.Lock()
        self._comport = comport
        self._rate = rate
        self._port = None
        self._crc = 0xffff