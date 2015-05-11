from Tkinter import *
from idlelib.ToolTip import ToolTip
from tkMessageBox import showerror
from BAL.Interface.GUIWizard import GUIWizard

__author__ = 'tom1231'


class MotorCloseTwoEncLoopWizard(GUIWizard):

    @staticmethod
    def displayData(data):
        info = 'Type: ' + data['type'] + '\n'
        info += 'Publish Hz: ' + data['publishHz'] + '\n'
        info += 'LPFAlpha parameter: ' + data['LPFAlpha'] + '\n'
        info += 'LPF Hz: ' + data['LPFHz'] + '\n'
        info += 'Driver Address: ' + data['driverAddress'] + '\n'
        info += 'Channel: ' + data['channel'] + '\n'
        info += 'Port1 number: ' + data['port'] + '\n'
        info += 'Port2 number: ' + data['port2'] + '\n'
        info += 'PID Hz: ' + data['PIDHz'] + '\n'
        info += 'Kp parameter: ' + data['kP'] + '\n'
        info += 'Ki parameter: ' + data['kI'] + '\n'
        info += 'Kd parameter: ' + data['kD'] + '\n'
        info += 'Integral limit: ' + data['limit'] + '\n'
        info += 'Max speed: ' + data['maxSpeed'] + '\n'
        info += 'PPR parameter: ' + data['cpr'] + '\n'
        info += 'Timeout (in milliSecond): ' + data['timeout'] + '\n'
        if data['motorType'] == '1': info += 'Motor Type: Speed\n'
        else: info += 'Motor Type: Position\n'
        if data['direction'] == '1': info += 'Motor direction: Normal\n'
        else: info += 'Motor direction: Reverse\n'
        if data['directionE'] == '1': info += 'Encoder direction: Normal\n'
        else: info += 'Encoder direction: Reverse\n'
        return info

    def editWizard(self, data):
        frame = Frame(self.master)
        publishHz = Label(frame, text='publish Hz:')
        self.publishHzTextField = Entry(frame)
        self.publishHzTextField.insert(END, data[1]['publishHz'])
        publishHz.grid(column=0, sticky=W)
        self.publishHzTextField.grid(row=0, column=1, sticky=E)

        nameLabel = Label(frame, text='name:')
        self.nameTextField = Entry(frame)
        self.nameTextField.insert(END, data[1]['name'])
        nameLabel.grid(sticky=W)
        self.nameTextField.grid(row=1, column=1, sticky=E)

        LPFAplhaLabel = Label(frame, text='LPF Alpha:')
        LPFHz = Label(frame, text='LPF Hz:')
        self.LPFAlphaTextField = Entry(frame)
        self.LPFAlphaTextField.insert(END, data[1]['LPFAlpha'])
        self.LPFHzTextField = Entry(frame)
        self.LPFHzTextField.insert(END, data[1]['LPFHz'])
        LPFHz.grid(sticky=W)
        self.LPFHzTextField.grid(row=2, column=1, sticky=E)
        LPFAplhaLabel.grid(sticky=W)
        self.LPFAlphaTextField.grid(row=3, column=1, sticky=E)


        driverAddress = Label(frame, text='Driver Address:')
        channelLabel = Label(frame, text='Channel:')
        self.driverAddressTextField = Entry(frame)
        self.driverAddressTextField.insert(END, data[1]['driverAddress'])
        self.channelTextField = Entry(frame)
        self.channelTextField.insert(END, data[1]['channel'])
        driverAddress.grid(sticky=W)
        channelLabel.grid(sticky=W)
        self.driverAddressTextField.grid(row=4, column=1, sticky=E)
        self.channelTextField.grid(row=5, column=1, sticky=E)

        PIDHzLabel = Label(frame, text='PID Hz:')
        kPLabel = Label(frame, text='KP parameter:')
        kILabel = Label(frame, text='KI parameter:')
        kDLabel = Label(frame, text='KD parameter:')
        maxSpeed = Label(frame, text='Max Speed:')
        integralLimitLabel = Label(frame, text='Integral limit (Field between [0 - 1]):')
        self.PIDHzTextField = Entry(frame)
        self.PIDHzTextField.insert(END, data[1]['PIDHz'])
        self.kPTextField = Entry(frame)
        self.kPTextField.insert(END, data[1]['kP'])
        self.kITextField = Entry(frame)
        self.kITextField.insert(END, data[1]['kI'])
        self.kDTextField = Entry(frame)
        self.kDTextField.insert(END, data[1]['kD'])
        self.integralLimitTextField = Entry(frame)
        self.integralLimitTextField.insert(END, data[1]['limit'])
        self.maxSpeedTextField = Entry(frame)
        self.maxSpeedTextField.insert(END, data[1]['maxSpeed'])
        PIDHzLabel.grid(sticky=W)
        kPLabel.grid(sticky=W)
        kILabel.grid(sticky=W)
        kDLabel.grid(sticky=W)
        maxSpeed.grid(sticky=W)
        integralLimitLabel.grid(sticky=W)
        self.PIDHzTextField.grid(row=6, column=1, sticky=E)
        self.kPTextField.grid(row=7, column=1, sticky=E)
        self.kITextField.grid(row=8, column=1, sticky=E)
        self.kDTextField.grid(row=9, column=1, sticky=E)
        self.integralLimitTextField.grid(row=10, column=1, sticky=E)
        self.maxSpeedTextField.grid(row=11, column=1, sticky=E)

        encoderPort1 = Label(frame, text='Encoder one port: ')
        encoderPort2 = Label(frame, text='Encoder two port: ')

        self.select1 = StringVar(frame)
        self.select1.set(data[1]['port'])
        self.select2 = StringVar(frame)
        self.select2.set(data[1]['port2'])
        portOp1 = apply(OptionMenu, (frame, self.select1) + (tuple(data[0]) + tuple(data[1]['port'])))

        portOp2 = apply(OptionMenu, (frame, self.select2) + (tuple(data[0]) + tuple(data[1]['port2'])))

        cprLabel = Label(frame, text='PPR parameter (CPR * 4):')

        ToolTip(cprLabel, 'CPR: Cycles Per Revolution. \nThe number of full quadrature cycles per full shaft revolution (360 mechanical degrees)')
        timeoutLabel = Label(frame, text='Timeout( in milliSecond ):')
        typeLabel = Label(frame, text='type:')
        self.cprTextField = Entry(frame)
        self.cprTextField.insert(END, data[1]['cpr'])
        self.timeoutTextField = Entry(frame)
        self.timeoutTextField.insert(END, data[1]['timeout'])
        self.type = StringVar(frame)
        if data[1]['motorType'] == '1':
            self.type.set('Speed')
        else:
            self.type.set('Position')
        typeOp = OptionMenu(frame, self.type, 'Position', 'Speed')
        cprLabel.grid(sticky=W)
        timeoutLabel.grid(sticky=W)
        encoderPort1.grid(sticky=W)
        encoderPort2.grid(sticky=W)
        typeLabel.grid(sticky=W)
        self.cprTextField.grid(row=12, column=1, sticky=E)
        self.timeoutTextField.grid(row=13, column=1, sticky=E)
        portOp1.grid(row=14, column=1, sticky=E)
        portOp2.grid(row=15, column=1, sticky=E)
        typeOp.grid(row=16, column=1, sticky=E)

        directionLabel = Label(frame, text='Reverse Motor Direction:')
        self.direction = IntVar(frame)
        if data[1]['direction'] == '1':
            self.direction.set(0)
        else:
            self.direction.set(1)
        option = Checkbutton(frame, variable=self.direction)
        directionLabel.grid(sticky=W)
        option.grid(row=17, column=1, sticky=E)

        directionELabel = Label(frame, text='Reverse Encoder Direction:')
        self.directionE = IntVar(frame)
        if data[1]['directionE'] == '1':
            self.directionE.set(0)
        else:
            self.directionE.set(1)
        optionE = Checkbutton(frame, variable=self.directionE)
        directionELabel.grid(sticky=W)
        optionE.grid(row=18, column=1, sticky=E)


        cancel = Button(frame, text='Cancel', command=self.cancel)
        add = Button(frame, text='Add', command=self.add)
        cancel.grid(column=1, sticky=E)
        add.grid(row=19, column=0, sticky=W)

        frame.pack()
        return self.finish

    def pickSabertooth(self): print('hi')

    def createWizard(self, itemAvailable):
        frame = Frame(self.master)

        mainMenu = Menu(frame, tearoff=0)
        driverTypeMenu = Menu(mainMenu, tearoff=0)
        driverTypeMenu.add_command(label='Sabertooth', command=self.pickSabertooth)
        mainMenu.add_cascade(label='Driver Type', menu=driverTypeMenu)
        self.master.config(menu=mainMenu)

        publishHz = Label(frame, text='publish Hz:')
        self.publishHzTextField = Entry(frame)
        self.publishHzTextField.insert(0, '50')
        publishHz.grid(column=0, sticky=W)
        self.publishHzTextField.grid(row=0, column=1, sticky=E)

        nameLabel = Label(frame, text='name:')
        self.nameTextField = Entry(frame)
        self.nameTextField.insert(0, 'RiC_Close_Motor')
        nameLabel.grid(sticky=W)
        self.nameTextField.grid(row=1, column=1, sticky=E)

        LPFAplhaLabel = Label(frame, text='LPF Alpha:')
        LPFHz = Label(frame, text='LPF Hz:')
        self.LPFAlphaTextField = Entry(frame)
        self.LPFAlphaTextField.insert(0, '0.7')
        self.LPFHzTextField = Entry(frame)
        self.LPFHzTextField.insert(0, '50')
        LPFHz.grid(sticky=W)
        self.LPFHzTextField.grid(row=2, column=1, sticky=E)
        LPFAplhaLabel.grid(sticky=W)
        self.LPFAlphaTextField.grid(row=3, column=1, sticky=E)

        driverAddress = Label(frame, text='Driver Address:')
        channelLabel = Label(frame, text='Channel:')
        self.driverAddressTextField = Entry(frame)
        self.driverAddressTextField.insert(0, '128')
        self.channelTextField = Entry(frame)
        self.channelTextField.insert(0, '1')
        driverAddress.grid(sticky=W)
        channelLabel.grid(sticky=W)
        self.driverAddressTextField.grid(row=4, column=1, sticky=E)
        self.channelTextField.grid(row=5, column=1, sticky=E)

        PIDHzLabel = Label(frame, text='PID Hz:')
        kPLabel = Label(frame, text='KP parameter:')
        kILabel = Label(frame, text='KI parameter:')
        kDLabel = Label(frame, text='KD parameter:')
        integralLimitLabel = Label(frame, text='Integral limit (Field between [0 - 1]):')
        maxSpeed = Label(frame, text='Max Speed:')
        self.PIDHzTextField = Entry(frame)
        self.PIDHzTextField.insert(0, '1000')
        self.kPTextField = Entry(frame)
        self.kPTextField.insert(0, '3.0')
        self.kITextField = Entry(frame)
        self.kITextField.insert(0, '3.0')
        self.kDTextField = Entry(frame)
        self.kDTextField.insert(0, '0')
        self.integralLimitTextField = Entry(frame)
        self.integralLimitTextField.insert(0, '1.0')
        self.maxSpeedTextField = Entry(frame)
        self.maxSpeedTextField.insert(0, '16.0')
        PIDHzLabel.grid(sticky=W)
        kPLabel.grid(sticky=W)
        kILabel.grid(sticky=W)
        kDLabel.grid(sticky=W)
        integralLimitLabel.grid(sticky=W)
        maxSpeed.grid(sticky=W)
        self.PIDHzTextField.grid(row=6, column=1, sticky=E)
        self.kPTextField.grid(row=7, column=1, sticky=E)
        self.kITextField.grid(row=8, column=1, sticky=E)
        self.kDTextField.grid(row=9, column=1, sticky=E)
        self.integralLimitTextField.grid(row=10, column=1, sticky=E)
        self.maxSpeedTextField.grid(row=11, column=1, sticky=E)

        cprLabel = Label(frame, text='PPR parameter (CPR * 4):')
        ToolTip(cprLabel, 'CPR: Cycles Per Revolution. \nThe number of full quadrature cycles per full shaft revolution (360 mechanical degrees)')
        timeoutLabel = Label(frame, text='Timeout (in milliSecond): ')
        typeLabel = Label(frame, text='type:')
        self.cprTextField = Entry(frame)
        self.cprTextField.insert(0, '4480')
        self.timeoutTextField = Entry(frame)
        self.timeoutTextField.insert(0, '1000')
        self.type = StringVar(frame)
        self.type.set('Speed')
        typeOp = OptionMenu(frame, self.type, 'Position', 'Speed')
        cprLabel.grid(sticky=W)
        timeoutLabel.grid(sticky=W)
        encoder1Port = Label(frame, text='Encoder one port: ')
        encoder2Port = Label(frame, text='Encoder two port: ')
        encoder1Port.grid(sticky=W)
        encoder2Port.grid(sticky=W)

        self.select1 = StringVar(frame)
        self.select1.set(itemAvailable[0])

        self.select2 = StringVar(frame)
        self.select2.set(itemAvailable[1])

        portOp1 = apply(OptionMenu, (frame, self.select1) + tuple(itemAvailable))
        portOp1.grid(row=14, column=1, sticky=E)

        portOp2 = apply(OptionMenu, (frame, self.select2) + tuple(itemAvailable))
        portOp2.grid(row=15, column=1, sticky=E)

        typeLabel.grid(sticky=W)
        self.cprTextField.grid(row=12, column=1, sticky=E)
        self.timeoutTextField.grid(row=13, column=1, sticky=E)
        typeOp.grid(row=16, column=1, sticky=E)



        directionLabel = Label(frame, text='Reverse Motor Direction:')
        self.direction = IntVar(frame)
        option = Checkbutton(frame, variable=self.direction)
        directionLabel.grid(sticky=W)
        option.grid(row=17, column=1, sticky=E)

        directionELabel = Label(frame, text='Reverse Encoder Direction:')
        self.directionE = IntVar(frame)
        optionE = Checkbutton(frame, variable=self.directionE)
        directionELabel.grid(sticky=W)
        optionE.grid(row=18, column=1, sticky=E)

        cancel = Button(frame, text='Cancel', command=self.cancel)
        add = Button(frame, text='Add', command=self.add)
        cancel.grid(column=1, sticky=E)
        add.grid(row=19, column=0, sticky=W)
        frame.pack()

        return self.finish

    def getData(self):
        return self.data

    def close(self):
        self.cancel()
        # showerror(title='Error', message='please use the cancel button to exit.')

    def nameIsValid(self):
        for i in xrange(len(self.devs)):
            if self.nameTextField.get() == self.devs[i]['name'] and i != self.place:
                showerror(title='Error', message='Name is already taken.')
                return False
            if i != self.place and self.devs[i]['type'] == 'MotorCloseLoop':
                if self.devs[i]['driverAddress'] == self.driverAddressTextField.get() and self.devs[i]['channel'] == self.channelTextField.get():
                    showerror(title='Error', message='Channel is already taken.')
                    return False

        return True

    def __init__(self, icon, devs, place=-1):
        GUIWizard.__init__(self, icon)
        self.master = Toplevel()
        self.master.tk.call('wm', 'iconphoto', self.master._w, self.icon)
        self.master.protocol('WM_DELETE_WINDOW', self.close)
        self.finish = BooleanVar()
        self.data = dict()
        self.devs = devs
        self.place = place


    def add(self):
        if self.nameIsValid():
            self.data['type'] = 'MotorCloseLoop'
            self.data['encoderType'] = '2'
            self.data['publishHz'] = self.publishHzTextField.get()
            self.data['name'] = self.nameTextField.get()
            self.data['LPFAlpha'] = self.LPFAlphaTextField.get()
            self.data['LPFHz'] = self.LPFHzTextField.get()
            self.data['driverAddress'] = self.driverAddressTextField.get()
            self.data['channel'] = self.channelTextField.get()
            self.data['port'] = self.select1.get()
            self.data['port2'] = self.select2.get()
            self.data['PIDHz'] = self.PIDHzTextField.get()
            self.data['kP'] = self.kPTextField.get()
            self.data['kI'] = self.kITextField.get()
            self.data['kD'] = self.kDTextField.get()
            self.data['limit'] = self.integralLimitTextField.get()
            self.data['maxSpeed'] = self.maxSpeedTextField.get()
            self.data['cpr'] = self.cprTextField.get()
            self.data['timeout'] = self.timeoutTextField.get()
            if self.type.get() == 'Speed':
                self.data['motorType'] = str(1)
            else: self.data['motorType'] = str(0)
            if self.direction.get():
                self.data['direction'] = str(-1)
            else: self.data['direction'] = str(1)
            if self.directionE.get():
                self.data['directionE'] = '-1'
            else:
                self.data['directionE'] = '1'
            self.master.destroy()
            self.finish.set(True)

    def cancel(self):
        self.master.destroy()
        self.finish.set(False)