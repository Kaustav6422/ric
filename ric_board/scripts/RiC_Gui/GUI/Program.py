import rospy
from BAL.DevicesRows import MotorOpenLoopWizard
from BAL.DevicesRows.BatteryWizard import BatteryWizard
from BAL.DevicesRows.DiffDriveOpenLoopWizard import DiffDriveOpenLoopWizard
from BAL.DevicesRows.MotorCloseLoopWizardTwoEnc import MotorCloseTwoEncLoopWizard


__author__ = 'tom1231'

from BAL.DevicesRows.MotorOpenLoopWizard import MotorOpenLoopWizard
from tkFileDialog import asksaveasfile
from BAL.DevicesRows.DiffDriveCloseLoopWizard import DiffDriveCloseLoopWizard
from BAL.DevicesRows.GPSWizard import GPSWizard
from BAL.DevicesRows.LaunchWizard import LaunchWizard
from BAL.DevicesRows.PPMWizard import PPMWizard
from BAL.DevicesRows.RelayWizard import RelayWizard
from BAL.DevicesRows.URFWizard import URFWizard
from Tkinter import *
from BAL.DevicesRows.ServoWizard import ServoWizard
from BAL.DevicesRows.SwitchWizard import SwitchWizard
from BAL.DevicesRows.IMUWizard import IMUWizard
from BAL.DevicesRows.MotorCloseLoopWizard import MotorCloseLoopWizard
from tkMessageBox import *
from tkSimpleDialog import *
from tkFileDialog import askopenfile
from idlelib.ToolTip import ToolTip
from ast import literal_eval
from os import system

