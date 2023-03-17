import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *   # QIcon
from PyQt5.QtCore import *  # Qt.White...
import time

MAX = 10000     # 전체 클래스에 사용할 변수

class BackgroundWorker(QThread):        # PyQt5 스레드를 위한 클래스 존재
    procChanged = pyqtSignal(int)       # 커스텀 시그널; 마우스 같은 시그널을 사용자가 따로 만드는 것



    def __init__(self, count=0, parent=None) -> None:
        super().__init__()
        self.main = parent
        self.working = False     # 스레드 동작 여부 = False
        self.count = count

    def run(self):          # thread.start() --> run() // 대신실행
        # self.parent.pgbTask.setRange(0, 100)
        # for i in range(0, 101):
        #     print(f'스레드 출력 > {i}')
        #     self.parent.pgbTask.setValue(i)
        #     self.parent.txtLog.append(f'스레드 출력 > {i}')
        while self.working:
            if self.count <= MAX:
                self.procChanged.emit(self.count)         # emit() - 값(시그널)을 보내주는 것
                self.count += 1             # 값 증가만 // 업무프로세스 동작하는 위치
                time.sleep(0.001)           # 1ms // 스레드는 동시성 => 시간을 쪼개줘야 함(슬라이스) // 타임슬립을 써야
                                            # 0.0000001 처럼 타임슬립을 너무 세밀하게 주면 GUI 처리를 제대로 못함 
            else:
                self.working = False        # run() 멈춤



class qtApp(QMainWindow):                       # 위젯은 qtApp 클래스에서 제어

    def __init__(self):
        super().__init__()
        uic.loadUi('./stdThread/threadApp.ui', self)
        #self.setWindowIcon(QIcon('./stdPython/info.png'))
        self.setWindowTitle('THREAD APP v0.4')
        self.pgbTask.setValue(0)

        # 내장된 시그널↓
        self.btnStart.clicked.connect(self.btnStartClicked)
        # 쓰레드 생성↓
        self.worker = BackgroundWorker(parent=self, count=0)
        # 백그라운드 워커에 있는 시그널을 접근하는 슬롯함수
        self.worker.procChanged.connect(self.procUpdated)

        self.pgbTask.setRange(0, MAX)

    #@pyqtSlot(int)              # 데코레이션; 커스텀 시그널을 사용하는 슬롯함수임을 설명// 하지만 별로 의미 없음
    def procUpdated(self, count):
        self.txtLog.append(f'스레드 출력 > {count}')
        self.pgbTask.setValue(count)

    #@pyqtSlot()
    def btnStartClicked(self):
        self.worker.start()         # BackgroundWorker(스레드) 안에 있는 run() 실행
        self.worker.working = True  # 스레드 동작 여부 = True 
        self.worker.count = 0       # 


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())