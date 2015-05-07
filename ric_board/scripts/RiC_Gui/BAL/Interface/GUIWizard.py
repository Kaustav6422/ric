__author__ = 'tom1231'


class GUIWizard:
    def __init__(self, icon):
        self.icon = icon

    def createWizard(self, itemAvailable):
        raise Exception('Error the function createRow must be override')

    def editWizard(self, data):
        raise Exception('Error the function editWizard must be override')

    def getData(self):
        raise Exception('Error the function getData must be override')

    @staticmethod
    def displayData(data): raise NotImplementedError


