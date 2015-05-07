from tkMessageBox import showerror

__author__ = 'tom1231'
from BAL.Interface.GUIWizard import GUIWizard
from Tkinter import *


class ServoWizard(GUIWizard):
    @staticmethod
    def displayData(data):
        info = 'Type: ' + data['type'] + '\n'
        info += 'Publish Hz: ' + data['publishHz'] + '\n'
        if data['initMove'] != '999.0':
            info += 'Initial move (In radians): ' + data['initMove'] + '\n'
        info += 'Port Number: ' + data['port'] + '\n'
        info += 'Max (In radians): ' + data['max'] + '\n'
        info += 'Min (In radians): ' + data['min'] + '\n'
        info += 'A parameter (In degrees): ' + data['a'] + '\n'
        info += 'B parameter (In degrees): ' + data['b'] + '\n'
        return info

    def nameIsValid(self):
        for i in xrange(len(self.devs)):
            if self.nameTextField.get() == self.devs[i]['name'] and i != self.place:
                return False
        return True

    def __init__(self, icon, devs, place=-1):
        GUIWizard.__init__(self, icon)
        self.finish = BooleanVar()
        self.data = dict()
        self.master = Toplevel()
        self.master.tk.call('wm', 'iconphoto', self.master._w, self.icon)
        self.master.protocol('WM_DELETE_WINDOW', self.cancel)
        self.devs = devs
        self.place = place

    def createWizard(self, itemAvailable):
        frame = Frame(self.master)
        publishHzLabel = Label(frame, text='Publish Hz:')
        self.publishHzTextField = Entry(frame)
        self.publishHzTextField.insert(0, '10')
        publishHzLabel.grid(row=0, sticky=W)
        self.publishHzTextField.grid(row=0, column=1, sticky=E)
        labelName = Label(frame, text='Servo Name:', width=20, anchor=W)
        labelName.grid(sticky=W, pady=1)
        rows, cols = frame.grid_size()
        self.nameTextField = Entry(frame)
        self.nameTextField.insert(0, 'RiC_Servo')
        self.nameTextField.grid(row=(rows - 1), column=1, pady=1)
        initMoveLabel = Label(frame, text='Initial position (in radians):')
        initMoveLabel.grid(sticky=W, pady=1)
        self.initMoveTextField = Entry(frame)
        self.initMoveTextField.config(state=DISABLED)
        self.initMoveTextField.grid(row=rows, column=1, pady=1)
        rows += 1
        minLabel = Label(frame, text='Minimum position (in radians):')
        minLabel.grid(sticky=W, pady=3)
        self.minTextField = Entry(frame)
        self.minTextField.insert(0, '-1.57')
        self.minTextField.grid(row=rows, column=1, pady=1)
        rows += 1
        maxLabel = Label(frame, text='Maximum position (in radians):')
        self.maxTextField = Entry(frame)
        self.maxTextField.insert(0, '1.57')
        maxLabel.grid(sticky=W, pady=1)
        self.maxTextField.grid(row=rows, column=1, pady=1)
        rows += 1
        aLabel = Label(frame, text='Parameter A (In degrees):')
        self.aTextField = Entry(frame)
        self.aTextField.insert(0, '90.0')
        aLabel.grid(sticky=W, pady=1)
        self.aTextField.grid(row=rows, column=1, pady=1)
        rows += 1
        bLabel = Label(frame, text='Parameter B (In degrees):')
        self.bTextField = Entry(frame)
        self.bTextField.insert(0, '57.3')
        bLabel.grid(sticky=W)
        self.bTextField.grid(row=rows, column=1, pady=1)
        rows += 1
        portNumLabel = Label(frame, text='Port:')
        portNumLabel.grid(sticky=W, pady=1)
        self.select = StringVar(frame)
        self.select.set(itemAvailable[0])
        ports = apply(OptionMenu, (frame, self.select) + tuple(itemAvailable))
        ports.grid(row=rows, column=1, pady=1, sticky=W)
        rows += 1
        self.checkInit = IntVar()
        checkInitBox = Checkbutton(frame, text=' Enable initial position', variable=self.checkInit, command=self.checkForInit)
        checkInitBox.grid(sticky=W)
        rows += 1
        cancel = Button(frame, text='Cancel', command=self.cancel)
        add = Button(frame, text='Add', command=self.add)
        cancel.grid(column=1, sticky=E)
        add.grid(row=rows, column=0, sticky=W)
        frame.pack()
        return self.finish

    def editWizard(self, data):
        self.checkInit = IntVar()
        frame = Frame(self.master)
        publishHzLabel = Label(frame, text='Publish Hz:')
        self.publishHzTextField = Entry(frame)
        self.publishHzTextField.insert(END, data[1]['publishHz'])
        publishHzLabel.grid(row=0, sticky=W)
        self.publishHzTextField.grid(row=0, column=1, sticky=E)
        labelName = Label(frame, text='Servo Name:', width=20, anchor=W)
        labelName.grid(sticky=W, pady=1)
        rows, cols = frame.grid_size()
        self.nameTextField = Entry(frame)
        self.nameTextField.insert(END, data[1]['name'])
        initMoveLabel = Label(frame, text='Initial position (in radians):')
        initMoveLabel.grid(sticky=W, pady=1)
        self.nameTextField.grid(row=(rows - 1), column=1, pady=1)
        self.initMoveTextField = Entry(frame)
        if data[1]['initMove'] != '999.0':
            self.checkInit.set(1)
            self.initMoveTextField.insert(END, data[1]['initMove'])
        else:
            self.initMoveTextField.config(state=DISABLED)
        self.initMoveTextField.grid(row=rows, column=1, pady=1)
        rows += 1
        minLabel = Label(frame, text='Minimum position (in radians):')
        minLabel.grid(sticky=W, pady=3)
        self.minTextField = Entry(frame)
        self.minTextField.insert(END, data[1]['min'])
        self.minTextField.grid(row=rows, column=1, pady=1)
        rows += 1
        maxLabel = Label(frame, text='Maximum position (in radians):')
        self.maxTextField = Entry(frame)
        self.maxTextField.insert(END, data[1]['max'])
        maxLabel.grid(sticky=W, pady=1)
        self.maxTextField.grid(row=rows, column=1, pady=1)
        rows += 1
        aLabel = Label(frame, text='Parameter A (In degrees):')
        self.aTextField = Entry(frame)
        self.aTextField.insert(END, data[1]['a'])
        aLabel.grid(sticky=W, pady=1)
        self.aTextField.grid(row=rows, column=1, pady=1)
        rows += 1
        bLabel = Label(frame, text='Parameter B (In degrees):')
        self.bTextField = Entry(frame)
        self.bTextField.insert(END, data[1]['b'])
        bLabel.grid(sticky=W)
        self.bTextField.grid(row=rows, column=1, pady=1)
        rows += 1
        portNumLabel = Label(frame, text='Port:')
        portNumLabel.grid(sticky=W, pady=1)
        self.select = StringVar(frame)
        self.select.set(data[1]['port'])
        ports = apply(OptionMenu, (frame, self.select) + tuple(data[0]) + tuple(data[1]['port']))
        ports.grid(row=rows, column=1, pady=1, sticky=W)
        rows += 1
        checkInitBox = Checkbutton(frame, text=' Enable initial position', variable=self.checkInit, command=self.checkForInit)
        checkInitBox.grid(sticky=W)
        rows += 1
        cancel = Button(frame, text='Cancel', command=self.cancel)
        add = Button(frame, text='Add', command=self.add)
        cancel.grid(column=1, sticky=E)
        add.grid(row=rows, column=0, sticky=W)

        frame.pack()
        return self.finish

    def getData(self):
        return self.data

    def add(self):
        if self.nameIsValid():
            self.data['type'] = 'Servo'
            self.data['publishHz'] = self.publishHzTextField.get()
            self.data['name'] = self.nameTextField.get()
            if not self.checkInit.get(): self.data['initMove'] = '999.0'
            else: self.data['initMove'] = self.initMoveTextField.get()
            self.data['port'] = self.select.get()
            self.data['min'] = self.minTextField.get()
            self.data['max'] = self.maxTextField.get()
            self.data['a'] = self.aTextField.get()
            self.data['b'] = self.bTextField.get()
            self.finish.set(True)
            self.master.destroy()
        else:
            showerror(title='Error', message='Name is already taken.')

    def cancel(self):
        self.finish.set(False)
        self.master.destroy()

    def checkForInit(self):
        if self.checkInit.get():
            self.initMoveTextField.config(state=NORMAL)
            self.initMoveTextField.insert(0, '0.0')
        else:
            self.initMoveTextField.delete(0, END)
            self.initMoveTextField.config(state=DISABLED)

