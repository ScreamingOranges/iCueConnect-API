import sys
import PyQt5
import PyQt5.QtWidgets

class inputGUI(PyQt5.QtWidgets.QDialog):
    def __init__(self, parent = None):
        super(inputGUI, self).__init__(parent)
        layout = PyQt5.QtWidgets.QFormLayout()

        self.btnAppID = PyQt5.QtWidgets.QPushButton("Enter app_id")
        self.btnAppID.clicked.connect(self.getAppID)
        self.leAppID = PyQt5.QtWidgets.QLabel()
        layout.addRow(self.btnAppID,self.leAppID)

        self.btnKey = PyQt5.QtWidgets.QPushButton("Enter key")
        self.btnKey.clicked.connect(self.getKey)
        self.leKey = PyQt5.QtWidgets.QLabel()
        layout.addRow(self.btnKey,self.leKey)

        self.btnSecret = PyQt5.QtWidgets.QPushButton("Enter secret")
        self.btnSecret.clicked.connect(self.getSecret)
        self.leSecret = PyQt5.QtWidgets.QLabel()
        layout.addRow(self.btnSecret,self.leSecret)
        
        self.btnCluster = PyQt5.QtWidgets.QPushButton("Choose cluster")
        self.btnCluster.clicked.connect(self.chooseCluster)
        self.leCluster = PyQt5.QtWidgets.QLabel()
        layout.addRow(self.btnCluster,self.leCluster)
        
        self.btnAccept = PyQt5.QtWidgets.QPushButton("Submit")
        self.btnAccept.clicked.connect(self.on_clicked)
        layout.addRow(self.btnAccept)

        self.setLayout(layout)
        self.setFixedWidth(250)
        self.setWindowTitle("iCueConnect")

    def getAppID(self):
        app_id, ok = PyQt5.QtWidgets.QInputDialog.getText(self, "iCueConnect", "Enter Pusher app_id:")
        if ok:
            self.leAppID.setText(str(app_id))

    def getKey(self):
        key,ok = PyQt5.QtWidgets.QInputDialog.getText(self,"iCueConnect","Enter Pusher key:")
        if ok:
            self.leKey.setText(str(key))
    
    def getSecret(self):
        secret,ok = PyQt5.QtWidgets.QInputDialog.getText(self,"iCueConnect","Enter Pusher secret:")
        if ok:
            self.leSecret.setText(str(secret))
    
    def chooseCluster(self):
        clusters = ("mt1", "us2", "us3", "eu", "ap1", "ap2", "ap3", "ap4")
        cluster, ok = PyQt5.QtWidgets.QInputDialog.getItem(self, "iCueConnect",  "Select Pusher cluster", clusters, 0, False)
        if ok and cluster:
            self.leCluster.setText(cluster)
    
    @PyQt5.QtCore.pyqtSlot()
    def on_clicked(self):        
        self.pCred = self.leAppID.text(), self.leKey.text(), self.leSecret.text(), self.leCluster.text()
        self.accept()
    


"""
#OLD EXAMPLE CALL
app = PyQt5.QtWidgets.QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)
pusherKey = inputGUI().getText()



#NEW EXAMPLE CALL
def main(): 
    global pusherCreds 
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    ex = inputGUI()
    ex.show()
    if ex.exec_() == inputGUI.Accepted:
        pusherCreds = ex.pCred
    
    print(pusherCreds)

if __name__ == '__main__':
    main()
#for json
#data = {"pusherAppID":pusherCreds[0],"pusherKey":pusherCreds[1],"pusherSecret":pusherCreds[2],"pusherCluster":pusherCreds[3]}
""" 
