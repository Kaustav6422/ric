__author__ = 'tom1231'
from PyQt4.QtCore import QUrl
from PyQt4.QtGui import *
from BAL.Interface.DeviceFrame import DeviceFrame, EX_DEV, OPRNNI
from lxml.etree import Element, SubElement, XML


class Keyboard(DeviceFrame):
    def __init__(self, frame, data):
        DeviceFrame.__init__(self, EX_DEV, frame, data)
        self._cmd = ''

    def getName(self):
        return 'keyboardTel'

    def add(self):
        pass

    def showDetails(self, items=None):
        pass

    def fromDict(self, data):
        pass

    def printDetails(self):
        pass

    def saveToFile(self, file):
        pass

    def toDict(self):
        pass