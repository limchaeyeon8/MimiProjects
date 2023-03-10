# 주소록 GUI 프로그램 - MySQL 연동

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *   # QIcon
import pymysql

class qtApp(QMainWindow):
    conn = None
    curIdx = 0  # 현재 데이터 PK 담을 변수 생성

    def __init__(self):
        super().__init__()
        uic.loadUi('./stdPyQt/addressBook.ui', self)

        self.initDB()               # DB 초기화

        self.setWindowIcon(QIcon('./stdPyQt/addressBook.png'))           # QIcon

        self.setWindowTitle('주소록 v0.5')

        self.initDB()       # DB 초기화

        # 버튼 시그널 / 슬롯함수 지정
        self.btnNew.clicked.connect(self.btnNewClicked)
        self.btnSave.clicked.connect(self.btnSaveClicked)
        self.tblAddress.doubleClicked.connect(self.tblAddressDoubleClicked)
        self.btnDel.clicked.connect(self.btnDelClicked)


    # 데이터 삭제
    def btnDelClicked(self):
        if self.curIdx == 0:
            QMessageBox.warning(self, '경고', '삭제할 데이터를 선택하세요')
            return # 함수 빠져나감
        else:
            reply = QMessageBox.question(self, '확인', '정말로 삭제하시겠습니까?', QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.Yes)
            if reply == QMessageBox.No:
                return # 함수 빠져나감

            self.conn = pymysql.connect(host='localhost', user='root', password='12345',
                                    db='miniproject', charset='utf8')       # DB 수행할 때마다 접속해서 쿼리 실행 후 쿼리 끝나면 DB 닫기
            query = 'DELETE FROM addressbook WHERE Idx = %s'
            cur = self.conn.cursor()
            cur.execute(query, (self.curIdx))

            self.conn.commit()
            self.conn.close()

            QMessageBox.about(self, '성공', '데이터를 삭제했습니다')

            self.initDB()
            self.btnNewClicked()

    def btnNewClicked(self):                # 새연락처 버튼 누르면
        # 라인 에디팅 내용 삭제 후 이름에 포커스
        self.txtName.setText('')
        self.txtPhone.setText('')
        self.txtEmail.setText('')
        self.txtAddr.setText('')
        self.txtName.setFocus()
        self.curIdx = 0 # 0은 진짜 신규!
        print(self.curIdx)

    def tblAddressDoubleClicked(self):      # 
        rowIndex = self.tblAddress.currentRow()
        self.txtName.setText(self.tblAddress.item(rowIndex, 1).text())
        self.txtPhone.setText(self.tblAddress.item(rowIndex, 2).text())
        self.txtEmail.setText(self.tblAddress.item(rowIndex, 3).text())
        self.txtAddr.setText(self.tblAddress.item(rowIndex, 4).text())
        #print(rowIndex)
        self.curIdx = int(self.tblAddress.item(rowIndex, 0).text())
        print(self.curIdx)

    def btnSaveClicked(self):               # 저장 버튼
        fullName = self.txtName.text()
        phoneNum = self.txtPhone.text()
        email = self.txtEmail.text()
        address = self.txtAddr.text()

        #print(fullName, phoneNum, email, address)
        
    
        ## 이름과 전화번호를 입력하지 않으면 알람
        if fullName == '' or phoneNum == '':
            QMessageBox.warning(self, '주의', '이름과 핸드폰 번호를 입력하세요')
            return      # 진행불가
        else:
            self.conn = pymysql.connect(host='localhost', user='root', password='12345',
                                    db='miniproject', charset='utf8')       # DB 수행할 때마다 접속해서 쿼리 실행 후 쿼리 끝나면 DB 닫기
            
            if self.curIdx == 0:        # 신규
                # 네 개 변수값 받아서 INSERT 쿼리문 만들기
                query = '''INSERT INTO addressbook (FullName, PhoneNum, Email, Address)
                                VALUES (%s, %s, %s, %s)'''
            else:
                query = '''UPDATE addressbook
                              SET FullName = %s
                                , PhoneNum = %s
                                , Email = %s
                                , Address = %s
                            WHERE Idx = %s;'''      # UPDATE 쿼리문

            cur = self.conn.cursor()
            if self.curIdx == 0:
                cur.execute(query, (fullName, phoneNum, email, address))
            else:
                cur.execute(query, (fullName, phoneNum, email, address, self.curIdx))

            self.conn.commit()
            self.conn.close()

            # 저장성공 메시지
            if self.curIdx == 0:        # 신규
                QMessageBox.about(self, '성공', '저장 완료')
            else:
                QMessageBox.about(self, '성공', '수정 완료')

            # QTableWidget 새 데이터가 출력되도록
            self.initDB()
            # 입력창 내용 없어지게
            self.btnNewClicked()


    # DB 활용
    def initDB(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='12345',
                                    db='miniproject', charset='utf8')
        cur = self.conn.cursor()
        query = '''SELECT Idx
                        , FullName
                        , PhoneNum
                        , Email
                        , Address
                     FROM addressbook'''     # 멀티라인 문자열 편리!
        cur.execute(query)
        rows = cur.fetchall()

        #print(rows)
        self.makeTable(rows)
        self.conn.close()           # 프로그램 종료할 때

    def makeTable(self, rows):
        self.tblAddress.setColumnCount(5)           # 0. 열(컬럼)갯수
        self.tblAddress.setRowCount(len(rows))      # 0. 행갯수

        self.tblAddress.setHorizontalHeaderLabels(['번호', '이름', '전화번호', '이메일', '주소'])  # 1. 열 제목

        self.tblAddress.setSelectionMode(QAbstractItemView.SingleSelection)                        # 1.  단일 선택

        self.tblAddress.setColumnWidth(0, 0)      # idx                                            # 1. 번호는 숨김
        self.tblAddress.setColumnWidth(1, 85)     # fullName
        self.tblAddress.setColumnWidth(2, 125)    # phoneNum
        self.tblAddress.setColumnWidth(3, 220)    # email
        self.tblAddress.setColumnWidth(4, 134)    # address
        self.tblAddress.setEditTriggers(QAbstractItemView.NoEditTriggers)                          # 1. 컬럼 수정 금지

        for i, row in enumerate(rows):
            #print(row[1]~[4])
            idx = row[0]
            fullName = row[1]
            phoneNum = row[2]
            email = row[3]
            address = row[4]

            self.tblAddress.setItem(i, 0, QTableWidgetItem(str(idx)))           
            self.tblAddress.setItem(i, 1, QTableWidgetItem(fullName))           
            self.tblAddress.setItem(i, 2, QTableWidgetItem(phoneNum))           
            self.tblAddress.setItem(i, 3, QTableWidgetItem(email))           
            self.tblAddress.setItem(i, 4, QTableWidgetItem(address))           

        self.stbCurrent.showMessage(f'전체 주소록 : {len(rows)}개')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()                                                       #
    sys.exit(app.exec_())
