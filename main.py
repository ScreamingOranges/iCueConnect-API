from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
import threading
from pusherConnect import pusherConnect
  

def connectionStarter():
    print("HI")

app = QApplication([])
app.setQuitOnLastWindowClosed(False)

# Adding an icon
icon = QIcon("icon.png")

# Adding item on the menu bar
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)

# Creating the options
menu = QMenu()
connectTriger = QAction("Connect")
connectTriger.triggered.connect(connectionStarter)
menu.addAction(connectTriger)

# To quit the app
quit = QAction("Quit")
quit.triggered.connect(app.quit)
menu.addAction(quit)

# Adding options to the System Tray
tray.setContextMenu(menu)
app.exec_()