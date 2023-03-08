# NaverApi 클래스 - Open API ; 인터넷 통해서 데이터 전달 받음

from urllib.request import Request, urlopen     # urlopen- 함수
from urllib.parse import quote                  # 인코딩
import datetime                                 # 현재시간 사용
import json                                     # 결과는 json으로 리턴값 받음

class NaverApi:
    # 생성자 만들기
    def __init__(self) -> None:
        print(f'[{datetime.datetime.now()}] Naver API 생성')


    # Naver API를 요청하는 (((중요한))) 함수
    def get_request_url(self, url):
        req = Request(url)
        # Naver API 개인별 >>>인증<<<
        req.add_header('X-Naver-Client-Id', 'xdwitVyDcjsJd0Hrl8gR')     # 대소문자 구문해서 정확히 적어야 함
        req.add_header('X-Naver-Client-Secret', '_xA_9vE4Li')

        try:
            res = urlopen(req)          # 요청 결과가 바로 돌아옴
            if res.getcode() == 200:    # response OK
                print(f'[{datetime.datetime.now()}] >>>Url Request Succeed<<<\n')        # 네이버 API 요청 성공 // [] - 요청 성공 시간
                return res.read().decode('utf-8')        # 한글변환문제 => utf-8로 decode
            else:
                print(f'[{datetime.datetime.now()}] ---Url Request Failed---\n')
                return None
        except Exception as e:
            print(f'[{datetime.datetime.now()}] ---예외 발생 : {e}--\n')
            return None

    # >>>실제 호출함수<<<
    def get_naver_search(self, node, search, start, display):       # 4개의 변수
        base_url = 'https://openapi.naver.com/v1/search'
        node_url = f'/{node}.json'
        params = f'?query={quote(search)}&start={start}&display={display}' # search ---- 그냥쓰면 안 됨 // from urllib.parse import quote

        url = base_url + node_url + params                          # url 합치기
        retData = self.get_request_url(url)

        if retData == None:
            return None
        else:
            return json.loads(retData)                              # json으로 return // import json