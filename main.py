from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
import threading
import sys
from pusherConnect import pusherConnect

app = QApplication([])

thread_P = threading.Thread(target = pusherConnect)
thread_P.setDaemon(True)
thread_P.start()

app.setQuitOnLastWindowClosed(False)

# Adding an icon
icon = QIcon("icon.png")

# Adding item on the menu bar
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)

# Creating the options
menu = QMenu()

# To quit the app
quit = QAction("Quit")
quit.triggered.connect(app.quit)
menu.addAction(quit)

# Adding options to the System Tray
tray.setContextMenu(menu)
app.exec_()
