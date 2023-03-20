# 전국 대학교 리스트
# pandas - 빅데이터 분석할 때 데이터 가져오 데 사용하는 모듈
# pip install pandas

import pandas as pd

filePath = './stdPython/university_List_2020.xlsx'
df_excel = pd.read_excel(filePath, engine='openpyxl')

df_excel.columns = df_excel.loc[4].tolist()         # 여기부터 사용
df_excel = df_excel.drop(index=list(range(0, 5)))   # 0~5번 항목까지만 리스트   # 실제 데이터 이외 행을 날려버림


print(df_excel.head())      # 상위 5개만 출력

print(df_excel['학교명'].values)        # 학교명인 것만
print(df_excel['주소'].values)        # 주소인 것만
