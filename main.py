import sys
import PyQt5
import PyQt5.QtGui
import PyQt5.QtWidgets
import threading
import pusherConnect
import tray_rc 

thread_P = threading.Thread(target = pusherConnect.pusherConnect)
thread_P.setDaemon(True)
thread_P.start()

app = PyQt5.QtWidgets.QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)


# Adding an icon
icon = PyQt5.QtGui.QIcon(":icon.png")

# Adding item on the menu bar
tray = PyQt5.QtWidgets.QSystemTrayIcon(icon, parent=app)
tray.setVisible(True)

# Creating the options
menu = PyQt5.QtWidgets.QMenu()

# To quit the app
quit = PyQt5.QtWidgets.QAction("Quit")
quit.triggered.connect(app.quit)
menu.addAction(quit)

# Adding options to the System Tray
tray.setContextMenu(menu)

sys.exit(app.exec_())
