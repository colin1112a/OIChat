"""
What's new?

Chinese:

English:

"""

# @formatter:on

import socket
import qdarkstyle
import time
import os
from threading import Thread
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

running = False
flag = True
ip = "127.0.0.1"  # 默认连接 IP
port = 10000  # 默认连接端口
username = ""
version = "2.3.1"  # 版本号
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    from winotify import Notification
    HAS_WINOTIFY = True
except ImportError:
    HAS_WINOTIFY = False


class RecvSignal(QtCore.QObject):
    """用于跨线程安全更新 UI 的信号"""
    message = QtCore.pyqtSignal(str)
    password_mode = QtCore.pyqtSignal()
    depassword_mode = QtCore.pyqtSignal()
    force_close = QtCore.pyqtSignal()


class GUI(object):   # 主窗口
    def __init__(self, Form, version):
        self.version = version
        self.Form = Form
        self.setupUi(Form)
        self.textEdit.setReadOnly(True)
        self.pushButton.clicked.connect(self.click)
        self.pushButton_2.clicked.connect(self.code_Click)
        self.pushButton_3.clicked.connect(self.fileclick)
        Form.setWindowIcon(QtGui.QIcon("./client.ico"))
        self.textEdit.setFontFamily("Consolas")
    def force_Close(self):
        self.Form.close()
        try:
            code_Ui.force_Close()
        except:
            pass
        try:
            file_Ui.force_Close()
        except:
            pass
    def code_Click(self):
        global code_Ui
        codeewindow = QtWidgets.QWidget()
        code_Ui = codewindow(codeewindow, self.version)
    def click(self):
        self.depassword_Mode()
        data = self.lineEdit.text()
        try:
            client_socket.send(data.encode("utf-8"))
        except:
            pass
        self.lineEdit.setText("")
    def password_Mode(self):
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
    def depassword_Mode(self):
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
    def send(self, data):
        self.textEdit.append(data)
        self.textEdit.moveCursor(QtGui.QTextCursor.End)
        self.textEdit.ensureCursorVisible()
    def fileclick(self):
        global file_Ui
        fileewindow = QtWidgets.QWidget()
        file_Ui = filewindow(fileewindow, self.version)
    def on_return_pressed(self):
        self.click()
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(506, 405)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 131, 31))
        self.label.setObjectName("label")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(10, 50, 481, 291))
        self.textEdit.setObjectName("textEdit")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(10, 350, 361, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(390, 350, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(400, 10, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(300, 10, 93, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.lineEdit.returnPressed.connect(self.on_return_pressed)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "OIChat " + self.version))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:14pt;\">OIChat</span></p></body></html>"))
        self.pushButton.setText(_translate("Form", "发送"))
        self.pushButton_2.setText(_translate("Form", "代码模式"))
        self.pushButton_3.setText(_translate("Form", "发送文件"))
        self.lineEdit.setFocus()


class codewindow(object): # 发送代码窗口
    def __init__(self, Form, version):
        self.version = version
        self.Form = Form
        super().__init__()
        self.setupUi(Form)
        self.pushButton.clicked.connect(self.click)
        Form.setWindowIcon(QtGui.QIcon("./client.ico"))
        self.Form.show()
    def force_Close(self):
        self.Form.close()
    def click(self):
        data = self.TextEdit.toPlainText()
        data = "发送了代码：" + "\n" + data + "\n"
        try:
            client_socket.send(data.encode("utf-8"))
        except:
            pass
        self.TextEdit.setText("")
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(483, 434)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 81, 21))
        self.label.setObjectName("label")
        self.TextEdit = QtWidgets.QTextEdit(Form)
        self.TextEdit.setGeometry(QtCore.QRect(10, 50, 461, 371))
        self.TextEdit.setObjectName("TextEdit")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(380, 10, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "OIChat " + self.version))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:14pt;\">OIChat</span></p></body></html>"))
        self.pushButton.setText(_translate("Form", "发送"))


