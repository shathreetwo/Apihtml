import requests

url = 'https://api.github.com/users/shathreetwo'
response = requests.get(url)
# 위 주소로 GET 요청 보냄.

if response.status_code == 200:
    data = response.json()
    # 응답 본문을 JSON 형식으로 파싱해 Python 딕셔너리로 변환
    print(data)
    print("이름:", data.get('name'))
    print("팔로워 수:", data.get('followers'))
else:
    print("에러:", response.status_code)

# 200이면 성공, 404는 페이지 없음 500은 서버 오류
