from tkMessageBox import showerror

__author__ = 'tom1231'
from BAL.Interface.GUIWizard import GUIWizard
from Tkinter import *

class GPSWizard(GUIWizard):
    @staticmethod
    def displayData(data):
        info = 'Type: ' + data['type'] + '\n'
        info += 'Publish Hz: ' + data['publishHz'] + '\n'
        info += 'Frame id: ' + data['frameId'] + '\n'
        info += 'Baud rate: ' + data['baudrate'] + '\n'
        return info

    def editWizard(self, data):
        frame = Frame(self.master)
        pubHzLabel = Label(frame, text='publish Hz:')
        nameLabel = Label(frame, text='name:')
        frameIdLabel = Label(frame, text='Frame Id:')
        baudrateLabel = Label(frame, text='Baud Rate:')

        self.pubHzTextField = Entry(frame)
        self.pubHzTextField.insert(END, data['publishHz'])
        self.nameTextField = Entry(frame)
        self.nameTextField.insert(END, data['name'])
        self.frameIdTextField = Entry(frame)
        self.frameIdTextField.insert(END, data['frameId'])
        self.baudrateTextField = Entry(frame)
        self.baudrateTextField.insert(END, data['baudrate'])

        pubHzLabel.grid(sticky=W)
        nameLabel.grid(sticky=W)
        frameIdLabel.grid(sticky=W)
        baudrateLabel.grid(sticky=W)

        self.pubHzTextField.grid(row=0, column=1, sticky=E)
        self.nameTextField.grid(row=1, column=1, sticky=E)
        self.frameIdTextField.grid(row=2, column=1, sticky=E)
        self.baudrateTextField.grid(row=3, column=1, sticky=E)

        cancel = Button(frame, text='Cancel', command=self.cancel)
        add = Button(frame, text='Add', command=self.add)

        cancel.grid(row=4, column=1, sticky=E)
        add.grid(row=4, sticky=W)

        frame.pack()
        return self.finish

    def createWizard(self, itemAvailable = None):
        frame = Frame(self.master)
        pubHzLabel = Label(frame, text='publish Hz:')
        nameLabel = Label(frame, text='name:')
        frameIdLabel = Label(frame, text='Frame Id:')
        baudrateLabel = Label(frame, text='Baud Rate:')

        self.pubHzTextField = Entry(frame)
        self.pubHzTextField.insert(0, '10')
        self.nameTextField = Entry(frame)
        self.nameTextField.insert(0, 'RiC_GPS')
        self.frameIdTextField = Entry(frame)
        self.frameIdTextField.insert(0, 'GPS_FRAME')
        self.baudrateTextField = Entry(frame)
        self.baudrateTextField.insert(0, '9600')

        pubHzLabel.grid(sticky=W)
        nameLabel.grid(sticky=W)
        frameIdLabel.grid(sticky=W)
        baudrateLabel.grid(sticky=W)

        self.pubHzTextField.grid(row=0, column=1, sticky=E)
        self.nameTextField.grid(row=1, column=1, sticky=E)
        self.frameIdTextField.grid(row=2, column=1, sticky=E)
        self.baudrateTextField.grid(row=3, column=1, sticky=E)

        cancel = Button(frame, text='Cancel', command=self.cancel)
        add = Button(frame, text='Add', command=self.add)

        cancel.grid(row=4, column=1, sticky=E)
        add.grid(row=4, sticky=W)

        frame.pack()
        return self.finish

    def getData(self):
        return self.data

    def __init__(self, icon):
        GUIWizard.__init__(self, icon)
        self.master = Toplevel()
        self.master.tk.call('wm', 'iconphoto', self.master._w, self.icon)
        self.data = dict()
        self.master.protocol('WM_DELETE_WINDOW', self.close)
        self.finish = BooleanVar()

    def close(self):
        self.cancel()
        # showerror(title='Error', message='please use the cancel button to exit.')

    def cancel(self):
        self.finish.set(False)
        self.master.destroy()

    def add(self):
        self.data['type'] = 'GPS'
        self.data['publishHz'] = self.pubHzTextField.get()
        self.data['name'] = self.nameTextField.get()
        self.data['frameId'] = self.frameIdTextField.get()
        self.data['baudrate'] = self.baudrateTextField.get()
        self.finish.set(True)
        self.master.destroy()