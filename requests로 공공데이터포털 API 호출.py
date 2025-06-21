import ssl
import requests
from urllib3.poolmanager import PoolManager
from requests.adapters import HTTPAdapter
from datetime import datetime

# 오늘 날짜를 "YYYY-MM-DD" 형식으로 생성
today = datetime.today().strftime("%Y-%m-%d")
print(today)

class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')  # 보안 수준 낮추기. 이거 없으면 ssl에러
        kwargs['ssl_context'] = ctx
        super().init_poolmanager(*args, **kwargs)

session = requests.Session()
session.mount('https://', TLSAdapter())

url = "https://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMinuDustFrcstDspth"
params = {
    "serviceKey": "ntHgt3rvR5X6/ZFHKiy4d1WOMFQ0bCAVYqFJTyKDGdkk1F+O11u7RFA0EVx/gLVHa8tnOjlILYfmWVR69IvNJw==",
    "returnType": "json",
    "numOfRows": 10,
    "pageNo": 1,
    "searchDate": today,
    "InformCode": "PM10"
}



res = session.get(url, params=params)
#print(res.status_code)
#print(res.text)

if res.status_code == 200:
    try:
        data = res.json()
        print("대기질 예보통보 조회")
        seen_dates = set()
        for item in data['response']['body']['items']:
            date = item['informData']
            if date not in seen_dates:
                seen_dates.add(date)
                print(f"\n{date} | {item['informGrade']}")
    except Exception as e:
        print("JSON 파싱 실패:", e)
else:
    print("API 요청 실패:", res.status_code)


# HTML 파일 생성
html = """<!DOCTYPE html>
<html lang="ko">
<head><meta charset="UTF-8"><title>미세먼지 예보</title></head>
<body>
<h1>미세먼지 예보</h1>
"""

seen_dates = set()  # 새로 초기화

for item in data['response']['body']['items']:
    date = item['informData']
    if date not in seen_dates:
        seen_dates.add(date)
        html += f"<h2>{date}</h2>"
        html += f"<p>{item['informGrade']}</p>"
        html += f"<p>{item['informCause']}</p>"

html += "</body></html>"

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("\n✔ index.html 생성 완료")
