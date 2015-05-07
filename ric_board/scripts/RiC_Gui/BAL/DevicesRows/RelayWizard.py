from BAL.Interface.GUIWizard import GUIWizard
from Tkinter import *
from tkMessageBox import showerror
__author__ = 'tom1231'


class RelayWizard(GUIWizard):
    @staticmethod
    def displayData(data):
        info = 'Type: ' + data['type'] + '\n'
        info += 'Port number: ' + data['port'] + '\n'
        return info

    def editWizard(self, data):
        frame = Frame(self.master)
        nameLabel = Label(frame, text='name:')
        portLabel = Label(frame, text='port: ')

        self.select = StringVar(frame)
        self.select.set(data[1]['port'])
        ports = apply(OptionMenu, (frame, self.select) + tuple(data[0]) + tuple(data[1]['port']))
        self.nameTextField = Entry(frame)
        self.nameTextField.insert(END, data[1]['name'])

        nameLabel.grid(sticky=W)
        portLabel.grid(sticky=W)

        self.nameTextField.grid(row=0, column=1, sticky=E)
        ports.grid(row=1, column=1, sticky=E)
        cancel = Button(frame, text='Cancel', command=self.cancel)
        add = Button(frame, text='Add', command=self.add)

        add.grid(sticky=W)
        cancel.grid(row=2, column=1, sticky=E)

        frame.pack()
        return self.finish

    def createWizard(self, itemAvailable):
        frame = Frame(self.master)
        nameLabel = Label(frame, text='name:')
        portLabel = Label(frame, text='port:')

        self.select = StringVar(frame)
        self.select.set(itemAvailable[0])
        ports = apply(OptionMenu, (frame, self.select) + tuple(itemAvailable))
        self.nameTextField = Entry(frame)
        self.nameTextField.insert(0, 'RiC_Relay')

        nameLabel.grid(sticky=W)
        portLabel.grid(sticky=W)

        self.nameTextField.grid(row=0, column=1, sticky=E)
        ports.grid(row=1, column=1, sticky=E)

        cancel = Button(frame, text='Cancel', command=self.cancel)
        add = Button(frame, text='Add', command=self.add)

        add.grid(sticky=W)
        cancel.grid(row=2, column=1, sticky=E)

        frame.pack()
        return self.finish

    def getData(self):
       return self.data

    def nameIsValid(self):
        for i in xrange(len(self.devs)):
            if self.nameTextField.get() == self.devs[i]['name'] and i != self.place:
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

    def add(self):
        if self.nameIsValid():
            self.data['type'] = 'Relay'
            self.data['name'] = self.nameTextField.get()
            self.data['port'] = self.select.get()
            self.finish.set(True)
            self.master.destroy()
        else:
            showerror(title='Error', message='Name is already taken.')

    def cancel(self):
        self.finish.set(False)
        self.master.destroy()