__author__ = 'tom1231'
from BAL.Interface.GUIWizard import GUIWizard
from Tkinter import *

class IMUWizard(GUIWizard):
    @staticmethod
    def displayData(data):
        info = 'Type: ' + data['type'] + '\n'
        info += 'Publish Hz: ' + data['publishHz'] + '\n'
        info += 'Frame id: ' + data['frameId'] + '\n'
        info += 'Declination angle: ' + data['camp'] + '\n'
        return info

    def __init__(self, icon):
        GUIWizard.__init__(self, icon)
        self.master = Toplevel()
        self.master.tk.call('wm', 'iconphoto', self.master._w, self.icon)
        self.finish = BooleanVar()
        self.data = dict()
        self.master.protocol('WM_DELETE_WINDOW', self.cancel)

    def editWizard(self, data):
        frame = Frame(self.master)
        self.pubHzLabel = Label(frame, text='IMU Publish Hz:')
        self.pubHzTextField = Entry(frame)
        self.pubHzTextField.insert(END, data['publishHz'])
        self.pubHzLabel.grid(sticky=W, pady=1)
        self.pubHzTextField.grid(row=0, column=1, pady=1)
        self.nameLabel = Label(frame, text='IMU Name:')
        self.nameTextField = Entry(frame)
        self.nameTextField.insert(END, data['name'])
        self.nameLabel.grid(row=1, sticky=W, pady=1)
        self.nameTextField.grid(row=1, column=1, pady=1)
        self.frameIdLabel = Label(frame, text='Frame id:')
        self.frameIdTextField = Entry(frame)
        self.frameIdTextField.insert(END, data['frameId'])
        self.frameIdLabel.grid(row=2, sticky=W, pady=1)
        self.frameIdTextField.grid(row=2, column=1, pady=1)
        cumpLabel = Label(frame, text='Declination angle:')
        cumpLabel.grid(row=3, column=0, sticky=W)
        self.campTextFeild = Entry(frame)
        self.campTextFeild.grid(row=3, column=1, sticky=E)
        self.campTextFeild.insert(END, data['camp'])
        cancel = Button(frame, text='Cancel', command=self.cancel)
        add = Button(frame, text='Add', command=self.add)
        cancel.grid(row=4, column=1, sticky=E)
        add.grid(row=4, column=0, sticky=W)
        frame.pack()
        return self.finish

    def getData(self):
        return self.data

    def createWizard(self, option=None):
        frame = Frame(self.master)
        self.pubHzLabel = Label(frame, text='IMU Publish Hz:')
        self.pubHzTextField = Entry(frame)
        self.pubHzTextField.insert(0, '50')
        self.pubHzLabel.grid(sticky=W, pady=1)
        self.pubHzTextField.grid(row=0, column=1, pady=1)
        self.nameLabel = Label(frame, text='IMU Name:')
        self.nameTextField = Entry(frame)
        self.nameTextField.insert(0, 'RiC_IMU')
        self.nameLabel.grid(row=1, sticky=W, pady=1)
        self.nameTextField.grid(row=1, column=1, pady=1)
        self.frameIdLabel = Label(frame, text='Frame id:')
        self.frameIdTextField = Entry(frame)
        self.frameIdTextField.insert(0, 'IMU_Frame')
        self.frameIdLabel.grid(row=2, sticky=W, pady=1)
        self.frameIdTextField.grid(row=2, column=1, pady=1)
        cumpLabel = Label(frame, text='Declination angle:')
        self.campTextFeild = Entry(frame)
        self.campTextFeild.insert(0, '0')
        cumpLabel.grid(row=3, column=0, sticky=W)
        self.campTextFeild.grid(row=3, column=1, sticky=E)
        cancel = Button(frame, text='Cancel', command=self.cancel)
        add = Button(frame, text='Add', command=self.add)
        cancel.grid(row=4, column=1, sticky=E)
        add.grid(row=4, column=0, sticky=W)
        frame.pack()
        return self.finish

    def add(self):
        self.data['type'] = 'IMU'
        self.data['name'] = self.nameTextField.get()
        self.data['publishHz'] = self.pubHzTextField.get()
        self.data['frameId'] = self.frameIdTextField.get()
        self.data['camp'] = self.campTextFeild.get()
        self.master.destroy()
        self.finish.set(True)

    def cancel(self):
        self.master.destroy()
        self.finish.set(False)