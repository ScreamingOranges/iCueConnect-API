import os 
import sys
import PyQt5
import PyQt5.QtGui
import PyQt5.QtWidgets
import threading
import json 
import pusherConnect
import helperGUI
import icueConnect
import tray_rc
import pusher
import jsonpickle


def startDaemonThread():
    thread_P = threading.Thread(target = pusherConnect.pusherConnect)
    thread_P.setDaemon(True)
    thread_P.start()

def checkJsonFile():
    credCheck = True
    if not os.path.exists("./data.json"):
        global pusherCreds 
        ex = helperGUI.inputGUI()
        ex.show()
        if ex.exec_() == helperGUI.inputGUI.Accepted:
            pusherCreds = ex.pCred
            data = {"pusherAppID":pusherCreds[0],"pusherKey":pusherCreds[1],"pusherSecret":pusherCreds[2],"pusherCluster":pusherCreds[3]}
            with open('data.json', 'w') as outfile:
                json.dump(data, outfile)
    else:
        if os.path.exists("./data.json"):
            with open('data.json', 'r') as openfile:
                json_object = json.load(openfile)
            pusherCreds = json_object["pusherAppID"], json_object["pusherKey"], json_object["pusherSecret"], json_object["pusherCluster"]
    try:
        pusher_client = pusher.Pusher(app_id=pusherCreds[0], key=pusherCreds[1], secret=pusherCreds[2], cluster=pusherCreds[3])
    except ValueError as err:
        helperGUI.popUpNotice("Pusher Connection Failed. Check Your Credentials.", "Critical")
        credCheck = False
    return credCheck

def pusherCredentials():
    global pusherCreds
    if os.path.exists("./data.json"):
        with open('data.json', 'r') as openfile:
            json_object = json.load(openfile)
        pusherCreds = json_object["pusherAppID"], json_object["pusherKey"], json_object["pusherSecret"], json_object["pusherCluster"]
    ex = helperGUI.inputGUI(pusherCreds)
    ex.show()
    if ex.exec_() == helperGUI.inputGUI.Accepted:
        pusherCreds = ex.pCred
        data = {"pusherAppID":pusherCreds[0],"pusherKey":pusherCreds[1],"pusherSecret":pusherCreds[2],"pusherCluster":pusherCreds[3]}
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)

def colorResetCall():
    conn = icueConnect.icueConnect()
    conn.releaseControl()
    del conn

def iCueSDK_TestCall():
    if os.path.exists("./data.json"):
        with open('data.json', 'r') as openfile:
            json_object = json.load(openfile)
            pusherID = json_object["pusherAppID"]
            pusherKey = json_object["pusherKey"]
            pusherSecret = json_object["pusherSecret"]
            pusherCluster = json_object["pusherCluster"]
    try:
        pusher_client = pusher.Pusher(app_id=pusherID, key=pusherKey, secret=pusherSecret, cluster=pusherCluster)
        pusher_client.trigger(u'api_Callback', u'test_event', jsonpickle.encode("The iCue Connect API Is Communicating Properly With Your Device!"))
    except ValueError as err:
        helperGUI.popUpNotice("Pusher Connection Failed. Check Your Credentials.", "Critical")
    conn = icueConnect.icueConnect()
    conn.requestControl()
    conn.perform_pulse_effect(300, [255, 255, 255])
    conn.solidColor([0, 0, 0])
    conn.delayedSolidColor(.01, [255, 0, 0])
    conn.perform_pulse_effect(300, [255, 255, 255])
    conn.solidColor([0, 0, 0])
    conn.releaseControl()
    del conn


def main():
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    if checkJsonFile():
        startDaemonThread()
    else:
        pusherCredentials()
        sys.exit("Pusher Connection Failed. Checking Your Updated Credentials On Next Start.")
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
    # To test iCue SDK 
    iCueSDK_Test = PyQt5.QtWidgets.QAction("Test")
    iCueSDK_Test.triggered.connect(iCueSDK_TestCall)
    menu.addAction(iCueSDK_Test)
    # To change Pusher Creds
    pusher_credentials = PyQt5.QtWidgets.QAction("Pusher Credentials")
    pusher_credentials.triggered.connect(pusherCredentials)
    menu.addAction(pusher_credentials)
    # To quit the app
    quit = PyQt5.QtWidgets.QAction("Quit")
    quit.triggered.connect(app.quit)
    menu.addAction(quit)
    # Adding options to the System Tray
    tray.setContextMenu(menu)
    sys.exit(app.exec_())

if __name__=="__main__":
    main()
