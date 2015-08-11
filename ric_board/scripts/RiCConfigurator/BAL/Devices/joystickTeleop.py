__author__ = 'tom1231'
from PyQt4.QtGui import *
from BAL.Interface.DeviceFrame import DeviceFrame, EX_DEV, JOYSTICK
from lxml.etree import SubElement


class JoystickTeleop(DeviceFrame):
    def __init__(self, frame, data):
        DeviceFrame.__init__(self, EX_DEV, frame, data)
        self._maxSpeed = '1'
        self._boost = '2'
        self._topic = 'diff'

    def showDetails(self, items=None):
        self.maxSpeed = QLineEdit(self._maxSpeed)
        self.boost = QLineEdit(self._boost)
        self.topic = QLineEdit(self._topic)

        self._frame.layout().addRow(QLabel('Differential drive name: '), self.topic)
        self._frame.layout().addRow(QLabel('Max Speed: '), self.maxSpeed)
        self._frame.layout().addRow(QLabel('Boost to max speed: '), self.boost)

    def add(self):
        if not self.nameIsValid():
            error = QErrorMessage()
            error.setWindowTitle("Same name error")
            error.showMessage("Name already taken.")
            error.exec_()
            self._isValid = False
            return

        self._maxSpeed = str(self.maxSpeed.text())
        self._boost = str(self.boost.text())
        self._topic = str(self.topic.text())
        self._isValid = True

    def printDetails(self):
        self._frame.layout().addRow(QLabel('Differential drive name: '), QLabel(self._topic))
        self._frame.layout().addRow(QLabel('Max Speed: '), QLabel(self._maxSpeed))
        self._frame.layout().addRow(QLabel('Boost to max speed: '), QLabel(self._boost))

    def getName(self):
        return 'joystick_teleop'

    def toDict(self):
        data = dict()

        data['type'] = JOYSTICK
        data['maxSpeed'] = self._maxSpeed
        data['boost'] = self._boost
        data['topic'] = self._topic

        return data

    def fromDict(self, data):
        self._maxSpeed = data['maxSpeed']
        self._boost = data['boost']
        self._topic = data['topic']

    def saveToFile(self, parent):
        element = SubElement(parent, 'include', {
            'file': '$(find ric_base_station)/launch/joystick_teleop.launch'
        })

        SubElement(element, 'arg', {
            'name': 'maxspeed',
            'value': self._maxSpeed
        })

        SubElement(element, 'arg', {
            'name': 'boost',
            'value': self._boost
        })

        SubElement(element, 'arg', {
            'name': 'topic',
            'value': self._topic
        })
