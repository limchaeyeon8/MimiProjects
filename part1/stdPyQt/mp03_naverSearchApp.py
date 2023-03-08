# Naver API 뉴스검색 앱

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *   # Icon
from NaverApi import *
import webbrowser # 웹브라우저 모듈

class qtApp(QWidget):

    def __init__(self):
        super().__init__()
        uic.loadUi('./stdPyQt/naverApiSearch.ui', self)             #

        self.setWindowIcon(QIcon('./stdPyQt/new.png'))              # Icon

        # 검색 버튼 클릭 '시그널'에 대한 '슬롯' 함수
        self.btnSearch.clicked.connect(self.btnSearchClicked)
        # 검색어 입력 후 '''엔터'''를 치면 처리
        self.txtSearch.returnPressed.connect(self.txtSearchReturned)
        # 더블클릭
        self.tblResult.doubleClicked.connect(self.tblResultDoubleClicked)

    def tblResultDoubleClicked(self):
        #row = self.tblResult.currentIndex().row()
        #column = self.tblResult.currentIndex().column()
        #print(row, column)
        selected = self.tblResult.currentRow()
        url = self.tblResult.item(selected, 1).text()
        #print(url)
        webbrowser.open(url)        # 뉴스기사 웹사이트 오픈

    def txtSearchReturned(self):
        self.btnSearchClicked()
        
    def btnSearchClicked(self):
        search = self.txtSearch.text()

        if search == '':
            QMessageBox.warning(self, '경고', '검색어를 입력하세요')
            return
        else:                       # 실제 검색 시작 // from NaverApi import *
            api = NaverApi()        #  NaverApi 클래스 객체 생성
            node = 'news'           # movie로 변경하면 영화검색
            outputs = []            # 결과 데이터를 담을 리스트변수
            display = 100

            result = api.get_naver_search(node, search, 1, display)
            #print(result)
            
            # 테이블위젯에 실제 출력
            items = result['items']     # json 결과 중 item 아래 배열만 추출
            #print(len(items))
            self.makeTable(items)       # 테이블위젯에 데이터들을 할당하는 함수

    # 테이블 위젯에 데이터 표시(디스플레이)
    def makeTable(self, items):
        self.tblResult.setSelectionMode(QAbstractItemView.SingleSelection)  # 단일선택
        self.tblResult.setColumnCount(2)
        self.tblResult.setRowCount(len(items))      # (현재)100개 행 생성
        self.tblResult.setHorizontalHeaderLabels(['기사제목', '뉴스링크'])
        self.tblResult.setColumnWidth(0, 305)
        self.tblResult.setColumnWidth(1, 240)
        # 컬럼 데이터 수정금지시킴
        self.tblResult.setEditTriggers(QAbstractItemView.NoEditTriggers)


        for i, post in enumerate(items):     # 0, 뉴스,,,,
            title = self.replaceHtmlTag(post['title'])      # HTML 특수문자 변환
            originallink = post['originallink']

            # setItem(행, 열, 넣을 데이터)
            self.tblResult.setItem(i, 0, QTableWidgetItem(title))            
            self.tblResult.setItem(i, 1, QTableWidgetItem(originallink))   

    # HTML 특수문자 변환
    def replaceHtmlTag(self, sentence) -> str:          # 나중에 str 리턴
        result = sentence.replace('&lt;', '<')          # lesser than 작다
        result = result.replace('&gt;', '>')            # greater than 크다
        result = result.replace('<b>', '')              # bold
        result = result.replace('</b>', '')
        result = result.replace('&apos', "'")           # apostropy 홑따옴표
        result = result.replace('&quot', '"')           # quotation mark 쌍따옴표
        # 변환 안 된 특수문자가 나타나면 여기 추가
        # result = result.replace('', '')        #

        return result
                    



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()                                                       #
    sys.exit(app.exec_())