class filewindow(object):
    def __init__(self,  Form, version):
        self.version = version
        self.Form = Form
        self.setupUi(Form)
        self.pushButton.clicked.connect(self.get_path)
        self.pushButton_2.clicked.connect(self.click)
        Form.setWindowIcon(QtGui.QIcon("./client.ico"))
        self.Form.show()
    def get_path(self):
        file_Name, file_Type = QtWidgets.QFileDialog.getOpenFileName(None, "请选择文件路径", "", "All files (*.*)")
        self.lineEdit.setText(file_Name)
    def force_Close(self):
        self.Form.close()
    def click(self):
        global ui
        data = self.lineEdit.text()
        if data == "":
            return
        try:
            f = open(data, "rb")
            ui.send("正在发送文件...")
            senddata = "!!!file " + os.path.basename(data)
            client_socket.send(senddata.encode("utf-8"))
            client_socket.sendall(f.read())
            time.sleep(5)
            client_socket.send(b"!!!endfile")
            f.close()
        except:
            ui.send("发送文件失败！")
        finally:
            self.lineEdit.setText("")
            self.Form.close()
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(483, 156)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 81, 21))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(80, 50, 281, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 69, 31))
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(370, 50, 93, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(190, 100, 93, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "OIChat " + self.version))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:14pt;\">OIChat</span></p></body></html>"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:14pt;\">路径:</span></p></body></html>"))
        self.pushButton.setText(_translate("Form", "选择"))
        self.pushButton_2.setText(_translate("Form", "发送"))


class namewindow(object):
    def click(self):
        global username
        text = self.lineEdit.text()
        if len(text) >= 4:
            username = text
            self.window.accept()
    def on_return_pressed(self):
        self.click()
    def setupUi(self, Form, version):
        self.version = version
        self.window = Form
        Form.setObjectName("Form")
        Form.resize(295, 116)
        Form.setWindowIcon(QtGui.QIcon("./client.ico"))
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 0, 161, 21))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(122, 40, 151, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 100, 21))
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(100, 70, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.click)
        self.lineEdit.returnPressed.connect(self.on_return_pressed)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        reg = QtCore.QRegExp("[a-zA-Z0-9]+$")
        regVal = QtGui.QRegExpValidator()
        regVal.setRegExp(reg)
        self.lineEdit.setValidator(regVal)
        self.lineEdit.setMaxLength(16)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "OIChat " + self.version))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:14pt;\">OIChat</span></p></body></html>"))
        self.lineEdit.setToolTip(_translate("Form", "<html><head/><body><p>用户名</p></body></html>"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:11pt;\">输入用户名：</span></p></body></html>"))
        self.pushButton.setText(_translate("Form", "确定"))


class ipportwindow(object):
    def click(self):
        global ip
        global port
        ip = self.lineEdit.text()
        port = int(self.lineEdit_2.text())
        self.window.accept()
    def on_return_pressed(self):
        self.click()
    def setupUi(self, Form, version):
        self.version = version
        self.window = Form
        Form.setObjectName("Form")
        Form.resize(295, 185)
        Form.setWindowIcon(QtGui.QIcon("./client.ico"))
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 0, 161, 21))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(160, 60, 113, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 150, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(10, 100, 171, 21))
        self.label_3.setObjectName("label_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(160, 100, 113, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(90, 135, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.click)
        self.lineEdit.returnPressed.connect(self.on_return_pressed)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "OIChat " + self.version))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:14pt;\">OIChat</span></p></body></html>"))
        self.lineEdit.setToolTip(_translate("Form", "<html><head/><body><p>服务器 IP</p></body></html>"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:11pt;\">输入服务器 IP :</span></p></body></html>"))
        self.label_3.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:11pt;\">输入服务器端口:</span></p></body></html>"))
        self.lineEdit_2.setToolTip(_translate("Form", "<html><head/><body><p>服务器端口</p></body></html>"))
        self.pushButton.setText(_translate("Form", "确定"))


