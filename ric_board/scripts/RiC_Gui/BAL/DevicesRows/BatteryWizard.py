__author__ = 'tom1231'
from BAL.Interface.GUIWizard import GUIWizard
from Tkinter import *
from tkMessageBox import showerror


class BatteryWizard(GUIWizard):

    @staticmethod
    def displayData(data):
        info = 'Type: ' + data['type'] + '\n'
        info = 'Publish Hz: ' + data['pubHz'] + '\n'
        info += 'Voltage divider ratio: ' + data['voltageDividerRatio'] + '\n'
        return info


    def __init__(self, icon):
        GUIWizard.__init__(self, icon)
        self.master = Toplevel()
        self.master.tk.call('wm', 'iconphoto', self.master._w, self.icon)
        self.data = dict()
        self.finish = BooleanVar()
        self.master.protocol('WM_DELETE_WINDOW', self.cancel)

    def cancel(self):
        self.finish.set(False)
        self.master.destroy()

    def add(self):
        self.data['type'] = 'Battery'

        self.data['name'] = 'battery_monitor'
        self.data['pubHz'] = self.pubHz.get()
        self.data['voltageDividerRatio'] = self.voltageDividerRatio.get()

        self.finish.set(True)
        self.master.destroy()

    def getData(self):
        return self.data

    def editWizard(self, data):
        frame = Frame(self.master)

        pubHz = Label(frame, text='Publish Hz:')
        voltageDividerRatio = Label(frame, text='Voltage divider ratio:')

        self.pubHz = Entry(frame)
        self.pubHz.insert(0, data['pubHz'])
        self.voltageDividerRatio = Entry(frame)
        self.voltageDividerRatio.insert(0, data['voltageDividerRatio'])

        cancel = Button(frame, text='Cancel', command=self.cancel)
        add = Button(frame, text='Add', command=self.add)

        pubHz.grid(sticky=W)
        voltageDividerRatio.grid(sticky=W)
        add.grid(sticky=W)

        self.pubHz.grid(row=0, column=1, sticky=E)
        self.voltageDividerRatio.grid(row=1, column=1, sticky=E)
        cancel.grid(row=2, column=1, sticky=E)

        frame.pack()
        return self.finish

    def createWizard(self, itemAvailable=None):
        frame = Frame(self.master)

        pubHz = Label(frame, text='Publish Hz:')
        voltageDividerRatio = Label(frame, text='Voltage divider ratio:')

        self.pubHz = Entry(frame)
        self.pubHz.insert(0, '10')
        self.voltageDividerRatio = Entry(frame)
        self.voltageDividerRatio.insert(0, '6')

        cancel = Button(frame, text='Cancel', command=self.cancel)
        add = Button(frame, text='Add', command=self.add)

        pubHz.grid(sticky=W)
        voltageDividerRatio.grid(sticky=W)
        add.grid(sticky=W)

        self.pubHz.grid(row=0, column=1, sticky=E)
        self.voltageDividerRatio.grid(row=1, column=1, sticky=E)
        cancel.grid(row=2, column=1, sticky=E)

        frame.pack()
        return self.finish





