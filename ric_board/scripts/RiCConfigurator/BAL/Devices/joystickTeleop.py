__author__ = 'tom1231'
from PyQt4.QtGui import *
from BAL.Interface.DeviceFrame import DeviceFrame, EX_DEV, JOYSTICK
from lxml.etree import SubElement


class JoystickTeleop(DeviceFrame):
    def __init__(self, frame, data):
        DeviceFrame.__init__(self, EX_DEV, frame, data)
        self._maxSpeed = '1'
        self._maxSpeedAngular = '0.5'
        self._boost = '2'
        self._topic = 'diff/command'
        self._pubHz = '20'

    def showDetails(self, items=None):
        self.maxSpeed = QLineEdit(self._maxSpeed)
        self.maxSpeedAngular = QLineEdit(self._maxSpeedAngular)
        self.boost = QLineEdit(self._boost)
        self.topic = QLineEdit(self._topic)
        self.pubHz = QLineEdit(self._pubHz)

        self._frame.layout().addRow(QLabel('Publish Hz: '), self.pubHz)
        self._frame.layout().addRow(QLabel('Differential drive topic: '), self.topic)
        self._frame.layout().addRow(QLabel('Max Speed linear: '), self.maxSpeed)
        self._frame.layout().addRow(QLabel('Max Speed angular: '), self.maxSpeedAngular)
        self._frame.layout().addRow(QLabel('Scale: '), self.boost)

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
        self._pubHz = str(self.pubHz.text())
        self._maxSpeedAngular = str(self.maxSpeedAngular.text())
        self._isValid = True

    def printDetails(self):
        self._frame.layout().addRow(QLabel('Publish Hz: '), QLabel(self._pubHz))
        self._frame.layout().addRow(QLabel('Differential drive topic: '), QLabel(self._topic))
        self._frame.layout().addRow(QLabel('Max Speed linear: '), QLabel(self._maxSpeed))
        self._frame.layout().addRow(QLabel('Max Speed angular: '), QLabel(self._maxSpeedAngular))
        self._frame.layout().addRow(QLabel('Scale: '), QLabel(self._boost))

    def getName(self):
        return 'joystick_teleop'

    def toDict(self):
        data = dict()

        data['type'] = JOYSTICK
        data['maxSpeed'] = self._maxSpeed
        data['boost'] = self._boost
        data['topic'] = self._topic
        data['maxSpeedAngular'] = self._maxSpeedAngular
        data['pubHz'] = self._pubHz

        return data

    def fromDict(self, data):
        self._maxSpeed = data['maxSpeed']
        self._boost = data['boost']
        self._topic = data['topic']
        if data.has_key('maxSpeedAngular'):
            self._maxSpeedAngular = data['maxSpeedAngular']
        if data.has_key('maxSpeedAngular'):
            self._pubHz = data['pubHz']

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

        SubElement(element, 'arg', {
            'name': 'pubHz',
            'value': self._pubHz
        })

        SubElement(element, 'arg', {
            'name': 'maxSpeedAngular',
            'value': self._maxSpeedAngular
        })