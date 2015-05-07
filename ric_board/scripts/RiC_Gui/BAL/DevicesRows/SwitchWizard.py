from tkMessageBox import showerror

__author__ = 'tom1231'
from BAL.Interface.GUIWizard import GUIWizard
from Tkinter import *


class SwitchWizard(GUIWizard):
    @staticmethod
    def displayData(data):
        info = 'Type: ' + data['type'] + '\n'
        info += 'Publish Hz: ' + data['publishHz'] + '\n'
        info += 'Port number: ' + data['port'] + '\n'
        return info

    def __init__(self, icon, devs, place=-1):
        GUIWizard.__init__(self, icon)
        self.root = Toplevel()
        self.data = dict()
        self.finish = BooleanVar()
        self.sel = None
        self.root.tk.call('wm', 'iconphoto', self.root._w, self.icon)
        self.root.protocol('WM_DELETE_WINDOW', self.cancel)
        self.devs = devs
        self.place = place

    def nameIsValid(self):
        for i in xrange(len(self.devs)):
            if self.nameTextField.get() == self.devs[i]['name'] and i != self.place:
                return False
        return True

    def editWizard(self, data):
        rootF = Frame(self.root)
        self.sel = StringVar(rootF)
        self.sel.set(data[1]['port'])
        self.ports = apply(OptionMenu, (rootF, self.sel) + tuple(data[0]) + tuple(data[1]['port']))

        self.pubHzTextField = Entry(rootF)
        pubHzLabel = Label(rootF, text='Publish Hz:')
        pubHzLabel.grid(row=0, sticky=W, pady=1)
        self.pubHzTextField.grid(row=0, column=1, pady=1)
        self.pubHzTextField.insert(END, data[1]['publishHz'])
        nameLabel = Label(rootF, text='Switch name:\t               ')
        nameLabel.grid(sticky=W, pady=1)
        rows, cols = rootF.grid_size()
        self.nameTextField = Entry(rootF)
        self.nameTextField.insert(END, data[1]['name'])
        self.nameTextField.grid(row=rows - 1, column=1, pady=1)
        portLabel = Label(rootF, text='port:')
        portLabel.grid(sticky=W, pady=1)
        self.ports.grid(row=rows, column=1, sticky=E)

        cancel = Button(rootF, text='cancel', command=self.cancel)
        cancel.grid(row=rows + 1, column=1, sticky=E)
        add = Button(rootF, text='Add', command=self.done)
        add.grid(row=rows + 1, sticky=W)

        rootF.pack()
        return self.finish

    def createWizard(self, itemAvailable):
        rootF = Frame(self.root)
        self.sel = StringVar(rootF)
        self.sel.set(itemAvailable[0])
        self.ports = apply(OptionMenu, (rootF, self.sel) + tuple(itemAvailable))
        self.pubHzTextField = Entry(rootF)
        self.pubHzTextField.insert(0, '20')
        pubHzLabel = Label(rootF, text='Switches publish Hz:')
        pubHzLabel.grid(row=0, sticky=W, pady=1)
        self.pubHzTextField.grid(row=0, column=1, pady=1)
        nameLabel = Label(rootF, text='Switch name:\t               ')
        nameLabel.grid(sticky=W, pady=1)
        rows, cols = rootF.grid_size()
        self.nameTextField = Entry(rootF)
        self.nameTextField.insert(0, 'RiC_Switch')
        self.nameTextField.grid(row=rows - 1, column=1, pady=1)
        pinLabel = Label(rootF, text='port:')
        pinLabel.grid(sticky=W, pady=1)
        self.ports.grid(row=rows, column=1, pady=1, sticky=E)
        cancel = Button(rootF, text='cancel', command=self.cancel)
        cancel.grid(row=rows + 1, column=1, sticky=E)
        add = Button(rootF, text='Add', command=self.done)
        add.grid(row=rows + 1, sticky=W)
        rootF.pack()
        return self.finish

    def getData(self):
        return self.data

    def done(self):
        if self.nameIsValid():
            self.data['type'] = 'Switch'
            self.data['publishHz'] = self.pubHzTextField.get()
            self.data['name'] = self.nameTextField.get()
            self.data['port'] = self.sel.get()
            self.finish.set(True)
            self.root.destroy()
        else:
            showerror(title='Error', message='Name is already taken.')

    def cancel(self):
        self.finish.set(False)
        self.root.destroy()

