# 암호해제 앱

import itertools
import time
import zipfile

passwd_str = '0123456789'     # 패스워드에 영문자도 들어있으면
# passwd_str = '0123456789abcdefghijklmnopqrstuvwxyzABCD~~~XYZ' 대문자까지 다 들어있어야 함

file = zipfile.ZipFile('./stdPython/site.zip')
isFind = False          # 암호를 찾았는지 물어봄

for i in range (4, 5):
    attempts = itertools.product(passwd_str, repeat=i)

    for attempt in attempts:
        try_pass = ''.join(attempt)
        print(try_pass)
        time.sleep(0.01)

        try:            # 예외
            file.extractall(pwd = try_pass.encode(encoding='utf-8'))
            print(f'암호는 {try_pass} 입니다.')
            isFind = True; break

        except:
            pass

    if isFind == True: break