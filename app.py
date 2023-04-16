from scapy.all import Ether, ARP, srp, send
import argparse
import time
import os
import sys
import sys 
from PyQt5.QtCore import QCoreApplication, QObject, QRunnable, QThread, QThreadPool
from PyQt5.QtWidgets import * 
import arp

class Window(QMainWindow):
    def __init__(self):
        super().__init__() 

        self.setWindowTitle("ARP Spoofing by H2J")

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

        btn = QPushButton(text="Send ARP", parent=self)
        btn.move(10, 10)
        btn.clicked.connect(self.sendArp)

    def sendArp(self):
        targetInput = self.targetLine.text()
        hostInput = self.hostLine.text()

        self.arp = arp.SendARP(targetInput, hostInput)
        self.arp.start()
        #self.arp.exec()
        #sys.exit(app.exec_())






if __name__ == "__main__":

    app = QApplication(sys.argv)
    win = Window()
    win.show()
    app.exec_()


    