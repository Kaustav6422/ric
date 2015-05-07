from tkMessageBox import showerror

__author__ = 'tom1231'
from BAL.Interface.GUIWizard import GUIWizard
from Tkinter import *

class URFWizard(GUIWizard):
    @staticmethod
    def displayData(data):
        info = 'Type: ' + data['type'] + '\n'
        info += 'Publish Hz: ' + data['publishHz'] + '\n'
        info += 'Frame id: ' + data['frameId'] + '\n'
        if data['urfType'] == '10':
            info += 'URF Type: URF_HRLV\n'
        else:
            info += 'URF Type: URF_LV\n'
        info += 'Port number: ' + data['port'] + '\n'
        return info

    def editWizard(self, data):
        frame = Frame(self.master)

        pubHzLabel = Label(frame, text='publishHz:')
        nameLabel = Label(frame, text='Name:')
        frameIdLabel = Label(frame, text='Frame Id:')
        typeLabel = Label(frame, text='Type:')
        portNum = Label(frame, text='Port:')

        self.pubHzTextField = Entry(frame)
        self.pubHzTextField.insert(END, data[1]['publishHz'])
        self.nameTextField = Entry(frame)
        self.nameTextField.insert(END, data[1]['name'])
        self.frameIdTextField = Entry(frame)
        self.frameIdTextField.insert(END, data[1]['frameId'])
        self.portSel = StringVar(frame)
        self.portSel.set(data[1]['port'])
        self.typeSel = StringVar(frame)
        if data[1]['urfType'] == '3': self.typeSel.set('URF_HRLV')
        else: self.typeSel.set('URF_LV')

        portOp = apply(OptionMenu, (frame, self.portSel) + tuple(data[0]) + tuple(data[1]['port']))
        typeOp = OptionMenu(frame, self.typeSel, 'URF_HRLV', 'URF_LV')

        cancel = Button(frame, text='Cancel', command=self.cancel)
        add = Button(frame, text='Add', command=self.add)

        pubHzLabel.grid(sticky=W)
        nameLabel.grid(sticky=W)
        frameIdLabel.grid(sticky=W)
        typeLabel.grid(sticky=W)
        portNum.grid(sticky=W)

        self.pubHzTextField.grid(row=0, column=1, sticky=E)
        self.nameTextField.grid(row=1, column=1, sticky=E)
        self.frameIdTextField.grid(row=2, column=1, sticky=E)

        typeOp.grid(row=3, column=1, sticky=E)
        portOp.grid(row=4, column=1, sticky=E)

        add.grid(sticky=W)
        cancel.grid(row=5, column=1, sticky=E)

        frame.pack()
        return self.finish

    def createWizard(self, itemAvailable):
        frame = Frame(self.master)

        pubHzLabel = Label(frame, text='publish Hz:')
        nameLabel = Label(frame, text='Name:')
        frameIdLabel = Label(frame, text='Frame Id:')
        typeLabel = Label(frame, text='Type:')
        portNum = Label(frame, text='Port:')

        self.pubHzTextField = Entry(frame)
        self.pubHzTextField.insert(0, '50')
        self.nameTextField = Entry(frame)
        self.nameTextField.insert(0, 'RiC_URF')
        self.frameIdTextField = Entry(frame)
        self.frameIdTextField.insert(0, 'RiC_URF_Frame')

        self.portSel = StringVar(frame)
        self.portSel.set(itemAvailable[0])
        self.typeSel = StringVar(frame)
        self.typeSel.set('URF_HRLV')

        portOp = apply(OptionMenu, (frame, self.portSel) + tuple(itemAvailable))
        typeOp = OptionMenu(frame, self.typeSel, 'URF_HRLV', 'URF_LV')

        cancel = Button(frame, text='Cancel', command=self.cancel)
        add = Button(frame, text='Add', command=self.add)

        pubHzLabel.grid(sticky=W)
        nameLabel.grid(sticky=W)
        frameIdLabel.grid(sticky=W)
        typeLabel.grid(sticky=W)
        portNum.grid(sticky=W)

        self.pubHzTextField.grid(row=0, column=1, sticky=E)
        self.nameTextField.grid(row=1, column=1, sticky=E)
        self.frameIdTextField.grid(row=2, column=1, sticky=E)

        portOp.grid(row=4, column=1, sticky=E)
        typeOp.grid(row=3, column=1, sticky=E)

        add.grid(sticky=W)
        cancel.grid(row=5, column=1, sticky=E)

        frame.pack()
        return self.finish

    def getData(self):
        return self.data

    def __init__(self, icon, devs, place=-1):
        GUIWizard.__init__(self, icon)
        self.master = Toplevel()
        self.finish = BooleanVar()
        self.data = dict()
        self.master.tk.call('wm', 'iconphoto', self.master._w, self.icon)
        self.master.protocol('WM_DELETE_WINDOW', self.close)
        self.devs = devs
        self.place = place

    def nameIsValid(self):
        for i in xrange(len(self.devs)):
            if self.nameTextField.get() == self.devs[i]['name'] and i != self.place:
                return False
        return True

    def close(self):
        self.cancel()
        # showerror(title='Error', message='please use the cancel button to exit.')

    def add(self):
        if self.nameIsValid():
            self.data['type'] = 'URF'
            self.data['publishHz'] = self.pubHzTextField.get()
            self.data['name'] = self.nameTextField.get()
            self.data['frameId'] = self.frameIdTextField.get()
            if self.typeSel.get() == 'URF_HRLV':
                self.data['urfType'] = '10'
            else:
                self.data['urfType'] = '11'
            self.data['port'] = self.portSel.get()
            self.finish.set(True)
            self.master.destroy()
        else:
            showerror(title='Error', message='Name is already taken.')

    def cancel(self):
        self.finish.set(False)
        self.master.destroy()