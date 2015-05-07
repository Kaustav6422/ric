from tkMessageBox import showerror

__author__ = 'tom1231'
from BAL.Interface.GUIWizard import GUIWizard
from Tkinter import *
# float rWheel,float weigh
# ,String name,String base_link,
# String odom


def getKey(data, value):
    for key, item in data.iteritems():
        if item == value:
            return key
    return None

class DiffDriveCloseLoopWizard(GUIWizard):
    @staticmethod
    def displayData(data):
        info = 'Type: ' + data[0]['type'] + '\n'
        info += 'Publish Hz: ' + data[0]['publishHz'] + '\n'
        info += 'Wheel Radius: ' + data[0]['rWheel'] + '\n'
        info += 'Wheel width: ' + data[0]['width'] + '\n'
        info += 'Base link: ' + data[0]['baseLink'] + '\n'
        info += 'Odometry: ' + data[0]['odom'] + '\n'
        info += 'Slip factor: ' + data[0]['split'] + '\n'
        info += 'Max angular: ' + data[0]['maxAng'] + '\n'
        info += 'Max linear: ' + data[0]['maxLin'] + '\n'
        info += 'MotorL: ' + getKey(data[1], data[0]['motorL']) + '\n'
        info += 'MotorR: ' + getKey(data[1], data[0]['motorR']) + '\n'
        return info

    def editWizard(self, data):
        frame = Frame(self.master)

        pubHzLabel = Label(frame, text='Publish Hz:')
        nameLabel = Label(frame, text='Name:')
        rWheelLabel = Label(frame, text='Radius of the wheel (in meters):')
        widthLabel = Label(frame, text='Width of the robot (in meters):')
        baseLinkLabel = Label(frame, text='Base Link name:')
        ondomLabel = Label(frame, text='Odometry name:')
        splitLabel = Label(frame, text='Slip factor:')
        maxAngLabel = Label(frame, text='Max angular:')
        maxLinLabel = Label(frame, text='Max linear:')


        self.pubHzTextField = Entry(frame)
        self.pubHzTextField.insert(END, data['publishHz'])
        self.nameTextField = Entry(frame)
        self.nameTextField.insert(END, data['name'])
        self.rWheelTextField = Entry(frame)
        self.rWheelTextField.insert(END, data['rWheel'])
        self.widthTextField = Entry(frame)
        self.widthTextField.insert(END, data['width'])
        self.baseLinkTextField = Entry(frame)
        self.baseLinkTextField.insert(END, data['baseLink'])
        self.odomTextField = Entry(frame)
        self.odomTextField.insert(END, data['odom'])
        self.splitTextField = Entry(frame)
        self.splitTextField.insert(END, data['split'])
        self.maxAngTextField = Entry(frame)
        self.maxAngTextField.insert(END, data['maxAng'])
        self.maxLinTextField = Entry(frame)
        self.maxLinTextField.insert(END, data['maxLin'])
        self.choiceL = StringVar(frame)
        self.choiceL.set(getKey(self.choices, data['motorL']))
        self.choiceR = StringVar(frame)
        self.choiceR.set(getKey(self.choices, data['motorR']))

        dropL = OptionMenu(frame, self.choiceL, *self.choices)
        dropR = OptionMenu(frame, self.choiceR, *self.choices)

        cancel = Button(frame, text='Cancel', command=self.cancel)
        add = Button(frame, text='Add', command=self.add)

        pubHzLabel.grid(sticky=W)
        nameLabel.grid(sticky=W)
        rWheelLabel.grid(sticky=W)
        widthLabel.grid(sticky=W)
        baseLinkLabel.grid(sticky=W)
        ondomLabel.grid(sticky=W)
        splitLabel.grid(sticky=W)
        maxAngLabel.grid(sticky=W)
        maxLinLabel.grid(sticky=W)
        dropL.grid(sticky=W)
        add.grid(sticky=W)

        self.pubHzTextField.grid(row=0, column=1, sticky=E)
        self.nameTextField.grid(row=1, column=1, sticky=E)
        self.rWheelTextField.grid(row=2, column=1, sticky=E)
        self.widthTextField.grid(row=3, column=1, sticky=E)
        self.baseLinkTextField.grid(row=4, column=1, sticky=E)
        self.odomTextField.grid(row=5, column=1, sticky=E)
        self.splitTextField.grid(row=6, column=1, sticky=E)
        self.maxAngTextField.grid(row=7, column=1, sticky=E)
        self.maxLinTextField.grid(row=8, column=1, sticky=E)
        dropR.grid(row=9, column=1, sticky=E)
        cancel.grid(row=10, column=1, sticky=E)

        frame.pack()
        return self.finish

    def createWizard(self, itemAvailable = None):
        frame = Frame(self.master)

        pubHzLabel = Label(frame, text='Publish Hz:')
        nameLabel = Label(frame, text='Name:')
        rWheelLabel = Label(frame, text='Radius of the wheel (in meters):')
        widthLabel = Label(frame, text='Width of the robot  (in meters):')
        baseLinkLabel = Label(frame, text='Base Link name:')
        ondomLabel = Label(frame, text='Odometry name:')
        splitLabel = Label(frame, text='Slip factor:')
        maxAngLabel = Label(frame, text='Max angular:')
        maxLinLabel = Label(frame, text='Max linear:')

        self.pubHzTextField = Entry(frame)
        self.pubHzTextField.insert(0, '50')
        self.nameTextField = Entry(frame)
        self.nameTextField.insert(0, 'diff_driver')
        self.rWheelTextField = Entry(frame)
        self.rWheelTextField.insert(0, '0.07')
        self.widthTextField = Entry(frame)
        self.widthTextField.insert(0, '0.255')
        self.baseLinkTextField = Entry(frame)
        self.baseLinkTextField.insert(0, 'base_link')
        self.odomTextField = Entry(frame)
        self.odomTextField.insert(0, 'odom_link')
        self.splitTextField = Entry(frame)
        self.splitTextField.insert(END, '0.85')
        self.maxAngTextField = Entry(frame)
        self.maxAngTextField.insert(END, '16.0')
        self.maxLinTextField = Entry(frame)
        self.maxLinTextField.insert(END, '16.0')
        self.motorsTextField = Entry(frame)
        self.choiceL = StringVar(frame)
        self.choiceR = StringVar(frame)
        self.choiceL.set(self.choices.keys()[0])
        self.choiceR.set(self.choices.keys()[1])

        dropL = OptionMenu(frame, self.choiceL, *self.choices)
        dropR = OptionMenu(frame, self.choiceR, *self.choices)

        cancel = Button(frame, text='Cancel', command=self.cancel)
        add = Button(frame, text='Add', command=self.add)
        pubHzLabel.grid(sticky=W)
        nameLabel.grid(sticky=W)
        rWheelLabel.grid(sticky=W)
        widthLabel.grid(sticky=W)
        baseLinkLabel.grid(sticky=W)
        ondomLabel.grid(sticky=W)
        splitLabel.grid(sticky=W)
        maxAngLabel.grid(sticky=W)
        maxLinLabel.grid(sticky=W)
        dropL.grid(sticky=W)
        add.grid(sticky=W)

        self.pubHzTextField.grid(row=0, column=1, sticky=E)
        self.nameTextField.grid(row=1, column=1, sticky=E)
        self.rWheelTextField.grid(row=2, column=1, sticky=E)
        self.widthTextField.grid(row=3, column=1, sticky=E)
        self.baseLinkTextField.grid(row=4, column=1, sticky=E)
        self.odomTextField.grid(row=5, column=1, sticky=E)
        self.splitTextField.grid(row=6, column=1, sticky=E)
        self.maxAngTextField.grid(row=7, column=1, sticky=E)
        self.maxLinTextField.grid(row=8, column=1, sticky=E)
        dropR.grid(row=9, column=1, sticky=E)
        cancel.grid(row=10, column=1, sticky=E)

        frame.pack()
        return self.finish

    def getData(self):
        return self.data

    def __init__(self, icon, motors):
        GUIWizard.__init__(self, icon)
        self.master = Toplevel()
        self.master.tk.call('wm', 'iconphoto', self.master._w, self.icon)
        self.data = dict()
        self.finish = BooleanVar()
        self.choices = dict()
        for i in xrange(len(motors)):
            self.choices[motors[i]] = str(i)
        self.master.protocol('WM_DELETE_WINDOW', self.close)


    def close(self):
        self.cancel()
        # showerror(title='Error', message='please use the cancel button to exit.')

    def add(self):
        self.data['type'] = 'DiffCloseLoop'
        self.data['publishHz'] = self.pubHzTextField.get()
        self.data['name'] = self.nameTextField.get()
        self.data['rWheel'] = self.rWheelTextField.get()
        self.data['width'] = self.widthTextField.get()
        self.data['baseLink'] = self.baseLinkTextField.get()
        self.data['odom'] = self.odomTextField.get()
        self.data['split'] = self.splitTextField.get()
        self.data['maxAng'] = self.maxAngTextField.get()
        self.data['maxLin'] = self.maxLinTextField.get()
        if self.choiceL.get() != self.choiceR.get():
            self.data['motorL'] = self.choices[self.choiceL.get()]
            self.data['motorR'] = self.choices[self.choiceR.get()]
            self.finish.set(True)
            self.master.destroy()
        else:
            showerror(title='Error', message="You can't have the same motor on left and on right.")

    def cancel(self):
        self.finish.set(False)
        self.master.destroy()