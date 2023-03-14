# Thread
# 기본프로세스 하나, 서브스레드 다섯개 동시에 진행

import threading
import time     # 필수

class BackgroundWorker(threading.Thread):       # Thread를 상속받은 백그라운드 작업 클래스
    def __init__(self, names) -> None:                 # 생성자 생성
        super().__init__()
        self._name = f'{threading.current_thread().name} : {names}'      # 현재스레드, 이름 가져옴

    def run(self) -> None:
        print(f'BackgroundWorker start : {self._name}')
        time.sleep(3)
        print(f'BackgroundWorker end : {self._name}')

if __name__ == '__main__':
    print('MAIN THREAD START')          # 기본 프로세스 == 메인 스레드

    for i in range(5):
        name = f'서브 스레드 {i}'
        th = BackgroundWorker(name)
        th.start()                  # run() 실행됨

    print('MAIN THREAD END')