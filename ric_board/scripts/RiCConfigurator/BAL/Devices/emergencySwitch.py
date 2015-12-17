from PyQt4.QtGui import *
from BAL.Interface.DeviceFrame import DeviceFrame, EMERGENCY_SWITCH


class EmergencySwitch(DeviceFrame):
    def __init__(self, frame, data):
        DeviceFrame.__init__(self, EMERGENCY_SWITCH, frame, data)
        self._pin_to_listen = '27'
        self._state = '1'

    def showDetails(self, items=None):
        self.pin_to_listen = QLineEdit(self._pin_to_listen)
        self.state = QComboBox()
        self.state.addItem("Normally open", '1')
        self.state.addItem("Normally close", '2')

        self._frame.layout().addRow(QLabel('Pin to listen: '), self.pin_to_listen)
        self._frame.layout().addRow(QLabel('Mode: '), self.state)


    def getName(self):
        return 'emergency_switch'

    def saveToFile(self, file):
        file.write('emergency_switch/pin: {0}\n'.format(self._pin_to_listen))
        file.write('emergency_switch/state: {0}\n'.format(self._state))

    def printDetails(self):
        self._frame.layout().addRow(QLabel('Pin to listen: '), QLabel(self._pin_to_listen))

        mode = 'Normally '
        if self._state == '1':
            mode += 'open'
        else:
            mode += 'close'

        self._frame.layout().addRow(QLabel('Mode: '), QLabel(mode))

    def fromDict(self, data):
        self._pin_to_listen = data['pinToListen']
        self._state = data['state']

    def toDict(self):
        data = dict()

        data['type'] = EMERGENCY_SWITCH
        data['name'] = self.getName()
        data['pinToListen'] = self._pin_to_listen
        data['state'] = self._state

        return data

    def add(self):
        if not self.nameIsValid():
            QMessageBox.critical(self._frame, "Error", "You can only have one emergency switch")
            self._isValid = False
            return
        self._pin_to_listen = str(self.pin_to_listen.text())
        self._state = str(self.state.itemData(self.state.currentIndex()).toString())
        self._isValid = True
