import rospkg

__author__ = 'tom1231'
from PyQt4.QtGui import *
from BAL.Interface.DeviceFrame import DeviceFrame, EX_DEV, ROBOT_MODEL
from lxml.etree import Element, SubElement, XML


class RobotModel(DeviceFrame):

    def __init__(self, frame, data):
        DeviceFrame.__init__(self, EX_DEV, frame, data)
        self._filePath = ''
        self._pkg = 'ric_description'

    def getName(self):
        return 'robot_model'

    def saveToFile(self, parent):
        SubElement(parent, 'param', {
          'name': 'robot_description',
          'command': "$(find xacro)/xacro.py '%s'" % self._filePath
        })
        SubElement(parent, 'node', {
            'name': 'robot_state_publisher',
            'pkg': 'robot_state_publisher',
            'type': 'state_publisher'
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
        self.pkg = QLineEdit(self._pkg)

        self.pkg.textChanged.connect(self.change)
        browse.clicked.connect(self.browse)

        self._frame.layout().addRow(QLabel('Package: '), self.pkg)
        self._frame.layout().addRow(QLabel('File path: '), browse)

    def change(self, text):
        self._pkg = str(text)

    def browse(self):
        self._filePath = QFileDialog.getOpenFileName(self._frame, self._frame.tr("File Path"), rospkg.RosPack().get_path(self._pkg), self._frame.tr("ALL (*.*)"))


    def fromDict(self, data):
        self._filePath = data['filePath']

    def toDict(self):
        data = dict()

        data['type'] = ROBOT_MODEL
        data['filePath'] = self._filePath

        return data

    def printDetails(self):
        self._frame.layout().addRow(QLabel('Package: '), QLabel(self._pkg))
        self._frame.layout().addRow(QLabel('File path: '), QLabel(self._filePath))
