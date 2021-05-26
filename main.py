import os 
import sys
import PyQt5
import PyQt5.QtGui
import PyQt5.QtWidgets
import threading
import json 
import pusherConnect
import inputGUI
import icueConnect
import tray_rc



def startDaemonThread():
    thread_P = threading.Thread(target = pusherConnect.pusherConnect)
    thread_P.setDaemon(True)
    thread_P.start()

def checkJsonFile():
    if not os.path.exists("./data.json"):
        global pusherCreds 
        ex = inputGUI.inputGUI()
        ex.show()
        if ex.exec_() == inputGUI.inputGUI.Accepted:
            pusherCreds = ex.pCred
            data = {"pusherAppID":pusherCreds[0],"pusherKey":pusherCreds[1],"pusherSecret":pusherCreds[2],"pusherCluster":pusherCreds[3]}
            with open('data.json', 'w') as outfile:
                json.dump(data, outfile)
            
def colorResetCall():
    conn = icueConnect.icueConnect()
    conn.setPriority(0)
    del conn

def main():
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    checkJsonFile()
    startDaemonThread()
    # Adding an icon
    icon = PyQt5.QtGui.QIcon(":icon.png")
    # Adding item on the menu bar
    tray = PyQt5.QtWidgets.QSystemTrayIcon(icon, parent=app)
    tray.setVisible(True)
    # Creating the options
    menu = PyQt5.QtWidgets.QMenu()
    # To reset color 
    colorReset = PyQt5.QtWidgets.QAction("Revert Control")
    colorReset.triggered.connect(colorResetCall)
    menu.addAction(colorReset)
    # To quit the app
    quit = PyQt5.QtWidgets.QAction("Quit")
    quit.triggered.connect(app.quit)
    menu.addAction(quit)
    # Adding options to the System Tray
    tray.setContextMenu(menu)
    sys.exit(app.exec_())

if __name__=="__main__":
    main()
