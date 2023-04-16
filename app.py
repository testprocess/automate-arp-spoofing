from scapy.all import Ether, ARP, srp, send
import argparse
import time
import os
import sys
import sys 
from PyQt5.QtCore import QCoreApplication, QObject, QRunnable, QThread, QThreadPool, pyqtSlot
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import arp

class Window(QMainWindow):
    def __init__(self):
        super().__init__() 

        self.promptLable = '== ARP SP == \n'

        self.setWindowTitle("ARP Spoofing by H2J")
        self.setGeometry(100, 100, 600, 400)

        self.target_label = QLabel(self)
        self.target_label.move(20, 50)
        self.target_label.setText('Target IP')
        self.targetLine = QLineEdit("192.168.0.62", self)
        self.targetLine.move(20,70)

        self.host_label = QLabel(self)
        self.host_label.move(20, 100)
        self.host_label.setText('Host IP')
        self.hostLine = QLineEdit("192.168.0.1", self)
        self.hostLine.move(20,120)

        self.label = ScrollLabel(self)
        self.label.setGeometry(140, 10, 450, 200)
        self.label.setText(self.promptLable)

        btn = QPushButton(text="Send ARP", parent=self)
        btn.move(20, 10)
        btn.clicked.connect(self.sendArp)

    def sendArp(self):
        targetInput = self.targetLine.text()
        hostInput = self.hostLine.text()

        self.arp = arp.SendARP(targetInput, hostInput)
        self.arp.start()
        self.arp.prompt.connect(self.receiveFromArp)
        #self.arp.exec()
        #sys.exit(app.exec_())

    @pyqtSlot(str)
    def receiveFromArp(self, message):
        print("f", message)
        self.promptLable += message + "\n"
        self.label.setText(self.promptLable)


class ScrollLabel(QScrollArea):
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)
        self.setWidgetResizable(True)
        content = QWidget(self)
        self.setWidget(content)
 
        lay = QVBoxLayout(content)
 
        self.label = QLabel(content)
 
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
 
        self.label.setWordWrap(True)
 
        lay.addWidget(self.label)

    def setText(self, text):
        # setting text to the label
        self.label.setText(text)
 

if __name__ == "__main__":

    app = QApplication(sys.argv)
    win = Window()
    win.show()
    app.exec_()


    