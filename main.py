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

class main:
    def __iCueSDK_TestCall(self):
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
    
    def __colorResetCall(self):
        conn = icueConnect.icueConnect()
        conn.releaseControl()
        del conn
    
    def __updatePusherCredentials(self):
        ex = helperGUI.inputGUI(self.pusherCreds)
        ex.show()
        if ex.exec_() == helperGUI.inputGUI.Accepted:
            self.pusherCreds = ex.pCred
            data = {"pusherAppID":self.pusherCreds[0],"pusherKey":self.pusherCreds[1],"pusherSecret":self.pusherCreds[2],"pusherCluster":self.pusherCreds[3]}
            with open('data.json', 'w') as outfile:
                json.dump(data, outfile)
    
    def __checkJsonFile(self):
        credCheck = True
        #If data.json doesnt exist
        if not os.path.exists("./data.json"):
            ex = helperGUI.inputGUI()
            ex.show()
            if ex.exec_() == helperGUI.inputGUI.Accepted:
                self.pusherCreds = ex.pCred
                data = {"pusherAppID":self.pusherCreds[0],"pusherKey":self.pusherCreds[1],"pusherSecret":self.pusherCreds[2],"pusherCluster":self.pusherCreds[3]}
                with open('data.json', 'w') as outfile:
                    json.dump(data, outfile)
        #If data.json does exist
        else:
            if os.path.exists("./data.json"):
                with open('data.json', 'r') as openfile:
                    json_object = json.load(openfile)
                self.pusherCreds = json_object["pusherAppID"], json_object["pusherKey"], json_object["pusherSecret"], json_object["pusherCluster"]
        #Test pusher connection with credentials
        try:
            pusher.Pusher(app_id=self.pusherCreds[0], key=self.pusherCreds[1], secret=self.pusherCreds[2], cluster=self.pusherCreds[3])
        except ValueError as err:
            helperGUI.popUpNotice("Pusher Connection Failed. Check Your Credentials.", "Critical")
            credCheck = False
        return credCheck
    
    def __init__(self):
        app = PyQt5.QtWidgets.QApplication(sys.argv)
        if self.__checkJsonFile():
            self.thread_P = threading.Thread(target = pusherConnect.pusherConnect)
            self.thread_P.setDaemon(True)
            self.thread_P.start()
        else:
            self.__updatePusherCredentials()
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
        colorReset.triggered.connect(self.__colorResetCall)
        menu.addAction(colorReset)
        # To test iCue SDK 
        iCueSDK_Test = PyQt5.QtWidgets.QAction("Test")
        iCueSDK_Test.triggered.connect(self.__iCueSDK_TestCall)
        menu.addAction(iCueSDK_Test)
        # To change Pusher Creds
        pusher_credentials = PyQt5.QtWidgets.QAction("Pusher Credentials")
        pusher_credentials.triggered.connect(self.__updatePusherCredentials)
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