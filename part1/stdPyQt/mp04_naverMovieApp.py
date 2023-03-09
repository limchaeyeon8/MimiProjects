# Naver API 뉴스검색 앱

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *   # QIcon
from NaverApi import *
from urllib.request import urlopen
import webbrowser # 웹브라우저 모듈

class qtApp(QWidget):

    def __init__(self):
        super().__init__()
        uic.loadUi('./stdPyQt/naverApiMovie.ui', self)             #

        self.setWindowIcon(QIcon('./stdPyQt/movie.png'))           # QIcon

        # 검색 버튼 클릭 '시그널'에 대한 '슬롯' 함수
        self.btnSearch.clicked.connect(self.btnSearchClicked)
        # 검색어 입력 후 '''엔터'''를 치면 처리
        self.txtSearch.returnPressed.connect(self.txtSearchReturned)
        # 더블클릭
        self.tblResult.doubleClicked.connect(self.tblResultDoubleClicked)

    def tblResultDoubleClicked(self):
        selected = self.tblResult.currentRow()
        url = self.tblResult.item(selected, 5).text()           # url 링크 컬럼 변경
        webbrowser.open(url)        # 네이버 영화 웹사이트 오픈

    def txtSearchReturned(self):
        self.btnSearchClicked()
        
    def btnSearchClicked(self):
        search = self.txtSearch.text()

        if search == '':
            QMessageBox.warning(self, '경고', '영화명을 입력하세요')
            return
        else:                       # 실제 검색 시작 // from NaverApi import *
            api = NaverApi()        #  NaverApi 클래스 객체 생성
            node = 'movie'           # movie로 변경하면 영화검색
            display = 100

            result = api.get_naver_search(node, search, 1, display)
            print(result)
            
            # 테이블위젯에 실제 출력
            items = result['items']     # json 결과 중 item 아래 배열만 추출
            #print(len(items))
            self.makeTable(items)       # 테이블위젯에 데이터들을 할당하는 함수

    # 테이블 위젯에 데이터 표시(디스플레이) ---> 네이버 영화 결과에 맞게 변경
    def makeTable(self, items):
        self.tblResult.setSelectionMode(QAbstractItemView.SingleSelection)  # 단일선택
        self.tblResult.setColumnCount(7)            # 컬럼개수 증가
        self.tblResult.setRowCount(len(items))      # (현재)3개 행 생성
        self.tblResult.setHorizontalHeaderLabels(['영화제목', '개봉년도', '감독', '배우진', '평점', '영화링크', '포스터'])
        self.tblResult.setColumnWidth(0, 200)
        self.tblResult.setColumnWidth(1, 65)     # 개봉년도
        self.tblResult.setColumnWidth(2, 150)    # 감독
        self.tblResult.setColumnWidth(3, 250)    # 배우진
        self.tblResult.setColumnWidth(4, 50)     # 평점
        #self.tblResult.setColumnWidth(6, 200)   # 포스터

        # 컬럼 데이터 수정금지시킴
        self.tblResult.setEditTriggers(QAbstractItemView.NoEditTriggers)


        for i, post in enumerate(items):     # 0, 영화,,,,
            title = self.replaceHtmlTag(post['title'])      # HTML 특수문자 변환    /// 영어제목 가져오기 추가해야함
            subtitle = post['subtitle']
            title = f'{title} ({subtitle})'
            pubDate = post['pubDate']
            director = post['director'].replace('|', ', ')[:-1]
            actor = post['actor'].replace('|', ', ')[:-1]
            userRating = post['userRating']
            link = post['link']

            img_url = post['image']

            #print(img_url == '')
            
            if img_url != '':       # 빈값이면 포스터가 없는 것
                data = urlopen(img_url).read()  # 파이썬으로 2진 데이터를 만들어줌 
                                                # ㄴ네이버영화에 있는 이미지 다운, 이미지 데이터를 출력 // 아직 텍스트 형태의 데이터
                image = QImage()                # 이미지를 담을 수 있는 이미지 객체
                image.loadFromData(data)
                # QTableWidget 이미지를 그냥 넣을 수 없음/ QLabel()에 집어넣은 뒤 QLabel을 QTableWidget에 할당
                imgLabel = QLabel()
                imgLabel.setPixmap(QPixmap(image))  # 포스터 이미지화 완료

                # data를 이미지 파일로 저장
                # 테스트
                #f = open(f'./stdPyQt/temp/poster_{i+1}.png', mode='wb')  # 파일쓰기
                #f.write(data)
                #f.close()

            # setItem(행, 열, 넣을 데이터)
            self.tblResult.setItem(i, 0, QTableWidgetItem(title))   
            self.tblResult.setItem(i, 1, QTableWidgetItem(pubDate))            
            self.tblResult.setItem(i, 2, QTableWidgetItem(director))        
            self.tblResult.setItem(i, 3, QTableWidgetItem(actor))        
            self.tblResult.setItem(i, 4, QTableWidgetItem(userRating))        
            self.tblResult.setItem(i, 5, QTableWidgetItem(link))
            
            if img_url != '':
                self.tblResult.setCellWidget(i, 6, imgLabel)        # 포스터 이미지 처리-> 셀에 저장
                self.tblResult.setRowHeight(i, 110)     # 포스터 쉘 높이를 늘림
            else:
                self.tblResult.setItem(i, 6, QTableWidgetItem('No Poster')) # 일반 텍스트
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
