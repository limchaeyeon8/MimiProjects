# Qt Designer 디자인 사용

import sys
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *

class qtApp(QWidget):

    count = 0                                                # 클릭횟수 카운트 변수

    def __init__(self):
        super().__init__()
        uic.loadUi('./stdPyQt/mainApp.ui', self)             #


        # Qt Designer에서 구성한 위젯시그널 만듦
        self.btnOK.clicked.connect(self.btnOKClicked)
        self.btnPOP.clicked.connect(self.btnPOPClicked)

    def btnPOPClicked(self):
        QMessageBox.about(self, 'popup', '+까꿍+')

    def btnOKClicked(self):                                  # 슬롯함수
        self.count += 1
        self.lblMessage.clear()
        self.lblMessage.setText(f'당근을 흔들어주세요\n당근!!!!!!! + {self.count}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()                                                #
    sys.exit(app.exec_())
