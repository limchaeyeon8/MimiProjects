import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *   # QIcon
from PyQt5.QtCore import *  # Qt.White...
import time

class BackgroundWorker(QThread):        # PyQt5 스레드를 위한 클래스 존재
    procChanged = pyqtSignal(int)       # 시그널



    def __init__(self, count=0, parent=None) -> None:
        super().__init__()
        self.main = parent
        self.working = True     # 스레드 동작 여부
        self.count = count

    def run(self):
        # self.parent.pgbTask.setRange(0, 100)
        # for i in range(0, 101):
        #     print(f'스레드 출력 > {i}')
        #     self.parent.pgbTask.setValue(i)
        #     self.parent.txtLog.append(f'스레드 출력 > {i}')
        while self.working:
            self.procChanged.emit(self.count)         # emit() - 값(시그널)을 보내주는 것
            self.count += 1             # 값 증가만


class qtApp(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('./stdThread/threadApp.ui', self)
        #self.setWindowIcon(QIcon('./stdPython/info.png'))
        self.setWindowTitle('NO THREAD APP v0.4')
        self.pgbTask.setValue(0)

        self.btnStart.clicked.connect(self.btnStartClicked)
        # 쓰레드 초기화
        self.worker = BackgroundWorker(parent=self, couunt=0)
        # 백그라운드 워커에 있는 시그널을 접근하는 슬롯함수
        self.worker.procChanged.connect(self.procUpdated)

        self.pgbTask.setRange(0, 1000000)

    @pyqtSlot(int)              # 데코  # 파라미터는 int
    def procUpdated(self, count):
        self.txtLog.append(f'스레드 출력 > {count}')
        self.pgbTask.setValue(count)

    @pyqtSlot()
    def btnStartClicked(self):
        self.worker.start()
        self.worker.working = True



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())