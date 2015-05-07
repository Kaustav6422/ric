from tkMessageBox import showerror

__author__ = 'tom1231'
from BAL.Interface.GUIWizard import GUIWizard
from Tkinter import *
from lxml.etree import SubElement
import webbrowser

class OpenniWizard(GUIWizard):

    @staticmethod
    def displayData(data):
        info = 'Element Type: ' + data['elType'] + '\n'
        info += 'Value: ' + data['value'] + '\n'
        return info

    def editWizard(self, data):
        frame = Frame(self.master)
        value = Label(frame, text='value:')

        self.name = 'camera'
        self.value = Entry(frame)
        self.value.insert(END, data['value'])

        add = Button(frame, text='Add', command=self.add)
        cancel = Button(frame, text='cancel', command=self.cancel)

        value.grid(sticky=W)
        add.grid(sticky=W)

        self.value.grid(row=0, column=1, sticky=E)
        cancel.grid(row=1, column=1, sticky=E)

        hypLink = Label(frame, text='See openni2 default arguments', fg='blue', cursor='hand2')
        hypLink.bind('<Button-1>', self.hrfCallBack)
        hypLink.grid()

        frame.pack()
        return self.finish

    def createWizard(self, itemAvailable = None):
        frame = Frame(self.master)
        value = Label(frame, text='value:')

        self.name = 'camera'
        self.value = Entry(frame)
        self.value.insert(0, 'None')

        add = Button(frame, text='Add', command=self.add)
        cancel = Button(frame, text='cancel', command=self.cancel)

        value.grid(sticky=W)
        add.grid(sticky=W)

        self.value.grid(row=0, column=1, sticky=E)
        cancel.grid(row=1, column=1, sticky=E)

        hypLink = Label(frame, text='See openni2 default arguments', fg='blue', cursor='hand2')
        hypLink.bind('<Button-1>', self.hrfCallBack)
        hypLink.grid()

        frame.pack()
        return self.finish

    def hrfCallBack(self, event):
        webbrowser.open('http://wiki.ros.org/openni2_launch')

    def getData(self):
        return self.text, self.element, self.data

    def cancel(self):
        self.finish.set(False)
        self.master.destroy()

    def add(self):
        self.data['elType'] = 'Openni'
        self.data['value'] = self.value.get()

        self.element = SubElement(self.parent, 'include', {
            'file': '$(find openni2_launch)/launch/openni2.launch'
        })

        SubElement(self.element, 'arg', {
            'name': 'camera',
            'value': self.value.get()
        })
        self.text = 'OpanniCamera'
        self.finish.set(True)
        self.master.destroy()

    def __init__(self, parent, icon):
        GUIWizard.__init__(self, icon)
        self.master = Toplevel()
        self.finish = BooleanVar()
        self.element = None
        self.text = None
        self.parent = parent
        self.data = dict()
        self.master.tk.call('wm', 'iconphoto', self.master._w, self.icon)
        self.master.protocol('WM_DELETE_WINDOW', self.close)

    def close(self):
        self.cancel()
        # showerror(title='Error', message='please use the cancel button to exit.')