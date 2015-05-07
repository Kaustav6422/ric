
__author__ = 'tom1231'


from BAL.Interface.GUIWizard import GUIWizard
from Tkinter import *
from tkMessageBox import showerror
from lxml.etree import SubElement
import webbrowser


class HokuyoWizard(GUIWizard):
    @staticmethod
    def displayData(data):
        info = 'Element Type: ' + data['elType'] + '\n'
        info += 'Output: ' + data['output'] + '\n'
        info += 'Port: ' + data['port'] + '\n'
        info += 'Frame id: ' + data['frameId'] + '\n'
        return info

    def editWizard(self, data):
        frame = Frame(self.master)
        name = Label(frame, text='Name:')
        output = Label(frame, text='Output:')
        port = Label(frame, text='Port:')
        frameId = Label(frame, text='Frame id:')

        self.name = Entry(frame)
        self.name.insert(END, data['name'])
        self.output = Entry(frame)
        self.output.insert(END, data['output'])
        self.port = Entry(frame)
        self.port.insert(END, data['port'])
        self.frameId = Entry(frame)
        self.frameId.insert(END, data['frameId'])

        add = Button(frame, text='Add', command=self.add)
        cancel = Button(frame, text='Cancel', command=self.cancel)

        name.grid(sticky=W)
        output.grid(sticky=W)
        port.grid(sticky=W)
        frameId.grid(sticky=W)
        add.grid(sticky=W)

        self.name.grid(row=0, column=1, sticky=E)
        self.output.grid(row=1, column=1, sticky=E)
        self.port.grid(row=2, column=1, sticky=E)
        self.frameId.grid(row=3, column=1, sticky=E)
        cancel.grid(row=4, column=1, sticky=E)

        hypLink = Label(frame, text='See hokuyo default arguments', fg='blue', cursor='hand2')
        hypLink.bind('<Button-1>', self.hrfCallBack)
        hypLink.grid()

        frame.pack()
        return self.finish

    def nameIsValid(self):
        for i in xrange(len(self.names)):
            if self.name.get() == self.names[i] and i != self.place:
                return False
        return True

    def createWizard(self, itemAvailable=None):
        frame = Frame(self.master)
        name = Label(frame, text='Name:')
        output = Label(frame, text='Output:')
        port = Label(frame, text='Port:')
        frameId = Label(frame, text='Frame id:')

        self.name = Entry(frame)
        self.name.insert(0, 'Hokuyo_Node')
        self.output = Entry(frame)
        self.output.insert(0, 'screen')
        self.port = Entry(frame)
        self.port.insert(0, '/dev/Hokuyo')
        self.frameId = Entry(frame)
        self.frameId.insert(0, 'Hokuyo_Frame')

        add = Button(frame, text='Add', command=self.add)
        cancel = Button(frame, text='Cancel', command=self.cancel)

        name.grid(sticky=W)
        output.grid(sticky=W)
        port.grid(sticky=W)
        frameId.grid(sticky=W)
        add.grid(sticky=W)

        self.name.grid(row=0, column=1, sticky=E)
        self.output.grid(row=1, column=1, sticky=E)
        self.port.grid(row=2, column=1, sticky=E)
        self.frameId.grid(row=3, column=1, sticky=E)
        cancel.grid(row=4, column=1, sticky=E)

        hypLink = Label(frame, text='See hokuyo default arguments', fg='blue', cursor='hand2')
        hypLink.bind('<Button-1>', self.hrfCallBack)
        hypLink.grid()

        frame.pack()
        return self.finish

    def hrfCallBack(self, event):
        webbrowser.open('http://wiki.ros.org/hokuyo_node')

    def getData(self):
        return self.text, self.element, self.data

    def __init__(self, parent, icon, names, place=-1):
        GUIWizard.__init__(self, icon)
        self.element = None
        self.text = None
        self.master = Toplevel()
        self.master.tk.call('wm', 'iconphoto', self.master._w, self.icon)
        self.finish = BooleanVar()
        self.parent = parent
        self.data = dict()
        self.master.protocol('WM_DELETE_WINDOW', self.close)
        self.names = names
        self.place = place

    def close(self):
        self.cancel()
        # showerror(title='Error', message='please use the cancel button to exit.')

    def add(self):
        if self.nameIsValid():
            self.data['elType'] = 'Hokuyo'
            self.data['name'] = self.name.get()
            self.data['output'] = self.output.get()
            self.data['port'] = self.port.get()
            self.data['frameId'] = self.frameId.get()
            self.element = SubElement(self.parent, 'node', {
                'pkg': 'hokuyo_node',
                'type': 'hokuyo_node',
                'name': self.name.get(),
                'output': self.output.get()
            })
            SubElement(self.element, 'param', {
                'name': 'port',
                'value': self.port.get()
            })
            SubElement(self.element, 'param', {
                'name': 'frame_id',
                'value': self.frameId.get()
            })
            self.text = self.name.get()
            self.finish.set(True)
            self.master.destroy()
        else:
            showerror(title='Error', message='Name is already taken.')

    def cancel(self):
        self.finish.set(False)
        self.master.destroy()