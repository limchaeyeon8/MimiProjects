# QR code PyQt App

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *   # QIcon
from PyQt5.QtCore import * # Qt.White...
import qrcode

# QR code 커스터마이징(이미지용) 클래스
class qtApp(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('./stdPython/qrcodeApp.ui', self)
        self.setWindowIcon(QIcon('./stdPython/qr-code.png'))           # QIcon
        self.setWindowTitle('QR 생성앱 v0.1')

        # 시그널/슬롯 함수 생성
        self.btnQrGen.clicked.connect(self.btnQrGenClicked)
        self.txtQrData.returnPressed.connect(self.btnQrGenClicked)

    def btnQrGenClicked(self):
        data = self.txtQrData.text()

        if data == '':
            QMessageBox.warning(self, '경고', '데이터를 입력하세요')
            return
        else:
            qr_image = qrcode.make(data)
            qr_image.save('./stdPython/site.png')

            img = QPixmap('./stdPython/site.png')
            self.lblQrCode.setPixmap(QPixmap(img).scaledToWidth(300))


    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()                                                       #
    sys.exit(app.exec_())
