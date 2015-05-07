from tkMessageBox import showerror

__author__ = 'tom1231'

from BAL.Interface.GUIWizard import GUIWizard
from Tkinter import *
from lxml.etree import Element, SubElement
import webbrowser

class CamWizard(GUIWizard):
    @staticmethod
    def displayData(data):
        info = 'Element Type: ' + data['elType'] + '\n'
        info += 'Output: ' + data['output'] + '\n'
        info += 'Respawn: ' + data['respawn'] + '\n'
        info += 'Video device: ' + data['videoDevice'] + '\n'
        info += 'Camera frame id: ' + data['cameraFrameId'] + '\n'
        info += 'Pixel format: ' + data['pixelFormat'] + '\n'
        info += 'Image width: ' + data['imageWidth'] + '\n'
        info += 'Image height: ' + data['imageHeight'] + '\n'
        return info

    def editWizard(self, data):
        frame = Frame(self.master)
        name = Label(frame, text='name:')
        output = Label(frame, text='output:')
        respawn = Label(frame, text='respawn:')
        videoDevice = Label(frame, text='video device:')
        cameraFrameId = Label(frame, text='Camera frame id:')
        pixelFormat = Label(frame, text='Pixel format:')
        imageWidth = Label(frame, text='image Width:')
        imageHeight = Label(frame, text='Image height:')

        self.name = Entry(frame)
        self.name.insert(END, data['name'])
        self.output = Entry(frame)
        self.output.insert(END, data['output'])
        self.respawn = Entry(frame)
        self.respawn.insert(END, data['respawn'])
        self.videoDevice = Entry(frame)
        self.videoDevice.insert(END, data['videoDevice'])
        self.cameraFrameId = Entry(frame)
        self.cameraFrameId.insert(END, data['cameraFrameId'])
        self.pixelFormat = Entry(frame)
        self.pixelFormat.insert(END, data['pixelFormat'])
        self.imageWidth = Entry(frame)
        self.imageWidth.insert(END, data['imageWidth'])
        self.imageHeight = Entry(frame)
        self.imageHeight.insert(END, data['imageHeight'])

        name.grid(sticky=W)
        output.grid(sticky=W)
        respawn.grid(sticky=W)
        videoDevice.grid(sticky=W)
        cameraFrameId.grid(sticky=W)
        pixelFormat.grid(sticky=W)
        imageWidth.grid(sticky=W)
        imageHeight.grid(sticky=W)

        self.name.grid(row=0, column=1, sticky=E)
        self.output.grid(row=1, column=1, sticky=E)
        self.respawn.grid(row=2, column=1, sticky=E)
        self.videoDevice.grid(row=3, column=1, sticky=E)
        self.cameraFrameId.grid(row=4, column=1, sticky=E)
        self.pixelFormat.grid(row=5, column=1, sticky=E)
        self.imageWidth.grid(row=6, column=1, sticky=E)
        self.imageHeight.grid(row=7, column=1, sticky=E)

        add = Button(frame, text='Add', command=self.add)
        cancel = Button(frame, text='Cancel', command=self.cancel)

        add.grid(sticky=W)
        cancel.grid(row=8, column=1, sticky=E)

        hypLink = Label(frame, text='See usb camera default arguments', fg='blue', cursor='hand2')
        hypLink.bind('<Button-1>', self.hrfCallBack)
        hypLink.grid()

        frame.pack()
        return self.finish

    def createWizard(self, itemAvailable = None):
        frame = Frame(self.master)
        name = Label(frame, text='name:')
        output = Label(frame, text='output:')
        respawn = Label(frame, text='respawn:')
        videoDevice = Label(frame, text='video device:')
        cameraFrameId = Label(frame, text='Camera frame id:')
        pixelFormat = Label(frame, text='Pixel format:')
        imageWidth = Label(frame, text='image Width:')
        imageHeight = Label(frame, text='Image height:')

        self.name = Entry(frame)
        self.name.insert(0, 'Cam')
        self.output = Entry(frame)
        self.output.insert(0, 'screen')
        self.respawn = Entry(frame)
        self.respawn.insert(0, 'true')
        self.videoDevice = Entry(frame)
        self.videoDevice.insert(0, '/dev/video0')
        self.cameraFrameId = Entry(frame)
        self.cameraFrameId.insert(0, 'head_camera')
        self.pixelFormat = Entry(frame)
        self.pixelFormat.insert(0, 'mjpeg')
        self.imageWidth = Entry(frame)
        self.imageWidth.insert(0, '640')
        self.imageHeight = Entry(frame)
        self.imageHeight.insert(0, '480')

        name.grid(sticky=W)
        output.grid(sticky=W)
        respawn.grid(sticky=W)
        videoDevice.grid(sticky=W)
        cameraFrameId.grid(sticky=W)
        pixelFormat.grid(sticky=W)
        imageWidth.grid(sticky=W)
        imageHeight.grid(sticky=W)

        self.name.grid(row=0, column=1, sticky=E)
        self.output.grid(row=1, column=1, sticky=E)
        self.respawn.grid(row=2, column=1, sticky=E)
        self.videoDevice.grid(row=3, column=1, sticky=E)
        self.cameraFrameId.grid(row=4, column=1, sticky=E)
        self.pixelFormat.grid(row=5, column=1, sticky=E)
        self.imageWidth.grid(row=6, column=1, sticky=E)
        self.imageHeight.grid(row=7, column=1, sticky=E)

        add = Button(frame, text='Add', command=self.add)
        cancel = Button(frame, text='Cancel', command=self.cancel)

        add.grid(sticky=W)
        cancel.grid(row=8, column=1, sticky=E)
        hypLink = Label(frame, text='See usb camera default arguments', fg='blue', cursor='hand2')
        hypLink.bind('<Button-1>', self.hrfCallBack)
        hypLink.grid()

        frame.pack()
        return self.finish

    def hrfCallBack(self, event):
        webbrowser.open(r'http://wiki.ros.org/usb_cam')

    def add(self):
        if self.nameIsValid():
            self.data['elType'] = 'Camera'
            self.data['output'] = self.output.get()
            self.data['respawn'] = self.respawn.get()
            self.data['videoDevice'] = self.videoDevice.get()
            self.data['cameraFrameId'] = self.cameraFrameId.get()
            self.data['pixelFormat'] = self.pixelFormat.get()
            self.data['imageWidth'] = self.imageWidth.get()
            self.data['imageHeight'] = self.imageHeight.get()
            self.data['name'] = self.name.get()
            nodeAt = {
                'pkg': 'usb_cam',
                'name': self.name.get(),
                'output': self.output.get(),
                'respawn': self.respawn.get(),
                'type': 'usb_cam_node'
            }
            self.element = SubElement(self.parent, 'node', nodeAt)
            SubElement(self.element, 'param', {
                'name': 'video_device',
                'value': self.videoDevice.get()
            })
            SubElement(self.element, 'param', {
                'name': 'camera_frame_id',
                'value': self.cameraFrameId.get()
            })
            SubElement(self.element, 'param', {
                'name': 'pixel_format',
                'value': self.pixelFormat.get()
            })
            SubElement(self.element, 'param', {
                'name': 'image_width',
                'value': self.imageWidth.get()
            })
            SubElement(self.element, 'param', {
                'name': 'image_height',
                'value': self.imageHeight.get()
            })
            self.text = self.name.get()
            self.master.destroy()
            self.finish.set(True)
        else:
            showerror(title='Error', message='Name is already taken.')

    def cancel(self):
        self.master.destroy()
        self.finish.set(False)

    def getData(self):
        return self.text, self.element, self.data

    def nameIsValid(self):
        for i in xrange(len(self.names)):
            if self.name.get() == self.names[i] and i != self.place:
                return False
        return True

    def __init__(self, parent, icon, names, place=-1):
        GUIWizard.__init__(self, icon)
        self.master = Toplevel()
        self.master.tk.call('wm', 'iconphoto', self.master._w, self.icon)
        self.finish = BooleanVar()
        self.element = None
        self.text = None
        self.parent = parent
        self.names = names
        self.place = place
        self.master.protocol('WM_DELETE_WINDOW', self.close)
        self.data = dict()

    def close(self):
        self.cancel()
        # showerror(title='Error', message='please use the cancel button to exit.')
