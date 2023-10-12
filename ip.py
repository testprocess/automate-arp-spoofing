import subprocess 
from PyQt5.QtCore import QCoreApplication, QObject, QRunnable, pyqtSignal, QThread


class ScanIPRange(QThread):
    prompt = pyqtSignal(str, bool)

    def __init__(self, gateway):
        super().__init__()
        self.gateway = gateway


    def getIps(self):
        return [".".join(self.gateway.split(".")[:3] + [str(i)]) for i in range(2, 255)]

    def scan(self):
        ips = self.getIps()
        for ipItem in ips:
            res = subprocess.call(['ping', '-c', '3', ipItem]) 
            if res == 0: 
                print( "ping to", ipItem, "OK") 
                self.prompt.emit(ipItem, True)
            elif res == 2: 
                print("no response from", ipItem) 
                self.prompt.emit(ipItem, False)

            else: 
                print("ping to", ipItem, "failed!") 

    def run(self):
        self.scan()