class Program():
    def __init__(self, pkgPath):
        self.pkgPath = pkgPath
        self.nameOfFile = ''
        self.launch = None
        self.root = Tk()
        self.root.wm_title('RiC Board configuration tool')
        self.icon = PhotoImage(file='%s/scripts/RiC_Gui/img/icon.png' % pkgPath)
        self.root.tk.call('wm', 'iconphoto', self.root._w, self.icon)
        self.root.resizable(0, 0)
        logoFrame = Frame(self.root)
        img = PhotoImage(file='%s/scripts/RiC_Gui/img/logo.png' % pkgPath)
        imgLabel = Label(logoFrame, image=img)
        imgLabel.pack()
        self.mainFrame = Frame(self.root)
        scrollBarList = Scrollbar(self.mainFrame)
        listTitle = Label(self.mainFrame, text='List of devices')
        self.listBox = Listbox(self.mainFrame, selectmode=SINGLE, yscrollcommand=scrollBarList.set, width=30)
        listTitle.grid(column=1, sticky=W)
        self.listBox.grid(column=1, sticky=W)
        self.listBox.bind('<Double-Button-1>', self.listClick)
        scrollBar = Scrollbar(self.mainFrame)
        self.info = Text(self.mainFrame, heigh=11, width=30, background='light grey', yscrollcommand=scrollBar.set)
        textTitle = Label(self.mainFrame, text='Device details')
        self.info.config(state=DISABLED)
        self.info.grid(row=1, column=2)
        textTitle.grid(row=0, column=2, sticky=W)
        scrollBar.config(command=self.info.yview)
        scrollBarList.config(command=self.listBox.yview)
        scrollBar.grid(row=1, column=3)
        scrollBarList.grid(row=1, column=0)
        self.switchPorts = ['1', '2']
        self.servoPorts = ['1', '2']
        self.relayPorts = ['1', '2']
        self.sensorPorts = ['1', '2', '3']
        self.motorsPorts = ['1', '2', '3', '4']
        self.motors = []
        self.addMenu()
        self.data = []
        self.initCloseLoop = False
        self.initOpenLoop = False
        self.initIMU = False
        self.initGPS = False
        self.initPPM = False
        self.initDiff = False
        self.initDiffOpen = False
        self.isXbeeEnable = False
        self.batteryInit = False
        self.override = True
        self.createDeleteAndEditButton()
        logoFrame.pack()
        self.mainFrame.pack()
        self.addLaunch()
        # img1 = PhotoImage(file='%s/scripts/RiC_Gui/img/gui.v01.png' % pkgPath)
        # imgLabel1= Label(self.mainFrame, image=img1).grid(row=2, column=2)
        self.root.mainloop()

    def isSameName(self, newDev):
        for dev in self.data:
            if dev['type'] == newDev['type'] and dev['name'] == newDev['name']:
                newDev['name'] += str(len(self.data) + 1)
                return

    def addServo(self):
        if len(self.servoPorts) > 0:
            servo = ServoWizard(self.icon, self.data)
            finish = servo.createWizard(self.servoPorts)
            self.mainFrame.wait_variable(finish)
            if finish.get():
                servoData = servo.getData()
                self.isSameName(servoData)
                self.data.append(servoData)
                self.listBox.insert(END, servoData['name'])
                self.servoPorts.remove(servoData['port'])
        else:
            showerror(title='Error', message="You can't build any more servo devices.")

    def addOpenDiff(self):
        if not self.initDiff:
            if not self.initDiffOpen:
                if self.initOpenLoop and len(self.motors) > 1:
                    diff = DiffDriveOpenLoopWizard(self.icon, self.motors)
                    finish = diff.createWizard()
                    self.mainFrame.wait_variable(finish)
                    if finish.get():
                        self.initDiffOpen = True
                        data = diff.getData()
                        self.data.append(data)
                        self.listBox.insert(END, data['name'])
                else:
                    showerror(title='Error', message="You can't build open differential drive, you need two or more loop motors.")
        else:
            showerror(title='Error', message="Only one differential drive can be present.")

    def addBat(self):
        if not self.batteryInit:
            battery = BatteryWizard(self.icon)
            finish = battery.createWizard()
            self.mainFrame.wait_variable(finish)
            if finish.get():
                self.batteryInit = True
                data = battery.getData()
                self.data.append(data)
                self.listBox.insert(END, data['name'])
        else:
            showerror(title='Error', message="You already have battery.")

    def addMenu(self):
        self.mainMenu = Menu(self.mainFrame)
        self.fileMenu = Menu(self.mainMenu, tearoff=0)
        self.addDevices = Menu(self.mainMenu, tearoff=0)
        motorMenu = Menu(self.addDevices, tearoff=0)
        closeMotorMenu = Menu(motorMenu, tearoff=0)
        diffMenu = Menu(self.addDevices, tearoff=0)
        helpMenu = Menu(self.mainMenu, tearoff=0)


        self.addDevices.add_command(label='Add Battery', command=self.addBat)
        self.addDevices.add_command(label='Add servo', command=self.addServo)
        self.addDevices.add_command(label='Add switch', command=self.addSwitch)
        self.addDevices.add_command(label='Add IMU', command=self.addIMU)
        self.addDevices.add_command(label='Add GPS', command=self.addGPS)
        self.addDevices.add_command(label='Add Relay', command=self.addRelay)
        self.addDevices.add_command(label='Add URF', command=self.addUrf)
        self.addDevices.add_command(label='Add PPM', command=self.addPPM)
        self.addDevices.add_cascade(label='Add Motors', menu=motorMenu)
        self.addDevices.add_cascade(label='Add Differential Drive', menu=diffMenu)

        closeMotorMenu.add_command(label='Add motor with one encoder', command=self.addCloseLoop)
        closeMotorMenu.add_command(label='Add motor with two encoder', command=self.add2EncMotor)

        motorMenu.add_cascade(label='Close Loop', menu=closeMotorMenu)
        motorMenu.add_command(label='Open Loop', command=self.addOpenLoop)

        diffMenu.add_command(label='Close Loop Drive', command=self.addDiffCL)
        diffMenu.add_command(label='Open Loop Drive', command=self.addOpenDiff)

        helpMenu.add_command(label='Setup USB rules', command=self.setupUSB)

        self.fileMenu.add_command(label='Import', command=self.load)
        self.fileMenu.add_command(label='Export', command=self.saveToFile)
        # self.fileMenu.add_command(label='Save as..', command=self.saveAs)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label='Quit', command=self.root.quit)

        self.mainMenu.add_cascade(label='File', menu=self.fileMenu)
        self.mainMenu.add_cascade(label='Add RiC Device', menu=self.addDevices)
        self.mainMenu.add_cascade(label='Help', menu=helpMenu)
        self.root.config(menu=self.mainMenu)

    def add2EncMotor(self):
        if not self.initOpenLoop:
            if len(self.motorsPorts) > 1:
                self.initCloseLoop = True
                motor = MotorCloseTwoEncLoopWizard(self.icon, self.data)
                finish = motor.createWizard(self.motorsPorts)
                self.mainFrame.wait_variable(finish)
                if finish.get():
                    data = motor.getData()
                    self.isSameName(data)
                    self.motorsPorts.remove(data['port'])
                    self.motorsPorts.remove(data['port2'])
                    self.motors.append(data['name'])
                    self.listBox.insert(END, data['name'])
                    self.data.append(data)
                else:
                    self.initCloseLoop = False
            else:
                showerror(title='Error', message='You need two or more port to build this motor.')
        else:
            showerror(title='Error', message='You can`t use close loop and open loop motors together.')

    def addLaunch(self):
        self.launch = LaunchWizard(self.mainFrame, self.mainMenu, self.edit, self.deleteFromList, self.info, self.icon)
        self.launch.createWizard()

    def addPPM(self):
        if not self.initPPM:
            ppm = PPMWizard(self.icon)
            finish = ppm.createWizard()
            self.mainFrame.wait_variable(finish)
            if finish.get():
                data = ppm.getData()
                self.isSameName(data)
                self.isSameName(data)
                self.listBox.insert(END, data['name'])
                self.data.append(data)
                self.initPPM = True
        else:
            showerror(title='Error', message='You can only create one PPM.')

    def saveAs(self):
        if len(self.data) > 0:
            file = asksaveasfile(filetypes=[("Yaml files", "*.yaml")])
            if file is not None:
                self.nameOfFile = file.name.split('/')[-1].split('.')[0]
                self.saveFile(file=file, path=self.pkgPath)
        else:
            showerror(title='Error', message='You need to fill the devices list and launch list to save')

    def saveToFile(self):
        if len(self.data) > 0:
            if not self.override:
                ans = askyesno(title='Override', message='You want to override the file %s' % self.nameOfFile)
                if not ans:
                    self.nameOfFile = ''
                self.override = True
            if self.nameOfFile == '' or self.nameOfFile == None:
                self.nameOfFile = askstring('Name of the files', 'Please enter the name of the file')
            if self.nameOfFile != None and self.nameOfFile != '':
                self.saveFile(path=self.pkgPath)
        else:
            showerror(title='Error', message='You need to fill the devices list and launch list to save')

    def addSwitch(self):
        if len(self.switchPorts) > 0:
            switch = SwitchWizard(self.icon, self.data)
            finish = switch.createWizard(self.switchPorts)
            self.mainFrame.wait_variable(finish)
            if finish.get():
                data = switch.getData()
                self.isSameName(data)
                self.data.append(data)
                self.listBox.insert(END, data['name'])
                self.initSwitch = True
                self.switchPorts.remove(data['port'])
        else:
            showerror(title='Error', message='You can`t build more switch device')

    def addIMU(self):
        if not self.initIMU:
            imu = IMUWizard(self.icon)
            finish = imu.createWizard()
            self.mainFrame.wait_variable(finish)
            if finish.get():
                imuData = imu.getData()
                self.data.append(imuData)
                self.listBox.insert(END, imuData['name'])
                self.initIMU = True
        else:
            showerror(title='Error', message='You can only build one IMU device')

    def addOpenLoop(self):
        if not self.initCloseLoop:
            self.initOpenLoop = True
            motor = MotorOpenLoopWizard(self.icon, self.data)
            finish = motor.createWizard()
            self.mainFrame.wait_variable(finish)
            if finish.get():
                motorData = motor.getData()
                self.isSameName(motorData)
                self.listBox.insert(END, motorData['name'])
                self.data.append(motorData)
                self.motors.append(motorData['name'])
            else:
                self.initOpenLoop = False
        else:
            showerror(title='Error', message='You can`t use open loop and close loop motors together.')

    def createDeleteAndEditButton(self):
        frame = Frame(self.mainFrame)
        self.deleteFromList = Button(frame, text='Delete')
        self.edit = Button(frame, text='Edit')
        self.deleteFromList.grid(column=1, padx=30)
        self.edit.grid(row=0, column=0, padx=30)
        frame.grid(row=2, column=2, sticky=N)
        ToolTip(self.deleteFromList, 'Delete the selected device')
        ToolTip(self.edit, 'Edit the selected device')

    def listClick(self, event):
        try:
            index, = self.listBox.curselection()
            self.writeToInfo(self.data[index])
            self.deleteFromList.config(command=self.deleteDev)
            self.edit.config(command=self.editDevice)
        except:
            print 'Error'

    def writeToInfo(self, data):
        self.info.config(state=NORMAL)
        self.info.delete(1.0, END)
        info = ''
        if data['type'] == 'Servo':
            info = ServoWizard.displayData(data)
        elif data['type'] == 'MotorCloseLoop':
            if data['encoderType'] == '1':
                info = MotorCloseLoopWizard.displayData(data)
            else:
                info = MotorCloseTwoEncLoopWizard.displayData(data)
        elif data['type'] == 'MotorOpenLoop':
            info = MotorOpenLoopWizard.displayData(data)
        elif data['type'] == 'DiffCloseLoop':
            motorD = dict()
            for i in xrange(len(self.motors)):
                motorD[self.motors[i]] = str(i)
            info = DiffDriveCloseLoopWizard.displayData((data, motorD))
        elif data['type'] == 'GPS':
            info = GPSWizard.displayData(data)
        elif data['type'] == 'IMU':
            info = IMUWizard.displayData(data)
        elif data['type'] == 'PPM':
            info = PPMWizard.displayData(data)
        elif data['type'] == 'Relay':
            info = RelayWizard.displayData(data)
        elif data['type'] == 'Switch':
            info = SwitchWizard.displayData(data)
        elif data['type'] == 'URF':
            info = URFWizard.displayData(data)
        elif data['type'] == 'Battery':
            info = BatteryWizard.displayData(data)
        elif data['type'] == 'DiffOpenLoop':
            motorD = dict()
            for i in xrange(len(self.motors)):
                motorD[self.motors[i]] = str(i)
            info = DiffDriveOpenLoopWizard.displayData((data, motorD))


        self.info.insert(END, info)
        self.info.config(state=DISABLED)

    def saveFile(self, file=None, path=None):
        try:
            if file == None: file = open('%s/config/%s.yaml' % (path, self.nameOfFile), 'w')
            switchCount = 0
            servoCount = 0
            closeLoop = 0
            relayCount = 0
            urfCount = 0
            openLoopNum = 0
            fileData = open('%s/DATA/%s.RiC' % (path, self.nameOfFile), 'w')
            for dev in self.data:
                # print dev
                if dev['type'] == 'Switch':
                    file.write('switch' + str(switchCount) + '/name: ' + dev['name'] + '\n')
                    file.write('switch' + str(switchCount) + '/port: ' + dev['port'] + '\n')
                    file.write('switch' + str(switchCount) + '/publishHz: ' + dev['publishHz'] + '\n')
                    switchCount += 1
                elif dev['type'] == 'Servo':
                    file.write('servo' + str(servoCount) + '/publishHz: ' + dev['publishHz'] + '\n')
                    file.write('servo' + str(servoCount) + '/name: ' + dev['name'] + '\n')
                    file.write('servo' + str(servoCount) + '/port: ' + dev['port'] + '\n')
                    file.write('servo' + str(servoCount) + '/min: ' + dev['min'] + '\n')
                    file.write('servo' + str(servoCount) + '/max: ' + dev['max'] + '\n')
                    file.write('servo' + str(servoCount) + '/initMove: ' + dev['initMove'] + '\n')
                    file.write('servo' + str(servoCount) + '/a: ' + dev['a'] + '\n')
                    file.write('servo' + str(servoCount) + '/b: ' + dev['b'] + '\n')
                    servoCount += 1
                elif dev['type'] == 'IMU':
                    file.write('IMU/publishHz: ' + dev['publishHz'] + '\n')
                    file.write('IMU/name: ' + dev['name'] + '\n')
                    file.write('IMU/frameId: ' + dev['frameId'] + '\n')
                    file.write('IMU/camp: ' + dev['camp'] + '\n')
                elif dev['type'] == 'MotorCloseLoop':
                    file.write('closeLoop' + str(closeLoop) + '/publishHz: ' + dev['publishHz'] + '\n')
                    file.write('closeLoop' + str(closeLoop) + '/name: ' + dev['name'] + '\n')
                    file.write('closeLoop' + str(closeLoop) + '/LPFAlpha: ' + dev['LPFAlpha'] + '\n')
                    file.write('closeLoop' + str(closeLoop) + '/LPFHz: ' + dev['LPFHz'] + '\n')
                    file.write('closeLoop' + str(closeLoop) + '/driverAddress: ' + dev['driverAddress'] + '\n')
                    file.write('closeLoop' + str(closeLoop) + '/channel: ' + dev['channel'] + '\n')
                    file.write('closeLoop' + str(closeLoop) + '/port: ' + dev['port'] + '\n')
                    file.write('closeLoop' + str(closeLoop) + '/PIDHz: ' + dev['PIDHz'] + '\n')
                    file.write('closeLoop' + str(closeLoop) + '/kP: ' + dev['kP'] + '\n')
                    file.write('closeLoop' + str(closeLoop) + '/kI: ' + dev['kI'] + '\n')
                    file.write('closeLoop' + str(closeLoop) + '/kD: ' + dev['kD'] + '\n')
                    file.write('closeLoop' + str(closeLoop) + '/limit: ' + dev['limit'] + '\n')
                    file.write('closeLoop' + str(closeLoop) + '/maxSpeed: ' + dev['maxSpeed'] + '\n')
                    file.write('closeLoop' + str(closeLoop) + '/cpr: ' + dev['cpr'] + '\n')
                    file.write('closeLoop' + str(closeLoop) + '/timeout: ' + dev['timeout'] + '\n')
                    file.write('closeLoop' + str(closeLoop) + '/motorType: ' + dev['motorType'] + '\n')
                    file.write('closeLoop' + str(closeLoop) + '/direction: ' + dev['direction'] + '\n')
                    file.write('closeLoop' + str(closeLoop) + '/directionE: ' + dev['directionE'] + '\n')
                    file.write('closeLoop' + str(closeLoop) + '/encoderType: ' + dev['encoderType'] + '\n')
                    if dev['encoderType'] == '2':
                        file.write('closeLoop' + str(closeLoop) + '/port2: ' + dev['port2'] + '\n')
                    closeLoop += 1
                elif dev['type'] == 'GPS':
                    file.write('GPS/publishHz: ' + dev['publishHz'] + '\n')
                    file.write('GPS/name: ' + dev['name'] + '\n')
                    file.write('GPS/frameId: ' + dev['frameId'] + '\n')
                    file.write('GPS/baudrate: ' + dev['baudrate'] + '\n')
                elif dev['type'] == 'Relay':
                    file.write('relay' + str(relayCount) + '/name: ' + dev['name'] + '\n')
                    file.write('relay' + str(relayCount) + '/port: ' + dev['port'] + '\n')
                    relayCount += 1
                elif dev['type'] == 'URF':
                    file.write('URF' + str(urfCount) + '/publishHz: ' + dev['publishHz'] + '\n')
                    file.write('URF' + str(urfCount) + '/name: ' + dev['name'] + '\n')
                    file.write('URF' + str(urfCount) + '/frameId: ' + dev['frameId'] + '\n')
                    file.write('URF' + str(urfCount) + '/type: ' + dev['urfType'] + '\n')
                    file.write('URF' + str(urfCount) + '/port: ' + dev['port'] + '\n')
                    urfCount += 1
                elif dev['type'] == 'PPM':
                    file.write('PPM/publishHz: ' + dev['publishHz'] + '\n')
                    file.write('PPM/name: ' + dev['name'] + '\n')
                elif dev['type'] == 'MotorOpenLoop':
                    file.write('openLoop' + str(openLoopNum) + '/name: ' + dev['name'] + '\n')
                    file.write('openLoop' + str(openLoopNum) + '/address: ' + dev['address'] + '\n')
                    file.write('openLoop' + str(openLoopNum) + '/channel: ' + dev['channel'] + '\n')
                    file.write('openLoop' + str(openLoopNum) + '/timeout: ' + dev['timeout'] + '\n')
                    file.write('openLoop' + str(openLoopNum) + '/max: ' + dev['max'] + '\n')
                    file.write('openLoop' + str(openLoopNum) + '/direction: ' + dev['direction'] + '\n')
                    openLoopNum += 1
                elif dev['type'] == 'Battery':
                    file.write('Battery/name: ' + dev['name'] + '\n')
                    file.write('Battery/pubHz: ' + dev['pubHz'] + '\n')
                    file.write('Battery/voltageDividerRatio: ' + dev['voltageDividerRatio'] + '\n')
                elif dev['type'] == 'DiffOpenLoop':
                    file.write('Diff/name: ' + dev['name'] + '\n')
                    file.write('Diff/rWheel: ' + dev['rWheel'] + '\n')
                    file.write('Diff/width: ' + dev['width'] + '\n')
                    file.write('Diff/maxAng: ' + dev['maxAng'] + '\n')
                    file.write('Diff/maxLin: ' + dev['maxLin'] + '\n')
                    file.write('Diff/motorL: ' + dev['motorL'] + '\n')
                    file.write('Diff/motorR: ' + dev['motorR'] + '\n')
                else:
                    file.write('Diff/publishHz: ' + dev['publishHz'] + '\n')
                    file.write('Diff/name: ' + dev['name'] + '\n')
                    file.write('Diff/rWheel: ' + dev['rWheel'] + '\n')
                    file.write('Diff/width: ' + dev['width'] + '\n')
                    file.write('Diff/baseLink: ' + dev['baseLink'] + '\n')
                    file.write('Diff/odom: ' + dev['odom'] + '\n')
                    file.write('Diff/slip: ' + dev['split'] + '\n')
                    file.write('Diff/maxAng: ' + dev['maxAng'] + '\n')
                    file.write('Diff/maxLin: ' + dev['maxLin'] + '\n')
                    file.write('Diff/motorL: ' + dev['motorL'] + '\n')
                    file.write('Diff/motorR: ' + dev['motorR'] + '\n')

                fileData.write(str(dev) + '\n')

            if self.initIMU:
                file.write('IMU_INIT: 1\n')
            else:
                file.write('IMU_INIT: 0\n')

            if self.initGPS:
                file.write('GPS_INIT: 1\n')
            else:
                file.write('GPS_INIT: 0\n')

            if self.initPPM:
                file.write('PPM_INIT: 1\n')
            else:
                file.write('PPM_INIT: 0\n')

            if self.batteryInit:
                file.write('BAT_INIT: 1\n')
            else:
                file.write('BAT_INIT: 0\n')

            if self.initDiff:
                file.write('DIFF_INIT: 1' + '\n')
            else:
                file.write('DIFF_INIT: 0' + '\n')

            if self.initDiffOpen:
                file.write('DIFF_INIT_OP: 1' + '\n')
            else:
                file.write('DIFF_INIT_OP: 0' + '\n')
            # if self.isXbeeEnable:
            #     file.write('XBEE_INIT: 1' + '\n')
            # else:
            #     file.write('XBEE_INIT: 0' + '\n')


            file.write('closeLoopNum: ' + str(closeLoop) + '\n')
            file.write('switchNum: ' + str(switchCount) + '\n')
            file.write('servoNum: ' + str(servoCount) + '\n')
            file.write('relayNum: ' + str(relayCount) + '\n')
            file.write('URFNum: ' + str(urfCount) + '\n')
            file.write('openLoopNum: ' + str(openLoopNum) + '\n')
            self.launch.save(file.name, fileData)
            file.close()
            fileData.close()
            # self.root.option_add('*Dialog.msg.width', 50)
            showinfo(title='Info',
                     message='The file has been saved.\nYaml:ric_board/config/%s.yaml\n\nLaunch:ric_board/launch/%s.launch\n\nTo run:roslaunch ric_board %s.launch' % (self.nameOfFile, self.nameOfFile, self.nameOfFile))
            # self.root.option_add('*Dialog.msg.width', -50)
        except:
            showerror(title='Error', message='File could not be save.')

    def deleteDev(self):
        try:
            index, = self.listBox.curselection()
            if (self.data[index]['type'] == 'MotorCloseLoop' or self.data[index]['type'] == 'MotorOpenLoop') and (self.initDiff or self.initDiffOpen):
                showerror(title='Error', message="You can't delete any motors when differential drive is present.")
                return
            self.info.config(state=NORMAL)
            self.info.delete(1.0, END)
            self.info.config(state=DISABLED)
            self.listBox.delete(index)
            self.dataDelete(self.data[index])
        except:
            pass

    def editDevice(self):
        try:
            index, = self.listBox.curselection()
            data = self.data[index]
            if data['type'] == 'Switch':
                device = SwitchWizard(self.icon, self.data, index)
                data = (self.switchPorts, data)
            elif data['type'] == 'Servo':
                device = ServoWizard(self.icon, self.data, index)
                data = (self.servoPorts, data)
            elif data['type'] == 'IMU':
                device = IMUWizard(self.icon)
            elif data['type'] == 'MotorCloseLoop':
                if data['encoderType'] == '1': device = MotorCloseLoopWizard(self.icon, self.data, index)
                else: device = MotorCloseTwoEncLoopWizard(self.icon, self.data, index)
                data = (self.motorsPorts, data)
            elif data['type'] == 'GPS':
                device = GPSWizard(self.icon)
            elif data['type'] == 'Relay':
                device = RelayWizard(self.icon, self.data, index)
                data = (self.relayPorts, data)
            elif data['type'] == 'URF':
                device = URFWizard(self.icon, self.data, index)
                data = (self.sensorPorts, data)
            elif data['type'] == 'PPM':
                device = PPMWizard(self.icon)
            elif data['type'] == 'DiffCloseLoop':
                device = DiffDriveCloseLoopWizard(self.icon, self.motors)
            elif data['type'] == 'DiffOpenLoop':
                device = DiffDriveOpenLoopWizard(self.icon, self.motors)
            elif data['type'] == 'MotorOpenLoop':
                device = MotorOpenLoopWizard(self.icon, self.data, index)
            elif data['type'] == 'Battery':
                device = BatteryWizard(self.icon)

            finish = device.editWizard(data)
            self.mainFrame.wait_variable(finish)
            if finish.get():
                oldName = self.data[index]['name']
                self.data[index] = device.getData()
                self.listBox.delete(index)
                self.listBox.insert(index, self.data[index]['name'])
                self.writeToInfo(self.data[index])
                if self.data[index]['type'] == 'MotorOpenLoop':
                    self.motors.remove(oldName)
                    self.motors.append(self.data[index]['name'])
                if self.data[index]['type'] == 'MotorCloseLoop':
                    self.motors.remove(oldName)
                    self.motors.append(self.data[index]['name'])
                    if data[1]['port'] != self.data[index]['port']:
                        self.motorsPorts.append(data[1]['port'])
                        self.motorsPorts.remove(self.data[index]['port'])
                        self.motorsPorts.sort()
                    if data[1]['encoderType'] == '2' and data[1]['port2'] != self.data[index]['port2']:
                        self.motorsPorts.append(data[1]['port2'])
                        self.motorsPorts.remove(self.data[index]['port2'])
                        self.motorsPorts.sort()
                if self.data[index]['type'] == 'Servo' and data[1]['port'] != self.data[index]['port']:
                    self.servoPorts.append(data[1]['port'])
                    self.servoPorts.remove(self.data[index]['port'])
                    self.servoPorts.sort()
                if self.data[index]['type'] == 'Relay' and data[1]['port'] != self.data[index]['port']:
                    self.relayPorts.append(data[1]['port'])
                    self.relayPorts.remove(self.data[index]['port'])
                    self.relayPorts.sort()
                if self.data[index]['type'] == 'Switch' and data[1]['port'] != self.data[index]['port']:
                    self.switchPorts.append(data[1]['port'])
                    self.switchPorts.remove(self.data[index]['port'])
                    self.switchPorts.sort()
                if self.data[index]['type'] == 'URF' and data[1]['port'] != self.data[index]['port']:
                    self.sensorPorts.append(data[1]['port'])
                    self.sensorPorts.remove(self.data[index]['port'])
                    self.sensorPorts.sort()
        except:
            pass

    def dataDelete(self, data):
        if data['type'] == 'Switch':
            self.switchPorts.append(data['port'])
            self.switchPorts.sort()
        elif data['type'] == 'Servo':
            self.servoPorts.append(data['port'])
            self.servoPorts.sort()
        elif data['type'] == 'IMU':
            self.initIMU = False
        elif data['type'] == 'MotorCloseLoop':
            if self.checkIfLast(data): self.initCloseLoop = False
            self.motors.remove(data['name'])
            self.motorsPorts.append(data['port'])
            if data['encoderType'] == '2':
                self.motorsPorts.append(data['port2'])
            self.motorsPorts.sort()
        elif data['type'] == 'MotorOpenLoop':
            if self.checkIfLast(data): self.initOpenLoop = False
            self.initOpenLoop = False
            self.motors.remove(data['name'])
        elif data['type'] == 'GPS':
            self.initGPS = False
        elif data['type'] == 'Relay':
            self.relayPorts.append(data['port'])
            self.relayPorts.sort()
        elif data['type'] == 'URF':
            self.sensorPorts.append(data['port'])
            self.sensorPorts.sort()
        elif data['type'] == 'PPM':
            self.initPPM = False
        elif data['type'] == 'Battery':
            self.batteryInit = False
        elif data['type'] == 'DiffOpenLoop':
            self.initDiffOpen = False
        else:
            self.initDiff = False

        self.data.remove(data)

    def load(self):
        file = askopenfile(initialdir='%s/DATA' % self.pkgPath, filetypes=[("RobotICan data file", "*.RiC")])
        if file != None:
            self.nameOfFile = file.name.split('/')[-1].split('.')[0]
            self.listBox.delete(0, END)
            for i in xrange(len(self.data)):
                self.dataDelete(self.data[0])
            lines = file.read().splitlines()
            for i in range(0, len(lines)):
                if lines[0][0] == '{':
                    self.data.append(literal_eval(lines[0]))
                    lines.remove(lines[0])
                else:
                    break
            self.launch.load(''.join(lines))
            for dev in self.data:
                if dev['type'] == 'IMU':
                    self.initIMU = True
                elif dev['type'] == 'GPS':
                    self.initGPS = True
                elif dev['type'] == 'PPM':
                    self.initPPM = True
                elif dev['type'] == 'DiffCloseLoop':
                    self.initDiff = True
                elif dev['type'] == 'DiffOpenLoop':
                    self.initDiffOpen = True
                elif dev['type'] == 'MotorCloseLoop':
                    self.initCloseLoop = True
                    self.motors.append(dev['name'])
                    self.motorsPorts.remove(dev['port'])
                    self.motorsPorts.sort()
                    if dev['encoderType'] == '2':
                        self.motorsPorts.remove(dev['port2'])
                        self.motorsPorts.sort()
                elif dev['type'] == 'MotorOpenLoop':
                    self.initOpenLoop = True
                    self.motors.append(dev['name'])
                elif dev['type'] == 'Relay':
                    self.relayPorts.remove(dev['port'])
                    self.relayPorts.sort()
                elif dev['type'] == 'URF':
                    self.sensorPorts.remove(dev['port'])
                    self.sensorPorts.sort()
                elif dev['type'] == 'Switch':
                    self.switchPorts.remove(dev['port'])
                    self.switchPorts.sort()
                elif dev['type'] == 'Servo':
                    self.servoPorts.remove(dev['port'])
                    self.servoPorts.sort()
                elif dev['type'] == 'Battery':
                    self.batteryInit = True
                self.listBox.insert(END, dev['name'])
                self.override = False


    def addCloseLoop(self):
        if not self.initOpenLoop:
            if len(self.motorsPorts) > 0:
                self.initCloseLoop = True
                motor = MotorCloseLoopWizard(self.icon, self.data)
                finish = motor.createWizard(self.motorsPorts)
                self.mainFrame.wait_variable(finish)
                if finish.get():
                    data = motor.getData()
                    self.isSameName(data)
                    self.motorsPorts.remove(data['port'])
                    self.motors.append(data['name'])
                    self.listBox.insert(END, data['name'])
                    self.data.append(data)
                else:
                    self.initCloseLoop = False
            else:
                showerror(title='Error', message='There is no more port left to build another motor.')
        else:
            showerror(title='Error', message='You can`t use close loop and open loop motors together.')

    def checkIfLast(self, devToDelete):
        for dev in self.data:
            if dev['type'] == devToDelete['type'] and dev != devToDelete:
                return False
        return True

    def addGPS(self):
        if not self.initGPS:
            gps = GPSWizard(self.icon)
            finish = gps.createWizard()
            self.mainFrame.wait_variable(finish)
            if finish.get():
                data = gps.getData()
                self.listBox.insert(END, data['name'])
                self.data.append(data)
                self.initGPS = True
        else:
            showerror(title='Error', message='You can only add one GPS device')

    def addRelay(self):
        if len(self.relayPorts) > 0:
            relay = RelayWizard(self.icon, self.data)
            finish = relay.createWizard(self.relayPorts)
            self.mainFrame.wait_variable(finish)
            if finish.get():
                data = relay.getData()
                self.isSameName(data)
                self.listBox.insert(END, data['name'])
                self.data.append(data)
                self.relayPorts.remove(data['port'])
        else:
            showerror(title='Error', message='You have no relay port left')

    def addUrf(self):
        if len(self.sensorPorts) > 0:
            urf = URFWizard(self.icon, self.data)
            finish = urf.createWizard(self.sensorPorts)
            self.mainFrame.wait_variable(finish)
            if finish.get():
                data = urf.getData()
                self.isSameName(data)
                self.listBox.insert(END, data['name'])
                self.data.append(data)
                self.sensorPorts.remove(data['port'])
        else:
            showerror(title='Error', message='You have no sensor port left')

    def addDiffCL(self):
        if not self.initDiffOpen and self.initCloseLoop:
            if self.devCount('MotorCloseLoop') >= 2:
                if not self.initDiff:
                    drive = DiffDriveCloseLoopWizard(self.icon, self.motors)
                    finish = drive.createWizard()
                    self.mainFrame.wait_variable(finish)
                    if finish.get():
                        data = drive.getData()
                        self.listBox.insert(END, data['name'])
                        self.data.append(data)
                        self.initDiff = True
                else:
                    showerror(title='Error', message='You can only have one drive')
            else:
                showerror(title='Error', message='Please create more Close Loop Motor')
        else:
            showerror(title='Error', message="Can't build close differential and open differential together")

    def devCount(self, type):
        count = 0
        for dev in self.data:
            if dev['type'] == type: count += 1
        return count

    def setupUSB(self):
        ans = askstring(title='Setup USB rules', prompt="Please enter your 'sudo' password")
        print ans
        if ans == None: return
        exe = system(
            'echo %s | sudo -S cp %s/scripts/RiC_Gui/RiCRules/ricRules.rules /etc/udev/rules.d/' % (ans, self.pkgPath))
        if exe == 0:
            showinfo(title='Info', message='Setup USB rules had done successfully')
        else:
            showerror(title='Error', message='Password is incorrect')

