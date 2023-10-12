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
import socket
import netifaces

import arp
import ip

class Window(QMainWindow):
    def __init__(self):
        super().__init__() 


        gateways = netifaces.gateways()

        self.GATEWAY_IP = gateways['default'][netifaces.AF_INET][0]

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
        self.hostLine = QLineEdit(self.GATEWAY_IP, self)
        self.hostLine.move(20,120)

        self.label = ScrollLabel(self)
        self.label.setGeometry(300, 50, 450, 200)
        self.label.setText(self.promptLable)

        self.iplist = QListWidget(self)
        self.iplist.resize(150, 200)
        self.iplist.move(140, 50)


        btn = QPushButton(text="Send ARP", parent=self)
        btn.move(20, 10)
        btn.clicked.connect(self.sendArp)


        btnIp = QPushButton(text="Scan IP", parent=self)
        btnIp.move(120, 10)
        btnIp.clicked.connect(self.scanIp)


    def scanIp(self):
        self.ipscan = ip.ScanIPRange(self.GATEWAY_IP)
        self.ipArray = self.ipscan.getIps()
        self.ipArrayItem = []

        for ipItem in self.ipArray:
            item = QListWidgetItem(ipItem)
            item.setBackground( QColor('#ffffff') )
            self.ipArrayItem.append(item)
            self.iplist.addItem(item)
        
        self.ipscan.start()
        self.ipscan.prompt.connect(self.receiveActiveIp)



    def sendArp(self):
        targetInput = self.targetLine.text()
        hostInput = self.hostLine.text()
        self.arp = arp.SendARP(targetInput, hostInput)
        self.arp.start()
        self.arp.prompt.connect(self.receiveFromArp)


    def changeColorIpItem(self, ip, color):
        index = self.ipArray.index(ip)
        self.ipArrayItem[index].setBackground( QColor(color) )


    @pyqtSlot(str, bool)
    def receiveActiveIp(self, ipName, isActive):
        
        # ipName = parameter[0]
        # isActive = parameter[1]
        print("f", ip)
        color = '#7fc97f'  if isActive == True else "#f26363"
        self.changeColorIpItem(ipName, color)


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
        self.label.setText(text)
 

if __name__ == "__main__":

    app = QApplication(sys.argv)
    win = Window()
    win.show()
    app.exec_()


    