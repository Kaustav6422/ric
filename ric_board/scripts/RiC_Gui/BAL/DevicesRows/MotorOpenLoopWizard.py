__author__ = 'tom1231'
from BAL.Interface.GUIWizard import GUIWizard
from Tkinter import *
from tkMessageBox import showerror


class MotorOpenLoopWizard(GUIWizard):
    @staticmethod
    def displayData(data):
        info = 'Type: ' + data['type'] + '\n'
        info += 'Address: ' + data['address'] + '\n'
        info += 'Channel: ' + data['channel'] + '\n'
        info += 'Timeout (in millisSecond): ' + data['timeout'] + '\n'
        return info

    def editWizard(self, data):
        frame = Frame(self.master)

        name = Label(frame, text='Name:')
        address = Label(frame, text='Address:')
        channel = Label(frame, text='Channel:')
        timeout = Label(frame, text='Timeout ( in millisSecond ):')

        self.name = Entry(frame)
        self.name.insert(END, data['name'])
        self.address = Entry(frame)
        self.address.insert(END, data['address'])
        self.channel = Entry(frame)
        self.channel.insert(END, data['channel'])
        self.timeout = Entry(frame)
        self.timeout.insert(END, data['timeout'])

        add = Button(frame, text='Add', command=self.add)
        cancel = Button(frame, text='Cancel', command=self.cancel)

        name.grid(sticky=W)
        address.grid(sticky=W)
        channel.grid(sticky=W)
        timeout.grid(sticky=W)
        add.grid(sticky=W)

        self.name.grid(row=0, column=1, sticky=E)
        self.address.grid(row=1, column=1, sticky=E)
        self.channel.grid(row=2, column=1, sticky=E)
        self.timeout.grid(row=3, column=1, sticky=E)
        cancel.grid(row=4, column=1, sticky=E)

        frame.pack()
        return self.finish

    def createWizard(self, itemAvailable=None):
        frame = Frame(self.master)

        name = Label(frame, text='Name:')
        address = Label(frame, text='Address:')
        channel = Label(frame, text='Channel:')
        timeout = Label(frame, text='Timeout (in millisSecond):')

        self.name = Entry(frame)
        self.name.insert(0, 'RiC_Open_Motor')
        self.address = Entry(frame)
        self.address.insert(0, '128')
        self.channel = Entry(frame)
        self.channel.insert(0, '1')
        self.timeout = Entry(frame)
        self.timeout.insert(0, '1000')

        add = Button(frame, text='Add', command=self.add)
        cancel = Button(frame, text='Cancel', command=self.cancel)

        name.grid(sticky=W)
        address.grid(sticky=W)
        channel.grid(sticky=W)
        timeout.grid(sticky=W)
        add.grid(sticky=W)

        self.name.grid(row=0, column=1, sticky=E)
        self.address.grid(row=1, column=1, sticky=E)
        self.channel.grid(row=2, column=1, sticky=E)
        self.timeout.grid(row=3, column=1, sticky=E)
        cancel.grid(row=4, column=1, sticky=E)

        frame.pack()
        return self.finish

    def getData(self):
        return self.data

    def nameIsValid(self):
        for i in xrange(len(self.devs)):
            if self.name.get() == self.devs[i]['name'] and i != self.place:
                return False
        return True

    def __init__(self, icon, devs, place=-1):
        GUIWizard.__init__(self, icon)
        self.master = Toplevel()
        self.finish = BooleanVar()
        self.data = dict()
        self.master.tk.call('wm', 'iconphoto', self.master._w, self.icon)
        self.master.protocol('WM_DELETE_WINDOW', self.close)
        self.devs = devs
        self.place = place

    def close(self):
        self.cancel()
        # showerror(title='Error', message='please use the cancel button to exit.')

    def cancel(self):
        self.finish.set(False)
        self.master.destroy()

    def add(self):
        if self.nameIsValid():
            self.data['type'] = 'MotorOpenLoop'
            self.data['name'] = self.name.get()
            self.data['address'] = self.address.get()
            self.data['channel'] = self.channel.get()
            self.data['timeout'] = self.timeout.get()
            self.finish.set(True)
            self.master.destroy()
        else:
            showerror(title='Error', message='Name is already taken.')