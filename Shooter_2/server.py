import _thread, socket
from settings import *

HOST = '192.168.1.188'   # Standard loopback interface address (localhost)
PORT = 65432

conns = {}

players = {}
bullets = {}
grenades = {}

id = 1

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_server_window(object):
    def setupUi(self, server_window):
        server_window.setObjectName("server_window")
        server_window.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(server_window)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(21)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(80, 70, 331, 451))
        self.textBrowser.setObjectName("textBrowser")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(180, 20, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(580, 30, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(480, 70, 256, 481))
        self.listWidget.setObjectName("listWidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(80, 530, 331, 20))
        self.lineEdit.setObjectName("lineEdit")
        server_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(server_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        server_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(server_window)
        self.statusbar.setObjectName("statusbar")
        server_window.setStatusBar(self.statusbar)

        self.retranslateUi(server_window)
        QtCore.QMetaObject.connectSlotsByName(server_window)

        self.lineEdit.returnPressed.connect(self.command)

    def retranslateUi(self, server_window):
        _translate = QtCore.QCoreApplication.translate
        server_window.setWindowTitle(_translate("server_window", "MainWindow"))
        self.label.setText(_translate("server_window", "Server"))
        self.label_2.setText(_translate("server_window", "Output"))
        self.label_3.setText(_translate("server_window", "Users"))

    def command(self):
        text = self.lineEdit.text()
        self.lineEdit.clear()

        text = text.split(" ")

        if text[0] == "dc":
            remove_user(int(text[1]))

    def update_output(self, data):
        self.textBrowser.append(data)

    def remove_user(self):
        self.listWidget.clear()
        for id in players:
            self.update_user(id)

    def update_user(self, id):
        self.listWidget.addItem(str(id))

def remove_user(id):
    del conns[id]
    del players[id]
    del bullets[id]
    del grenades[id]
    ui.remove_user()

def check(id):
    rect = PLAYER_HIT_BOX.copy()
    rect.x = players[id]["pos"]["x"]
    rect.y = players[id]["pos"]["y"]

    try:
        for ids in bullets:
            for bullet in bullets[ids]:
                if rect.x + rect.width > bullet["pos"]["x"] > rect.x and rect.y + rect.height > bullet["pos"]["y"] > rect.y:
                    print("yay")

    except:
        pass

def update():
    while True:
        try:
            for id in players:
                #check(id)
                pass
        except:
            pass

def new_client(conn, addr, id):
    # print("Connection started with:", addr)
    msg = "Connection started with:" + str(addr) + " id: " + str(id)
    ui.update_output(msg)
    while True:
        try:
            if id not in conns:
                conn.sendall(b"dc")
                msg = "Connection ended with:" + str(addr) + " id: " + str(id)
                ui.update_output(msg)
                break

            data = conn.recv(262144).decode()

            data = eval(data)

            players[id] = data["player"]
            bullets[id] = data["bullets"]
            grenades[id] = data["grenades"]

        except:
            msg = "Connection ended with:" + str(addr) + " id: " + str(id)
            ui.update_output(msg)
            remove_user(id)
            break


        temp = dict(players)
        tempB = dict(bullets)
        tempG = dict(grenades)

        del temp[id]
        del tempB[id]
        del tempG[id]

        d = {"players": temp, "bullets": tempB, "grenades": tempG}

        conn.sendall(str(d).encode())

        '''
        msg = "Connection ended with:" + str(addr) + " id: " + str(id)
        ui.update_output(msg)
        remove_user(id)
        break
        '''
def socket_func():
    global id
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(3)

        # _thread.start_new_thread(start_main, ())
        while True:
            conn, addr = s.accept()

            conns[id] = conn

            ui.update_user(id)
            _thread.start_new_thread(new_client, (conn, addr, id))

            id += 1

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    server_window = QtWidgets.QMainWindow()
    ui = Ui_server_window()
    _thread.start_new_thread(socket_func, ())
    _thread.start_new_thread(update, ())
    ui.setupUi(server_window)
    server_window.show()
    sys.exit(app.exec_())
