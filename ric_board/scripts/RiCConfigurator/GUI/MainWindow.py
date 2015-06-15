import json
import rospkg
from xml.etree import ElementTree
from lxml.etree import Element, SubElement, XML
from xml.dom import minidom
from BAL.Devices.CloseLoopTwo import CloseLoopTwo
from BAL.Devices.Battery import Battery
from BAL.Devices.CloseLoop import CloseLoop
from BAL.Devices.DiffClose import DiffClose
from BAL.Devices.DiffCloseFour import DiffCloseFour
from BAL.Devices.DiffOpen import DiffOpen
from BAL.Devices.Gps import Gps
from BAL.Devices.Hokuyo import Hokuyo
from BAL.Devices.Imu import Imu
from BAL.Devices.OpenLoop import OpenLoop
from BAL.Devices.Openni import Opennni
from BAL.Devices.Ppm import Ppm
from BAL.Devices.Relay import Relay
from BAL.Devices.RobotModel import RobotModel
from BAL.Devices.Servo import Servo
from BAL.Devices.Switch import Switch
from BAL.Devices.Urf import Urf
from BAL.Devices.UsbCam import UsbCam
from BAL.Interface.DeviceFrame import SERVO, BATTERY, SWITCH, IMU, PPM, GPS, RELAY, URF, CLOSE_LOP_ONE, CLOSE_LOP_TWO, \
    OPEN_LOP, DIFF_CLOSE, DIFF_OPEN, EX_DEV, HOKUYO, OPRNNI, USBCAM, DIFF_CLOSE_FOUR, ROBOT_MODEL
from GUI.ShowRiCBoard import ShowRiCBoard
from GUI.UsbRolesDialog import UsbRolesDialog

