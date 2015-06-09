__author__ = 'tom1231'
from PyQt4.QtGui import *
from BAL.Interface.DeviceFrame import DeviceFrame, EX_DEV, ROBOT_MODEL
from lxml.etree import Element, SubElement, XML


class RobotModel(DeviceFrame):

    def __init__(self, frame, data):
        DeviceFrame.__init__(self, EX_DEV, frame, data)
        self._filePath = ''

    def getName(self):
        return 'RobotModel'

    def saveToFile(self, parent):
        SubElement(parent, 'param', {
          'name': 'robot_description',
          'command': "$(find xacro)/xacro.py '%s'" % self._filePath
        })

    def add(self):
        if not self.nameIsValid():
            error = QErrorMessage()
            error.setWindowTitle("Same name error")
            error.showMessage("Name already taken.")
            error.exec_()
            self._isValid = False
            return
        if self._filePath == '' or self._filePath == None:
            error = QErrorMessage()
            error.setWindowTitle("File path")
            error.showMessage("File path is empty.")
            error.exec_()
            self._isValid = False
            return
        self._isValid = True

    def showDetails(self, items=None):
        browse = QPushButton('Browse')

        browse.clicked.connect(self.browse)

        self._frame.layout().addRow(QLabel('File path: '), browse)

    def browse(self):
        self._filePath = QFileDialog.getOpenFileName(self._frame, self._frame.tr("File Path"), '.', self._frame.tr("Xacro File (*.xacro)"))

    def fromDict(self, data):
        self._filePath = data['filePath']

    def toDict(self):
        data = dict()

        data['type'] = ROBOT_MODEL
        data['filePath'] = self._filePath

        return data

    def printDetails(self):
        self._frame.layout().addRow(QLabel('File path: '), QLabel(self._filePath))