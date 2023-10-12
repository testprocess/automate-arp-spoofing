import subprocess 
from PyQt5.QtCore import QThread


class ScanIPRange(QThread):
    def __init__(self, gateway):
        super().__init__()
        self.gateway = gateway


    def getPorts(self):
        return [".".join(self.gateway.split(".")[:3] + [str(i)]) for i in range(2, 255)]

    def scan(self):
        ports = self.getPorts()
        for port in ports:
            res = subprocess.call(['ping', '-c', '3', port]) 
            if res == 0: 
                print( "ping to", port, "OK") 
            elif res == 2: 
                print("no response from", port) 
            else: 
                print("ping to", port, "failed!") 

    def run(self):
        self.scan()