__author__ = 'tom1231'
from PyQt4.QtGui import *
from Schemes.main import Ui_MainWindow
import webbrowser
import pickle
import os.path


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.data = []
        self.motors = []
        self.currentShowDev = None
        self.root = Element('launch')

        self.actionAbout_RIC.triggered.connect(self.about)
        self.actionServo.triggered.connect(self.addServo)
        self.actionBattery_Monitor.triggered.connect(self.addBattery)
        self.actionSwitch.triggered.connect(self.addSwitch)
        self.actionIMU.triggered.connect(self.addImu)
        self.actionPPM.triggered.connect(self.addPpm)
        self.actionGPS.triggered.connect(self.addGps)
        self.actionRelay.triggered.connect(self.addRelay)
        self.actionURF.triggered.connect(self.addURF)
        self.actionMotor_with_one_encoder.triggered.connect(self.addCloseMotorOne)
        self.actionMotor_with_two_encoder.triggered.connect(self.addCloseMotorTwo)
        self.actionOpen_Loop.triggered.connect(self.addOpenMotor)
        self.actionWith_two_motors.triggered.connect(self.addDiffClose)
        self.actionWith_four_motors.triggered.connect(self.addDiffCloseFour)
        self.actionOpen_Loop_Drive.triggered.connect(self.addDiffOpen)
        self.actionUSB_Camera.triggered.connect(self.addUsbCam)
        self.actionOPENNI.triggered.connect(self.addOpenni)
        self.actionHakoyo.triggered.connect(self.addOHokuyo)
        self.actionSave.triggered.connect(self.save)
        self.actionOpen.triggered.connect(self.load)
        self.actionNew.triggered.connect(self.new)
        self.actionReconfig_RiC_Board.triggered.connect(self.configRiCBoard)
        self.actionRobot_Model.triggered.connect(self.addRobotModel)
        self.actionAbout_RiC_Board.triggered.connect(self.aboutRiCBoard)

        self.fileName.textChanged.connect(self.fileNameEven)
        self.nameSpace.textChanged.connect(self.namespaceEven)

        self.devList.itemPressed.connect(self.clickListEven)
        self.devList.doubleClicked.connect(self.devEdit)

        self.servoPorts = QComboBox()
        self.servoPorts.addItems([
            self.tr('1'),
            self.tr('2'),
            self.tr('3'),
            self.tr('4')
        ])

        self.switchPorts = QComboBox()
        self.switchPorts.addItems([
            self.tr('1'),
            self.tr('2')
        ])

        self.relayPorts = QComboBox()
        self.relayPorts.addItems([
            self.tr('1'),
            self.tr('2')
        ])

        self.urfPorts = QComboBox()
        self.urfPorts.addItems([
            self.tr('1'),
            self.tr('2'),
            self.tr('3')
        ])

        self.encoders = QComboBox()
        self.encoders.addItems([
            self.tr('1'),
            self.tr('2'),
            self.tr('3'),
            self.tr('4')
        ])

        self._ns = ''
        self._fileName = ''

        self.haveBattery = False
        self.haveIMU = False
        self.havePPM = False
        self.haveGPS = False
        self.haveCloseLoop = False
        self.haveOpenLoop = False
        self.haveDiff = False

        self.editMode = False
        self.listMode = False
        self.newDevMode = False
        self.override = True


    def about(self):
        webbrowser.open('http://wiki.ros.org/ric_board?distro=indigo')

    def aboutRiCBoard(self):
        dialog = ShowRiCBoard(self)
        dialog.show()
        dialog.exec_()

    def configRiCBoard(self):
        dialog = UsbRolesDialog(self)
        dialog.show()
        dialog.exec_()


    def new(self):
        self.interruptHandler()
        size = self.devList.count()
        for i in xrange(size):
            self.devList.takeItem(0)
        self.data = []
        self.motors = []
        self.currentShowDev = None
        self.root = Element('launch')

        self.servoPorts = QComboBox()
        self.servoPorts.addItems([
            self.tr('1'),
            self.tr('2'),
            self.tr('3'),
            self.tr('4')
        ])

        self.switchPorts = QComboBox()
        self.switchPorts.addItems([
            self.tr('1'),
            self.tr('2')
        ])

        self.relayPorts = QComboBox()
        self.relayPorts.addItems([
            self.tr('1'),
            self.tr('2')
        ])

        self.urfPorts = QComboBox()
        self.urfPorts.addItems([
            self.tr('1'),
            self.tr('2'),
            self.tr('3')
        ])

        self.encoders = QComboBox()
        self.encoders.addItems([
            self.tr('1'),
            self.tr('2'),
            self.tr('3'),
            self.tr('4')
        ])

        self._ns = ''
        self._fileName = ''

        self.haveBattery = False
        self.haveIMU = False
        self.havePPM = False
        self.haveGPS = False
        self.haveCloseLoop = False
        self.haveOpenLoop = False
        self.haveDiff = False

        self.editMode = False
        self.listMode = False
        self.newDevMode = False
        self.override = True

        self.fileName.setText(self._fileName)
        self.nameSpace.setText(self._ns)




    def load(self):
        pkg = rospkg.RosPack().get_path('ric_board')
        fileName = QFileDialog.getOpenFileName(self, self.tr("Load File"), "%s/DATA" % pkg, self.tr("RiC File (*.RIC)"))
        if fileName != '':
            self.new()
            self.override = False
            load = open(fileName)
            data = pickle.load(load)

            self._fileName = data[0]
            self._ns = data[1]

            self.nameSpace.setText(self._ns)
            self.fileName.setText(self._fileName)

            devices = data[2]

            # print devices

            for dev in devices:
                if dev['type'] == BATTERY:
                    self.currentShowDev = Battery(self.DevFrame, self.data)
                    self.currentShowDev.fromDict(dev)
                elif dev['type'] == SERVO:
                    self.currentShowDev = Servo(self.DevFrame, self.data, self.servoPorts)
                    self.currentShowDev.fromDict(dev)
                    self.servoPorts.removeItem(self.currentShowDev.findItem())
                elif dev['type'] == SWITCH:
                    self.currentShowDev = Switch(self.DevFrame, self.data, self.switchPorts)
                    self.currentShowDev.fromDict(dev)
                    self.switchPorts.removeItem(self.currentShowDev.findItem())
                elif dev['type'] == IMU:
                    self.currentShowDev = Imu(self.DevFrame, self.data)
                    self.currentShowDev.fromDict(dev)
                elif dev['type'] == PPM:
                    self.currentShowDev = Ppm(self.DevFrame, self.data)
                    self.currentShowDev.fromDict(dev)
                elif dev['type'] == GPS:
                    self.currentShowDev = Gps(self.DevFrame, self.data)
                    self.currentShowDev.fromDict(dev)
                elif dev['type'] == RELAY:
                    self.currentShowDev = Relay(self.DevFrame, self.data, self.relayPorts)
                    self.currentShowDev.fromDict(dev)
                    self.relayPorts.removeItem(self.currentShowDev.findItem())
                elif dev['type'] == URF:
                    self.currentShowDev = Urf(self.DevFrame, self.data, self.urfPorts)
                    self.currentShowDev.fromDict(dev)
                    self.urfPorts.removeItem(self.currentShowDev.findItem())
                elif dev['type'] == CLOSE_LOP_ONE:
                    self.currentShowDev = CloseLoop(self.DevFrame, self.data, self.encoders)
                    self.currentShowDev.fromDict(dev)
                    self.encoders.removeItem(self.currentShowDev.findItem())
                elif dev['type'] == CLOSE_LOP_TWO:
                    self.currentShowDev = CloseLoopTwo(self.DevFrame, self.data, self.encoders)
                    self.currentShowDev.fromDict(dev)
                    self.encoders.removeItem(self.currentShowDev.findItem())
                    self.encoders.removeItem(self.currentShowDev.findItem2())
                elif dev['type'] == OPEN_LOP:
                    self.currentShowDev = OpenLoop(self.DevFrame, self.data)
                    self.currentShowDev.fromDict(dev)
                elif dev['type'] == DIFF_CLOSE:
                    self.currentShowDev = DiffClose(self.DevFrame, self.data, self.motors)
                    self.currentShowDev.fromDict(dev)
                elif dev['type'] == DIFF_CLOSE_FOUR:
                    self.currentShowDev = DiffCloseFour(self.DevFrame, self.data, self.motors)
                    self.currentShowDev.fromDict(dev)
                elif dev['type'] == DIFF_OPEN:
                    self.currentShowDev = DiffOpen(self.DevFrame, self.data, self.motors)
                    self.currentShowDev.fromDict(dev)
                elif dev['type'] == HOKUYO:
                    self.currentShowDev = Hokuyo(self.DevFrame, self.data)
                    self.currentShowDev.fromDict(dev)
                elif dev['type'] == OPRNNI:
                    self.currentShowDev = Opennni(self.DevFrame, self.data)
                    self.currentShowDev.fromDict(dev)
                elif dev['type'] == USBCAM:
                    self.currentShowDev = UsbCam(self.DevFrame, self.data)
                    self.currentShowDev.fromDict(dev)
                elif dev['type'] == ROBOT_MODEL:
                    self.currentShowDev = RobotModel(self.DevFrame, self.data)
                    self.currentShowDev.fromDict(dev)

                if self.currentShowDev.getDevType() == BATTERY:
                    self.haveBattery = True
                if self.currentShowDev.getDevType() == IMU:
                    self.haveIMU = True
                if self.currentShowDev.getDevType() == PPM:
                    self.havePPM = True
                if self.currentShowDev.getDevType() == GPS:
                    self.haveGPS = True
                if (self.currentShowDev.getDevType() == CLOSE_LOP_ONE) or (self.currentShowDev.getDevType() == CLOSE_LOP_TWO):
                    self.haveCloseLoop = True
                    self.motors.append(self.currentShowDev.getName())
                if self.currentShowDev.getDevType() == OPEN_LOP:
                    self.haveOpenLoop = True
                    self.motors.append(self.currentShowDev.getName())
                if self.currentShowDev.getDevType() == DIFF_CLOSE or self.currentShowDev.getDevType() == DIFF_OPEN or self.currentShowDev.getDevType() == DIFF_CLOSE_FOUR:
                    self.haveDiff = True
                self.devList.addItem(QListWidgetItem(self.currentShowDev.getName()))
                self.data.append(self.currentShowDev)
                self.currentShowDev = None

    def save(self):
        pkg = rospkg.RosPack().get_path('ric_board')
        if len(self.data) == 0:
            error = QErrorMessage()
            error.setWindowTitle("File error")
            error.showMessage("Can not save a empty file.")
            error.exec_()
            return
        if self._fileName == '':
            error = QErrorMessage()
            error.setWindowTitle("File error")
            error.showMessage("Can not save file without a name.")
            error.exec_()
            return
        if not self.override:
            ans = QMessageBox.question(self, "Override", "Do you want to override this file", QMessageBox.Yes | QMessageBox.No)
            if ans == QMessageBox.Yes:
                self.override = True
            else: return

        parent = self.root
        if self._ns != '':
            parent = SubElement(self.root, 'group', {'ns': self._ns})

        at = {
            'pkg': 'ric_board',
            'type': 'Start.py',
            'name': 'RiCTraffic',
            'output': 'screen'
        }

        SubElement(parent, 'node', at)
        initDiffClose = '0'
        initDiffOpen = '0'
        initDiffCloseFour = '0'
        toSave = open("%s/config/%s.yaml" % (pkg, self._fileName), 'w')
        launch = open("%s/launch/%s.launch" % (pkg, self._fileName), 'w')
        for dev in self.data:
            if dev.getDevType() == EX_DEV:
                #if dev.toDict()['type'] == ROBOT_MODEL: dev.saveToFile(self.root)
                #else: dev.saveToFile(parent)
		dev.saveToFile(parent)
            else: dev.saveToFile(toSave)

            if dev.getDevType() == DIFF_OPEN: initDiffOpen = '1'
            if dev.getDevType() == DIFF_CLOSE: initDiffClose = '1'
            if dev.getDevType() == DIFF_CLOSE_FOUR: initDiffCloseFour = '1'

        if self.haveIMU: toSave.write('IMU_INIT: 1' + '\n')
        else: toSave.write('IMU_INIT: 0' + '\n')
        if self.haveGPS: toSave.write('GPS_INIT: 1' + '\n')
        else: toSave.write('GPS_INIT: 0' + '\n')
        if self.havePPM: toSave.write('PPM_INIT: 1' + '\n')
        else: toSave.write('PPM_INIT: 0' + '\n')
        if self.haveBattery: toSave.write('BAT_INIT: 1' + '\n')
        else: toSave.write('BAT_INIT: 0' + '\n')
        toSave.write('DIFF_INIT: ' + initDiffClose + '\n')
        toSave.write('DIFF_INIT_OP: ' + initDiffOpen + '\n')
        toSave.write('DIFF_CLOSE_FOUR: ' + initDiffCloseFour + '\n')

        toSave.write('closeLoopNum: ' + str(CloseLoop.closeLoop) + '\n')
        toSave.write('switchNum: ' + str(Switch.switchCount) + '\n')
        toSave.write('servoNum: ' + str(Servo.servoCount) + '\n')
        toSave.write('relayNum: ' + str(Relay.relayCount) + '\n')
        toSave.write('URFNum: ' + str(Urf.urfCount) + '\n')
        toSave.write('openLoopNum: ' + str(OpenLoop.openLoopNum) + '\n')


        SubElement(parent, 'rosparam', {
            'file': '$(find ric_board)/config/' + self._fileName + '.yaml',
            'command': 'load'
        })
        launch.write(prettify(self.root))

        fileData = open('%s/DATA/%s.RIC' % (pkg, self._fileName), 'wb')

        ls = []
        for dev in self.data:
            ls.append(dev.toDict())

        pickle.dump([self._fileName, self._ns, ls], fileData)

        toSave.close()
        launch.close()
        self.root = Element('launch')
        Servo.servoCount = 0
        Relay.relayCount = 0
        Urf.urfCount = 0
        Switch.switchCount = 0
        CloseLoop.closeLoop = 0
        OpenLoop.openLoopNum = 0
        # QMessageBox.information(self, 'File', 'File saved')
        error = QErrorMessage()
        error.setWindowTitle("File Saved")
        error.showMessage("To launch: $ roslaunch ric_board %s.launch " % self._fileName)
        error.exec_()

    def addRobotModel(self):
        self.interruptHandler()
        self.newDevMode = True
        self.currentShowDev = RobotModel(self.DevFrame, self.data)
        self.currentShowDev.showDetails()
        self.pushButton.clicked.connect(self.addDevToList)

    def addDiffCloseFour(self):
        if not self.haveCloseLoop or len(self.motors) < 4:
            error = QErrorMessage()
            error.setWindowTitle("Driver error")
            error.showMessage("Need to have at less four close loop motors")
            error.exec_()
            return
        if self.haveDiff:
            error = QErrorMessage()
            error.setWindowTitle("Driver error")
            error.showMessage("Can not have more")
            error.exec_()
            return
        self.interruptHandler()
        self.newDevMode = True
        self.currentShowDev = DiffCloseFour(self.DevFrame, self.data, self.motors)
        self.currentShowDev.showDetails()
        self.pushButton.clicked.connect(self.addDevToList)

    def addOpenni(self):
        self.interruptHandler()
        self.newDevMode = True
        self.currentShowDev = Opennni(self.DevFrame, self.data)
        self.currentShowDev.showDetails()
        self.pushButton.clicked.connect(self.addDevToList)

    def addOHokuyo(self):
        self.interruptHandler()
        self.newDevMode = True
        self.currentShowDev = Hokuyo(self.DevFrame, self.data)
        self.currentShowDev.showDetails()
        self.pushButton.clicked.connect(self.addDevToList)

    def addUsbCam(self):
        self.interruptHandler()
        self.newDevMode = True
        self.currentShowDev = UsbCam(self.DevFrame, self.data)
        self.currentShowDev.showDetails()
        self.pushButton.clicked.connect(self.addDevToList)

    def addDiffOpen(self):
        if not self.haveOpenLoop or len(self.motors) < 2:
            error = QErrorMessage()
            error.setWindowTitle("Driver error")
            error.showMessage("Need to have at less two open loop motors")
            error.exec_()
            return
        if self.haveDiff:
            error = QErrorMessage()
            error.setWindowTitle("Driver error")
            error.showMessage("Can not have more")
            error.exec_()
            return
        self.interruptHandler()
        self.newDevMode = True
        self.currentShowDev = DiffOpen(self.DevFrame, self.data, self.motors)
        self.currentShowDev.showDetails()
        self.pushButton.clicked.connect(self.addDevToList)

    def addDiffClose(self):
        if not self.haveCloseLoop or len(self.motors) < 2:
            error = QErrorMessage()
            error.setWindowTitle("Driver error")
            error.showMessage("Need to have at less two close loop motors")
            error.exec_()
            return
        if self.haveDiff:
            error = QErrorMessage()
            error.setWindowTitle("Driver error")
            error.showMessage("Can not have more")
            error.exec_()
            return
        self.interruptHandler()
        self.newDevMode = True
        self.currentShowDev = DiffClose(self.DevFrame, self.data, self.motors)
        self.currentShowDev.showDetails()
        self.pushButton.clicked.connect(self.addDevToList)

    def addOpenMotor(self):
        if self.haveCloseLoop:
            error = QErrorMessage()
            error.setWindowTitle("Error")
            error.showMessage("Open and close motors can not exist in the same configuration")
            error.exec_()
            return
        self.interruptHandler()
        self.newDevMode = True
        self.currentShowDev = OpenLoop(self.DevFrame, self.data)
        self.currentShowDev.showDetails()
        self.pushButton.clicked.connect(self.addDevToList)

    def addCloseMotorTwo(self):
        if self.haveOpenLoop:
            error = QErrorMessage()
            error.setWindowTitle("Error")
            error.showMessage("Open and close motors can not exist in the same configuration")
            error.exec_()
            return
        if self.encoders.count() < 2:
            error = QErrorMessage()
            error.setWindowTitle("Close Motor Error")
            error.showMessage("Need two or more encoder ports to build this motor")
            error.exec_()
            return
        self.interruptHandler()
        self.newDevMode = True
        self.currentShowDev = CloseLoopTwo(self.DevFrame, self.data, self.encoders)
        self.currentShowDev.showDetails()
        self.pushButton.clicked.connect(self.addDevToList)

    def addCloseMotorOne(self):
        if self.haveOpenLoop:
            error = QErrorMessage()
            error.setWindowTitle("Error")
            error.showMessage("Open and close motors can not exist in the same configuration")
            error.exec_()
            return
        if self.encoders.count() == 0:
            error = QErrorMessage()
            error.setWindowTitle("Close Motor Error")
            error.showMessage("Out of encoder ports")
            error.exec_()
            return
        self.interruptHandler()
        self.newDevMode = True
        self.currentShowDev = CloseLoop(self.DevFrame, self.data, self.encoders)
        self.currentShowDev.showDetails()
        self.pushButton.clicked.connect(self.addDevToList)

    def addURF(self):
        if self.urfPorts.count() == 0:
            error = QErrorMessage()
            error.setWindowTitle("URF Error")
            error.showMessage("Out of URF ports")
            error.exec_()
            return
        self.interruptHandler()
        self.newDevMode = True
        self.currentShowDev = Urf(self.DevFrame, self.data, self.urfPorts)
        self.currentShowDev.showDetails()
        self.pushButton.clicked.connect(self.addDevToList)

    def addBattery(self):
        if self.haveBattery:
            error = QErrorMessage()
            error.setWindowTitle("Battery Error")
            error.showMessage("Can't add another battery to ric board")
            error.exec_()
            return
        self.interruptHandler()
        self.newDevMode = True
        self.currentShowDev = Battery(self.DevFrame, self.data)
        self.currentShowDev.showDetails()
        self.pushButton.clicked.connect(self.addDevToList)

    def addServo(self):
        if self.servoPorts.count() == 0:
            error = QErrorMessage()
            error.setWindowTitle("Servo Error")
            error.showMessage("Out of servo ports")
            error.exec_()
            return
        self.interruptHandler()
        self.newDevMode = True
        self.currentShowDev = Servo(self.DevFrame, self.data, self.servoPorts)
        self.currentShowDev.showDetails()
        self.pushButton.clicked.connect(self.addDevToList)

    def addSwitch(self):
        if self.switchPorts.count() == 0:
            error = QErrorMessage()
            error.setWindowTitle("Switch Error")
            error.showMessage("Out of switch ports")
            error.exec_()
            return
        self.interruptHandler()
        self.newDevMode = True
        self.currentShowDev = Switch(self.DevFrame, self.data, self.switchPorts)
        self.currentShowDev.showDetails()
        self.pushButton.clicked.connect(self.addDevToList)

    def addImu(self):
        if self.haveIMU:
            error = QErrorMessage()
            error.setWindowTitle("IMU Error")
            error.showMessage("Can't add another IMU to ric board")
            error.exec_()
            return
        self.interruptHandler()
        self.newDevMode = True
        self.currentShowDev = Imu(self.DevFrame, self.data)
        self.currentShowDev.showDetails()
        self.pushButton.clicked.connect(self.addDevToList)

    def addPpm(self):
        if self.havePPM:
            error = QErrorMessage()
            error.setWindowTitle("PPM Error")
            error.showMessage("Can't add another PPM to ric board")
            error.exec_()
            return
        self.interruptHandler()
        self.newDevMode = True
        self.currentShowDev = Ppm(self.DevFrame, self.data)
        self.currentShowDev.showDetails()
        self.pushButton.clicked.connect(self.addDevToList)

    def addGps(self):
        if self.haveGPS:
            error = QErrorMessage()
            error.setWindowTitle("GPS Error")
            error.showMessage("Can't add another GPS to ric board")
            error.exec_()
            return
        self.interruptHandler()
        self.newDevMode = True
        self.currentShowDev = Gps(self.DevFrame, self.data)
        self.currentShowDev.showDetails()
        self.pushButton.clicked.connect(self.addDevToList)

    def addRelay(self):
        if self.relayPorts.count() == 0:
            error = QErrorMessage()
            error.setWindowTitle("Relay Error")
            error.showMessage("Out of relay ports")
            error.exec_()
            return
        self.interruptHandler()
        self.newDevMode = True
        self.currentShowDev = Relay(self.DevFrame, self.data, self.relayPorts)
        self.currentShowDev.showDetails()
        self.pushButton.clicked.connect(self.addDevToList)

    def clickListEven(self):
        self.interruptHandler()
        index = self.devList.currentRow()
        self.listMode = True
        self.currentShowDev = self.data[index]
        self.currentShowDev.printDetails()
        self.Edit.clicked.connect(self.devEdit)
        self.Delete.clicked.connect(self.devDelete)

    def namespaceEven(self, text):
        self._ns = str(text)

    def fileNameEven(self, text):
        self._fileName = str(text)

    def devDelete(self):
        if self.currentShowDev.getDevType() == SERVO:
            self.servoPorts.addItem(self.currentShowDev.getPort())
        if self.currentShowDev.getDevType() == BATTERY:
            self.haveBattery = False
        if self.currentShowDev.getDevType() == SWITCH:
            self.switchPorts.addItem(self.currentShowDev.getPort())
        if self.currentShowDev.getDevType() == IMU:
            self.haveIMU = False
        if self.currentShowDev.getDevType() == PPM:
            self.havePPM = False
        if self.currentShowDev.getDevType() == RELAY:
            self.relayPorts.addItem(self.currentShowDev.getPort())
        if self.currentShowDev.getDevType() == URF:
            self.urfPorts.addItem(self.currentShowDev.getPort())
        if self.currentShowDev.getDevType() == CLOSE_LOP_ONE:
            if self.haveDiff:
                QMessageBox.critical(self, "Error", "Can't delete a motor while differential drive is present")
                return
            self.motors.remove(self.currentShowDev.getName())
            self.encoders.addItem(self.currentShowDev.getEncoder())
        if self.currentShowDev.getDevType() == CLOSE_LOP_TWO:
            if self.haveDiff:
                QMessageBox.critical(self, "Error", "Can't delete a motor while differential drive is present")
                return
            self.motors.remove(self.currentShowDev.getName())
            self.encoders.addItem(self.currentShowDev.getEncoders()[0])
            self.encoders.addItem(self.currentShowDev.getEncoders()[1])
        if self.currentShowDev.getDevType() == OPEN_LOP:
            if self.haveDiff:
                QMessageBox.critical(self, "Error", "Can't delete a motor while differential drive is present")
                return
            self.motors.remove(self.currentShowDev.getName())
        if self.currentShowDev.getDevType() == DIFF_CLOSE or self.currentShowDev.getDevType() == DIFF_OPEN or self.currentShowDev.getDevType() == DIFF_CLOSE_FOUR:
            self.haveDiff = False

        self.data.remove(self.currentShowDev)
        self.devList.takeItem(self.devList.currentRow())
        self.removeAllFields()

        if len(self.motors) == 0 and self.haveCloseLoop: self.haveCloseLoop = False
        if len(self.motors) == 0 and self.haveOpenLoop: self.haveOpenLoop = False

        self.Edit.clicked.disconnect(self.devEdit)
        self.Delete.clicked.disconnect(self.devDelete)
        self.listMode = False

    def devEdit(self):
        self.interruptHandler()
        self.editMode = True
        if self.currentShowDev.getDevType() == SERVO:
            self.servoPorts.addItem(self.currentShowDev.getPort())
        if self.currentShowDev.getDevType() == SWITCH:
            self.switchPorts.addItem(self.currentShowDev.getPort())
        if self.currentShowDev.getDevType() == RELAY:
            self.relayPorts.addItem(self.currentShowDev.getPort())
        if self.currentShowDev.getDevType() == URF:
            self.urfPorts.addItem(self.currentShowDev.getPort())
        if self.currentShowDev.getDevType() == CLOSE_LOP_ONE:
            self.encoders.addItem(self.currentShowDev.getEncoder())
        if self.currentShowDev.getDevType() == CLOSE_LOP_TWO:
            self.encoders.addItem(self.currentShowDev.getEncoders()[0])
            self.encoders.addItem(self.currentShowDev.getEncoders()[1])

        self.currentShowDev.showDetails()
        self.pushButton.clicked.connect(self.editList)

    def removeAllFields(self):
        for i in xrange(self.DevFrame.layout().count()):
            self.DevFrame.layout().itemAt(i).widget().deleteLater()

    def interruptHandler(self):
        self.removeAllFields()
        if self.listMode:
            self.Edit.clicked.disconnect(self.devEdit)
            self.Delete.clicked.disconnect(self.devDelete)
            self.listMode = False
        if self.editMode:
            self.pushButton.clicked.disconnect(self.editList)
            if self.currentShowDev.getDevType() == SERVO:
                self.servoPorts.removeItem(self.currentShowDev.findItem())
            if self.currentShowDev.getDevType() == SWITCH:
                self.switchPorts.removeItem(self.currentShowDev.findItem())
            if self.currentShowDev.getDevType() == RELAY:
                self.relayPorts.removeItem(self.currentShowDev.findItem())
            if self.currentShowDev.getDevType() == URF:
                self.urfPorts.removeItem(self.currentShowDev.findItem())
            if self.currentShowDev.getDevType() == CLOSE_LOP_ONE:
                self.encoders.removeItem(self.currentShowDev.findItem())
            if self.currentShowDev.getDevType() == CLOSE_LOP_TWO:
                self.encoders.removeItem(self.currentShowDev.findItem())
                self.encoders.removeItem(self.currentShowDev.findItem2())
            self.editMode = False
        if self.newDevMode:
            self.pushButton.clicked.disconnect(self.addDevToList)
            self.newDevMode = False

    def removeFields(self):
        if self.currentShowDev.isValid():
            self.removeAllFields()
            self.pushButton.clicked.disconnect(self.removeFields)
            self.newDevMode = False

    def addDevToList(self):
        self.currentShowDev.add()
        if self.currentShowDev.isValid():
            if self.currentShowDev.getDevType() == BATTERY:
                self.haveBattery = True
            if self.currentShowDev.getDevType() == IMU:
                self.haveIMU = True
            if self.currentShowDev.getDevType() == PPM:
                self.havePPM = True
            if self.currentShowDev.getDevType() == GPS:
                self.haveGPS = True
            if (self.currentShowDev.getDevType() == CLOSE_LOP_ONE) or (self.currentShowDev.getDevType() == CLOSE_LOP_TWO):
                self.haveCloseLoop = True
                self.motors.append(self.currentShowDev.getName())
            if self.currentShowDev.getDevType() == OPEN_LOP:
                self.haveOpenLoop = True
                self.motors.append(self.currentShowDev.getName())
            if self.currentShowDev.getDevType() == DIFF_CLOSE or self.currentShowDev.getDevType() == DIFF_OPEN or self.currentShowDev.getDevType() == DIFF_CLOSE_FOUR:
                self.haveDiff = True
            self.devList.addItem(QListWidgetItem(self.currentShowDev.getName()))
            self.data.append(self.currentShowDev)
            self.removeAllFields()
            self.currentShowDev = None
            self.pushButton.clicked.disconnect(self.addDevToList)
            self.newDevMode = False

    def editList(self):
        oldName = self.currentShowDev.getName()
        self.currentShowDev.add()
        if self.currentShowDev.isValid():
            self.devList.currentItem().setText(self.currentShowDev.getName())
            self.data[self.devList.currentRow()] = self.currentShowDev
            if self.currentShowDev.getDevType() == OPEN_LOP or self.currentShowDev.getDevType() == CLOSE_LOP_ONE or self.currentShowDev.getDevType() == CLOSE_LOP_TWO:
                for i in xrange(len(self.motors)):
                    if self.motors[i] == oldName:
                        self.motors[i] = self.currentShowDev.getName()
                        break
            self.removeAllFields()
            self.currentShowDev = None
            self.pushButton.clicked.disconnect(self.editList)
            self.editMode = False
