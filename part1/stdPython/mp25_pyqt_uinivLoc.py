# PyQt에 folium 지도 표시

import sys
import io   ### 파일 저장
import folium
import pandas as pd
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *   # QIcon
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView     # 설치 pip install PyQtWebEngine

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('./stdPython/map.png'))
        self.setWindowTitle('전국대학지도')
        self.width, self.height = 1200, 800
        self.setMinimumSize(self.width, self.height)

        layout = QVBoxLayout()
        self.setLayout(layout)

        filePath = './stdPython/university_locations.xlsx'
        df_exel = pd.read_excel(filePath, engine='openpyxl', header=None)

        df_exel.columns = ['학교명', '주소', 'lng', 'lat']      # 헤더부여

        #print(df_exel)

        name_list = df_exel['학교명'].to_list()
        addr_list = df_exel['주소'].to_list()
        lng_list = df_exel['lng'].to_list()
        lat_list = df_exel['lat'].to_list()

        #url = 'https://naver.com'
        m = folium.Map(location=[37.553175, 126.989326], zoom_start=10)

        for i in range(len(name_list)):         # 446번 반복
            if lng_list[i] != 0:                # 위경도값이 0이 아니면
                marker = folium.Marker([lat_list[i], lng_list[i]], popup=name_list[i], 
                                    icon=folium.Icon(color='blue'))
                marker.add_to(m)

        data = io.BytesIO()
        m.save(data, close_file=False)

        webView = QWebEngineView()
        #webView.load(QUrl(url))
        webView.setHtml(data.getvalue().decode())
        layout.addWidget(webView)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())