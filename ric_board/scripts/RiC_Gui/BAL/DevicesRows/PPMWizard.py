from tkMessageBox import showerror
from BAL.Interface.GUIWizard import GUIWizard
from Tkinter import *
__author__ = 'tom1231'

class PPMWizard(GUIWizard):
    @staticmethod
    def displayData(data):
        info = 'Type: ' + data['type'] + '\n'
        info += 'Publish Hz: ' + data['publishHz'] + '\n'
        return info

    def editWizard(self, data):
        frame = Frame(self.master)

        pubHzLabel = Label(frame, text='Publish Hz:')
        nameLabel = Label(frame, text='Name:')

        self.pubHzTextField = Entry(frame)
        self.pubHzTextField.insert(END, data['publishHz'])
        self.nameTextField = Entry(frame)
        self.nameTextField.insert(END, data['name'])

        cancel = Button(frame, text='Cancel', command=self.cancel)
        add = Button(frame, text='Add', command=self.add)

        pubHzLabel.grid(sticky=W)
        nameLabel.grid(sticky=W)
        add.grid(sticky=W)

        self.pubHzTextField.grid(row=0, column=1, sticky=E)
        self.nameTextField.grid(row=1, column=1, sticky=E)
        cancel.grid(row=2, column=1, sticky=E)

        frame.pack()
        return self.finish

    def createWizard(self, itemAvailable = None):
        frame = Frame(self.master)

        pubHzLabel = Label(frame, text='Publish Hz:')
        nameLabel = Label(frame, text='Name:')

        self.pubHzTextField = Entry(frame)
        self.pubHzTextField.insert(0, '20')
        self.nameTextField = Entry(frame)
        self.nameTextField.insert(0, 'RiC_PPM')

        cancel = Button(frame, text='Cancel', command=self.cancel)
        add = Button(frame, text='Add', command=self.add)

        pubHzLabel.grid(sticky=W)
        nameLabel.grid(sticky=W)
        add.grid(sticky=W)

        self.pubHzTextField.grid(row=0, column=1, sticky=E)
        self.nameTextField.grid(row=1, column=1, sticky=E)
        cancel.grid(row=2, column=1, sticky=E)

        frame.pack()
        return self.finish

    def getData(self):
        return self.data

    def __init__(self, icon):
        GUIWizard.__init__(self, icon)
        self.data = dict()
        self.master = Toplevel()
        self.finish = BooleanVar()
        self.master.tk.call('wm', 'iconphoto', self.master._w, self.icon)
        self.master.protocol('WM_DELETE_WINDOW', self.close)

    def close(self):
        self.cancel()
        # showerror(title='Error', message='please use the cancel button to exit.')

    def add(self):
        self.data['type'] = 'PPM'
        self.data['publishHz'] = self.pubHzTextField.get()
        self.data['name'] = self.nameTextField.get()
        self.finish.set(True)
        self.master.destroy()

    def cancel(self):
        self.finish.set(False)
        self.master.destroy()