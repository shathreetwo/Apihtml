import requests

url = 'https://jsonplaceholder.typicode.com/posts'
response = requests.get(url)

if response.status_code == 200:
    posts = response.json()
    #print(posts)
    for post in posts[:5]:
        # posts 리스트 중 앞에서 5개 
        print(f"{post['id']}번 글 제목: {post['title']}")
        # f-string 문법 
