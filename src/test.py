import os
import time
import client
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.Qt import QThread
from PyQt5.QtCore import pyqtSignal

from ui_mainWinGui import Ui_MainWindow


class zhMain(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(zhMain, self).__init__()
        self.setupUi(self)
        self.thread_1 = ClientInit()
        self.thread_2 = TimeUpdate()

        # qt信号连接区
        self.genBtn.clicked.connect(self.on_generate)
        self.actBtn.clicked.connect(self.on_activate)
        self.startBtn.clicked.connect(self.on_start)
        self.thread_2.time_signal.connect(self.time_update)
        # 变量区

    def on_generate(self):
        self.genEdit.setText(client.CURRENT_MACHINE_ID)

    def on_activate(self):
        try:
            activate_code = self.actEdit.text()
            self.infoEdit.setText(client.register(activate_code))
        except Exception as e:
            return self.infoEdit.setText("invalid input")

    def on_start(self):
        self.thread_1.start()
        time.sleep(0.01)
        if client.STATE:
            self.thread_2.start()
        else:
            self.infoEdit.setText(client.client_init())

    def time_update(self, text):
        self.infoEdit.setText(text)

    # 退出按钮响应函数
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '退出程序', "确认退出程序？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            os._exit(0)  # 结束所有
        else:
            event.ignore()


class ClientInit(QThread):
    def __init__(self):
        super(ClientInit, self).__init__()

    def run(self):
        client.client_init()


class TimeUpdate(QThread):

    time_signal = pyqtSignal(str)

    def __init__(self):
        super(TimeUpdate, self).__init__()

    def run(self):
        while True:
            time_left = "剩余时间：" + str(client.dd) + "天" + str(client.hh) + "小时" + str(client.mm) + "分钟"
            self.time_signal.emit(time_left)
            time.sleep(60)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = zhMain()
    form.show()
    sys.exit(app.exec_())
