import sys
import PyQt5
import PyQt5.QtWidgets

class inputGUI(PyQt5.QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

    def getText(self):
        pusherKey, okPressed = PyQt5.QtWidgets.QInputDialog.getText(self, "iCueConnect","Enter Pusher Key:", PyQt5.QtWidgets.QLineEdit.Normal, "")
        if okPressed and pusherKey != '':
            return pusherKey
        sys.exit()

"""
#example call
app = PyQt5.QtWidgets.QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)
pusherKey = inputGUI().getText()
""" 