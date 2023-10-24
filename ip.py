import subprocess 
from PyQt5.QtCore import QCoreApplication, QObject, QRunnable, pyqtSignal, QThread
from multiprocessing import Process
import threading
import os
from re import findall

class ScanIPRange(QThread):
    prompt = pyqtSignal(str, bool)

    def __init__(self, gateway):
        super().__init__()
        self.gateway = gateway

    def chunk(self, list, n):
        return [list[i:i+n] for i in range(0, len(list), n)]

    def getIps(self):
        return [".".join(self.gateway.split(".")[:3] + [str(i)]) for i in range(2, 255)]
    
    def scanAll(self):
        ips = self.getIps()
        chunkRange = 10
        ipChunk = self.chunk(ips, chunkRange)
        for ipList in ipChunk:
            for ips in ipList:
                x = threading.Thread(target=self.scan, args=(ips,), daemon=True)
                x.start()
                print(x.isDaemon())
                # self.scan(ips)

    def scan(self, ip):
        if ("nt" in os.name):
            res = subprocess.Popen(f"ping -n 3 {ip}", stdout=subprocess.PIPE)
            isInclude = len(findall("TTL", str(res.stdout.readlines()))) >= 1

            if isInclude: 
                self.prompt.emit(ip, True)
            else: 
                self.prompt.emit(ip, False)
        else:
            res = subprocess.call(['ping', '-c', '3', ip]) 
            
            if res == 0: 
                self.prompt.emit(ip, True)
            elif res == 2: 
                self.prompt.emit(ip, False)





    def run(self):
        self.scanAll()