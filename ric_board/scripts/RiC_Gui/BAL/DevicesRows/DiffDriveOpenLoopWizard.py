from tkMessageBox import showerror

__author__ = 'tom1231'
from BAL.Interface.GUIWizard import GUIWizard
from BAL.DevicesRows.DiffDriveCloseLoopWizard import getKey
from Tkinter import *


class DiffDriveOpenLoopWizard(GUIWizard):

    @staticmethod
    def displayData(data):
        info = 'Type: ' + data[0]['type'] + '\n'
        info += 'Wheel Radius: ' + data[0]['rWheel'] + '\n'
        info += 'Wheel width: ' + data[0]['width'] + '\n'
        info += 'Max angular: ' + data[0]['maxAng'] + '\n'
        info += 'Max linear: ' + data[0]['maxLin'] + '\n'
        info += 'MotorL: ' + getKey(data[1], data[0]['motorL']) + '\n'
        info += 'MotorR: ' + getKey(data[1], data[0]['motorR']) + '\n'
        return info

    def __init__(self, icon, motors):
        GUIWizard.__init__(self, icon)
        self.master = Toplevel()
        self.master.tk.call('wm', 'iconphoto', self.master._w, self.icon)
        self.data = dict()
        self.finish = BooleanVar()
        self.choices = dict()
        for i in xrange(len(motors)):
            self.choices[motors[i]] = str(i)
        self.master.protocol('WM_DELETE_WINDOW', self.cancel)

    def createWizard(self, itemAvailable = None):
        frame = Frame(self.master)

        nameLabel = Label(frame, text='Name:')
        rWheelLabel = Label(frame, text='Radius of the wheel (in meters):')
        widthLabel = Label(frame, text='Width of the robot  (in meters):')
        maxAngLabel = Label(frame, text='Max angular:')
        maxLinLabel = Label(frame, text='Max linear:')

        self.nameTextField = Entry(frame)
        self.nameTextField.insert(0, 'diff_driver')
        self.rWheelTextField = Entry(frame)
        self.rWheelTextField.insert(0, '0.07')
        self.widthTextField = Entry(frame)
        self.widthTextField.insert(0, '0.255')
        self.maxAngTextField = Entry(frame)
        self.maxAngTextField.insert(END, '16.0')
        self.maxLinTextField = Entry(frame)
        self.maxLinTextField.insert(END, '16.0')
        self.choiceL = StringVar(frame)
        self.choiceR = StringVar(frame)
        self.choiceL.set(self.choices.keys()[0])
        self.choiceR.set(self.choices.keys()[1])

        dropL = OptionMenu(frame, self.choiceL, *self.choices)
        dropR = OptionMenu(frame, self.choiceR, *self.choices)

        cancel = Button(frame, text='Cancel', command=self.cancel)
        add = Button(frame, text='Add', command=self.add)

        nameLabel.grid(sticky=W)
        rWheelLabel.grid(sticky=W)
        widthLabel.grid(sticky=W)
        maxAngLabel.grid(sticky=W)
        maxLinLabel.grid(sticky=W)
        dropL.grid(sticky=W)
        add.grid(sticky=W)

        self.nameTextField.grid(row=0, column=1, sticky=E)
        self.rWheelTextField.grid(row=1, column=1, sticky=E)
        self.widthTextField.grid(row=2, column=1, sticky=E)
        self.maxAngTextField.grid(row=3, column=1, sticky=E)
        self.maxLinTextField.grid(row=4, column=1, sticky=E)
        dropR.grid(row=5, column=1, sticky=E)
        cancel.grid(row=6, column=1, sticky=E)

        frame.pack()
        return self.finish

    def editWizard(self, data):
        frame = Frame(self.master)

        nameLabel = Label(frame, text='Name:')
        rWheelLabel = Label(frame, text='Radius of the wheel (in meters):')
        widthLabel = Label(frame, text='Width of the robot  (in meters):')
        maxAngLabel = Label(frame, text='Max angular:')
        maxLinLabel = Label(frame, text='Max linear:')

        self.nameTextField = Entry(frame)
        self.nameTextField.insert(0, data['name'])
        self.rWheelTextField = Entry(frame)
        self.rWheelTextField.insert(0, data['rWheel'])
        self.widthTextField = Entry(frame)
        self.widthTextField.insert(0, data['width'])
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

        nameLabel.grid(sticky=W)
        rWheelLabel.grid(sticky=W)
        widthLabel.grid(sticky=W)
        maxAngLabel.grid(sticky=W)
        maxLinLabel.grid(sticky=W)
        dropL.grid(sticky=W)
        add.grid(sticky=W)

        self.nameTextField.grid(row=0, column=1, sticky=E)
        self.rWheelTextField.grid(row=1, column=1, sticky=E)
        self.widthTextField.grid(row=2, column=1, sticky=E)
        self.maxAngTextField.grid(row=3, column=1, sticky=E)
        self.maxLinTextField.grid(row=4, column=1, sticky=E)
        dropR.grid(row=5, column=1, sticky=E)
        cancel.grid(row=6, column=1, sticky=E)

        frame.pack()
        return self.finish

    def getData(self):
        return self.data

    def cancel(self):
        self.finish.set(False)
        self.master.destroy()

    def add(self):
        self.data['type'] = 'DiffOpenLoop'
        self.data['name'] = self.nameTextField.get()
        self.data['rWheel'] = self.rWheelTextField.get()
        self.data['width'] = self.widthTextField.get()
        self.data['maxAng'] = self.maxAngTextField.get()
        self.data['maxLin'] = self.maxLinTextField.get()
        if self.choiceL.get() != self.choiceR.get():
            self.data['motorL'] = self.choices[self.choiceL.get()]
            self.data['motorR'] = self.choices[self.choiceR.get()]
            self.finish.set(True)
            self.master.destroy()
        else:
            showerror(title='Error', message="You can't have the same motor on left and on right.")