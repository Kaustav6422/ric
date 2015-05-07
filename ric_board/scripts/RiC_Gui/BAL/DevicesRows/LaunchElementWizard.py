from tkMessageBox import showerror

__author__ = 'tom1231'
from BAL.Interface.GUIWizard import GUIWizard
from Tkinter import *
from lxml.etree import Element, SubElement

class LaunchElementWizard(GUIWizard):
    def editWizard(self, data):
        return GUIWizard.editWizard(self, data)

    def createWizard(self, itemAvailable = None):
        tag = Label(self.frame, text='Tag name:')
        self.tagField = Entry(self.frame)
        
        tag.grid(sticky=W)
        self.tagField.grid(row=0, column=1, sticky=E)
        
        
        self.frame.pack()
        return self.finish

    def getData(self):
        return self.name, self.element

    def addAtri(self):
        name = Label(self.frame, text='Name:')
        nameField = Entry(self.frame)
        val = Label(self.frame, text='Value:')
        valText = Entry(self.frame)

        self.data.append((nameField, valText))

        name.grid(row=self.rowCount, column=0, sticky=W)
        nameField.grid(row=self.rowCount, column=1, sticky=E)
        self.rowCount += 1
        val.grid(row=self.rowCount, column=0, sticky=W)
        valText.grid(row=self.rowCount, column=1, sticky=E)
        self.rowCount += 1

    def __init__(self, parent, icon):
        GUIWizard.__init__(self, icon)
        self.master = Toplevel()
        self.frame = Frame(self.master)
        self.finish = BooleanVar()
        self.parent = parent
        self.element = None
        self.rowCount = 1
        self.data = []
        self.master.protocol('WM_DELETE_WINDOW', self.close)
        self.addMenu()

    def close(self):
        self.cancel()
        # showerror(title='Error', message='please use the cancel button to exit.')

    def addMenu(self):
        menu = Menu(self.frame)
        menu.add_command(label='Done', command=self.done)
        menu.add_command(label='Add attribute', command=self.addAtri)
        menu.add_command(label='Cancel', command=self.cancel)
        self.master.config(menu=menu)

    def cancel(self):
        self.master.destroy()
        self.finish.set(False)

    def done(self):
        attributes = dict()
        for att in self.data:
            name, val = att
            attributes[name.get()] = val.get()
        self.element = SubElement(self.parent, self.tagField.get(), attributes)
        self.name = self.tagField.get()
        self.master.destroy()
        self.finish.set(True)