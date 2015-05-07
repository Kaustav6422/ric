import rospkg

__author__ = 'tom1231'

from BAL.DevicesRows.HokuyoWizard import HokuyoWizard
from BAL.DevicesRows.OpenniWizard import OpenniWizard
from tkMessageBox import showerror
from BAL.Interface.GUIWizard import GUIWizard
from xml.etree import ElementTree
from lxml.etree import Element, SubElement, XML
from xml.dom import minidom
from Tkinter import *
from BAL.DevicesRows.CamWizard import CamWizard
from os.path import dirname, basename, splitext
from idlelib.ToolTip import ToolTip


class LaunchWizard(GUIWizard):
    @staticmethod
    def displayData(data):
        return 'None'

    def editWizard(self, data):
        return None

    def createWizard(self, itemAvailable=None):
        frame = Frame(self.master)
        self.nsField = Entry(frame, width=30)
        self.nsField.bind('<FocusOut>', self.hint)
        self.nsField.bind('<Button-1>', self.clear)
        self.nsField.insert(END, 'Launch Name space')
        self.nsField.pack(side=LEFT)
        frame.grid(row=2, sticky=W)

    def hint(self, event):
        if self.nsField.get() == '':
            self.nsField.insert(END, 'Launch Name space')

    def clear(self, event):
        if self.nsField.get() == 'Launch Name space':
            self.nsField.delete(0, END)

    def save(self, absPath, fileData):
        path = dirname(absPath)
        name = basename(absPath)
        if self.nsField.get() == 'Launch Name space':
            self.nsField.delete(0, END)
            self.nsField.insert(0, '/')
        self.group.set('ns', self.nsField.get())
        param = SubElement(self.group, 'rosparam', {
            'file': '$(find ric_board)/config/'
                    + name
            ,
            'command': 'load'
        })
        if path != '':
            pathPkd = rospkg.RosPack().get_path('ric_board')
            # print p ,splitext(name)[0]
            file = open('%s/launch/%s.launch' % (pathPkd, splitext(name)[0]), 'w')
        else:
            file = open(splitext(name)[0] + '.launch', 'w')
        file.write(prettify(self.root))
        fileData.write(prettify(self.root))
        file.close()
        self.group.remove(param)


    def delete(self):
        try:
            index, = self.list.curselection()
            self.list.delete(index)
            element = self.dataElement[index]
            elementAtri = self.atriData[index]
            self.atriData.remove(elementAtri)
            element.getparent().remove(element)
            self.dataElement.remove(element)
            self.names.remove(self.names[index])
        except:
            pass

    def getData(self):
        return self.dataElement

    def menu(self, menu):
        sub = Menu(menu, tearoff=0)

        sub.add_command(label='Add Camera', command=self.addCam)
        sub.add_command(label='Add Openni', command=self.addOp)
        sub.add_command(label='Add Hokuyo', command=self.addHo)

        menu.insert_cascade(3, label='Add External Device', menu=sub)

    def addCam(self):
        cam = CamWizard(self.group, self.icon, self.names)
        finish = cam.createWizard()
        self.master.wait_variable(finish)
        if finish.get():
            name, element, elAtri = cam.getData()
            self.list.insert(END, name)
            self.dataElement.append(element)
            self.atriData.append(elAtri)
            self.names.append(name)

    def addOp(self):
        element = OpenniWizard(self.group, self.icon)
        finish = element.createWizard()
        self.master.wait_variable(finish)
        if finish.get():
            name, element, elData = element.getData()

            self.list.insert(END, name)
            self.dataElement.append(element)
            self.atriData.append(elData)
            self.names.append(name)

    def addHo(self):
        element = HokuyoWizard(self.group, self.icon, self.names)
        finish = element.createWizard()
        self.master.wait_variable(finish)
        if finish.get():
            name, data, elAtriData = element.getData()
            self.list.insert(END, name)
            self.dataElement.append(data)
            self.atriData.append(elAtriData)
            self.names.append(name)

    def __init__(self, root, menu, edit, delete, info, icon):
        GUIWizard.__init__(self, icon)
        self.editB = edit
        self.deleteB = delete
        self.info = info
        self.root = Element('launch')
        self.group = SubElement(self.root, 'group', {'ns': ''})
        self.addSerialNode()
        self.master = Frame(root)
        self._isLoaded = False
        self.list = Listbox(self.master, selectmode=SINGLE, width=30)
        self.list.bind('<Double-Button-1>', self.clickEvent)
        # test = Button(self.master, text='test', command=self.printTest)
        title = Label(self.master, text='List of launch elements')
        title.grid(sticky=W)
        self.list.grid(sticky=W)
        # test.grid(row=1, column=1)
        self.dataElement = []
        self.atriData = []
        self.names = []
        self.menu(menu)
        self.master.grid(row=2, column=1)

    def printTest(self):
        print prettify(self.root)

    def addSerialNode(self):
        at = {
            'pkg': 'ric_board',
            'type': 'Start.py',
            'name': 'RiCTraffic',
            'output': 'screen'
        }
        element = SubElement(self.group, 'node', at)

    def deleteAll(self):
        # print self.atriData
        while len(self.atriData) > 0:
            self.atriData.pop()
        while len(self.dataElement) > 0:
            self.dataElement.pop()
        while len(self.names) > 0:
            self.names.pop()

    def isLoaded(self):
        return self._isLoaded

    def load(self, xml):
        self.list.delete(0, END)
        if len(self.dataElement) > 0:
            self.deleteAll()

        self.root = XML(xml)
        self.group = self.root.getchildren()[0]
        self.nsField.delete(0, END)
        self.nsField.insert(END, self.group.get('ns'))
        self.group.getchildren()[-1].getparent().remove(self.group.getchildren()[-1])
        elements = self.group.getchildren()
        for i in range(1, len(elements)):
            element = elements[i]
            arri = dict()
            if element.tag == 'include':
                name = element.getchildren()[0].get('name')
                self.list.insert(END, name)
                arri['elType'] = 'Openni'
                arri['value'] = element.getchildren()[0].get('value')
            else:
                name = element.get('name')
                self.list.insert(END, name)
                if element.get('type') == 'usb_cam_node':
                    children = element.getchildren()
                    arri['elType'] = 'Camera'
                    arri['name'] = element.get('name')
                    arri['output'] = element.get('output')
                    arri['respawn'] = element.get('respawn')
                    arri['videoDevice'] = children[0].get('value')
                    arri['cameraFrameId'] = children[1].get('value')
                    arri['pixelFormat'] = children[2].get('value')
                    arri['imageWidth'] = children[3].get('value')
                    arri['imageHeight'] = children[4].get('value')
                elif element.get('type') == 'hokuyo_node':
                    children = element.getchildren()
                    arri['elType'] = 'Hokuyo'
                    arri['name'] = element.get('name')
                    arri['output'] = element.get('output')
                    arri['port'] = children[0].get('value')
                    arri['frameId'] = children[1].get('value')

            self.atriData.append(arri)
            self.dataElement.append(element)
            self.names.append(name)

    def clickEvent(self, event):
        try:
            index, = self.list.curselection()
            self.editB.config(command=self.editElement)
            self.deleteB.config(command=self.delete)
            self.showElement(self.atriData[index])
        except:
            pass

    def showElement(self, data):
        info = ''
        self.info.config(state=NORMAL)
        self.info.delete(1.0, END)
        if data['elType'] == 'Openni':
            info = OpenniWizard.displayData(data)
        elif data['elType'] == 'Camera':
            info = CamWizard.displayData(data)
        elif data['elType'] == 'Hokuyo':
            info = HokuyoWizard.displayData(data)

        self.info.insert(END, info)
        self.info.config(state=DISABLED)

    def editElement(self):
        try:
            index, = self.list.curselection()
            data = self.atriData[index]
            exDev = None
            if data['elType'] == 'Openni':
                exDev = OpenniWizard(self.group, self.icon)
            elif data['elType'] == 'Camera':
                exDev = CamWizard(self.group, self.icon, self.names, index)
            elif data['elType'] == 'Hokuyo':
                exDev = HokuyoWizard(self.group, self.icon, self.names, index)

            finish = exDev.editWizard(data)
            self.master.wait_variable(finish)
            if finish.get():
                deleteEl = self.dataElement[index]
                deleteEl.getparent().remove(deleteEl)
                name, elementData, elAttriData = exDev.getData()
                self.list.delete(index)
                self.list.insert(index, name)
                self.dataElement[index] = elementData
                self.atriData[index] = elAttriData
                self.names[index] = name
                self.showElement(elAttriData)


        except:
            pass


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")
