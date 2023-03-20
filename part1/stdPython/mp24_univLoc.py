# 전국대학 위치

import pandas as pd
import folium

filePath = './stdPython/university_locations.xlsx'
df_exel = pd.read_excel(filePath, engine='openpyxl', header=None)

df_exel.columns = ['학교명', '주소', 'lng', 'lat']      # 헤더부여

#print(df_exel)

name_list = df_exel['학교명'].to_list()
addr_list = df_exel['주소'].to_list()
lng_list = df_exel['lng'].to_list()
lat_list = df_exel['lat'].to_list()

fMap = folium.Map(location=[37.553175, 126.989326], zoom_start=10)

for i in range(len(name_list)):         # 446번 반복
    if lng_list[i] != 0:                # 위경도값이 0이 아니면
        marker = folium.Marker([lat_list[i], lng_list[i]], popup=name_list[i], 
                               icon=folium.Icon(color='blue'))
        marker.add_to(fMap)

fMap.save('./stdPython/Korea_univs.html')
