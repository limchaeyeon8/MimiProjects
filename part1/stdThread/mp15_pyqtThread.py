# 스레드 미사용앱

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *   # QIcon
from PyQt5.QtCore import *  # Qt.White...

class qtApp(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('./stdThread/threadApp.ui', self)
        #self.setWindowIcon(QIcon('./stdPython/info.png'))
        self.setWindowTitle('NO THREAD APP v0.4')
        self.pgbTask.setValue(0)

        self.btnStart.clicked.connect(self.btnStartClicked)

    def btnStartClicked(self):
        self.pgbTask.setRange(0, 9999999)
        for i in range(0, 1000000):
            print(f'노스레드 출력 > {i}')
            self.pgbTask.setValue(i)
            self.txtLog.append(f'노스레드 출력 > {i}')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())