def recv_thread():
    """接收消息的线程函数，通过信号安全更新 UI"""
    global client_socket, flag, running
    server_Return_Head = client_socket.recv(102400).decode("utf-8")
    client_socket.send((username + " " + version).encode("utf-8"))
    time.sleep(1)
    recv_signal.message.emit("GitHub 仓库地址：https://github.com/yuhaodi22222/OIChat")
    while running:
        try:
            data = client_socket.recv(102400).decode("utf-8")
            if not data:
                break
            if data[0:3] == "!!!":
                tmp = data[3:].split(" ")
                le = len(tmp)
                if tmp[0] == "warning":
                    recv_signal.message.emit(data[11:])
                    continue
                if tmp[0] == "password":
                    recv_signal.message.emit("请在下方输入框输入密码")
                    recv_signal.password_mode.emit()
                    continue
                if tmp[0] == "important":
                    From_User = tmp[1]
                    message_len = 14 + len(From_User)
                    messages = data[message_len:]
                    recv_signal.message.emit("用户 " + From_User + " 发送了重要消息：" + messages)
                    if HAS_WINOTIFY:
                        toast = Notification(app_id="OIChat", title="重要消息", msg="来自 " + From_User + ": " + messages)
                        toast.show()
                    continue
                if tmp[0] == "force_Close":
                    recv_signal.message.emit("管理员强制关闭了所有客户端")
                    time.sleep(0.5)
                    client_socket.close()
                    recv_signal.force_close.emit()
                    return
                if tmp[0] == "file":
                    filename = tmp[1]
                    if not os.path.exists("download"):
                        os.makedirs("download")
                    filename = os.path.basename(filename)
                    try:
                        fileaddr = os.path.join("download", filename)
                        filesss = open(fileaddr, "wb")
                        while True:
                            filesssdata = client_socket.recv(100)
                            if filesssdata == b"!!!endfile":
                                break
                            filesss.write(filesssdata)
                        filesss.close()
                    except:
                        print("文件接收出错")
                    continue
                if le == 1:
                    if tmp[0] == "kick":
                        recv_signal.message.emit("你被管理员踢出了服务器")
                        flag = False
                        continue
                    if tmp[0] == "ban":
                        recv_signal.message.emit("你被管理员封禁了")
                        flag = False
                        continue
            recv_signal.message.emit(data)
        except:
            while running:
                recv_signal.message.emit("连接断开，正在重连...")
                try:
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.connect((ip, port))
                    # 重连时正确处理协议握手
                    client_socket.recv(102400)
                    client_socket.send((username + " " + version).encode("utf-8"))
                    recv_signal.message.emit("重连成功！")
                    break
                except:
                    time.sleep(3)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    # 1. IP/端口输入对话框
    dialog1 = QtWidgets.QDialog()
    ipport = ipportwindow()
    ipport.setupUi(dialog1, version)
    if dialog1.exec_() != QtWidgets.QDialog.Accepted:
        sys.exit(0)

    # 2. 连接服务器
    ipad = (ip, port)
    try:
        client_socket.connect(ipad)
    except Exception as e:
        QtWidgets.QMessageBox.critical(None, "连接失败", f"无法连接到 {ip}:{port}\n{e}")
        sys.exit(1)

    running = True

    # 3. 用户名输入对话框
    dialog2 = QtWidgets.QDialog()
    name = namewindow()
    name.setupUi(dialog2, version)
    if dialog2.exec_() != QtWidgets.QDialog.Accepted:
        client_socket.close()
        sys.exit(0)

    # 4. 创建信号对象
    recv_signal = RecvSignal()

    # 5. 主窗口（在主线程创建）
    guimainwindow = QtWidgets.QWidget()
    ui = GUI(guimainwindow, version)

    # 6. 连接信号到 UI 槽函数
    recv_signal.message.connect(ui.send)
    recv_signal.password_mode.connect(ui.password_Mode)
    recv_signal.depassword_mode.connect(ui.depassword_Mode)
    recv_signal.force_close.connect(ui.force_Close)

    # 7. 启动接收线程
    t = Thread(target=recv_thread, daemon=True)
    t.start()

    guimainwindow.show()
    app.exec_()

    running = False
    try:
        client_socket.close()
    except:
        pass
    sys.exit(0)
