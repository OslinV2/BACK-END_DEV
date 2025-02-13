import requests
from bs4 import BeautifulSoup as bs4

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0'
}

chars = requests.get('https://rickandmortyapi.com/api/character', headers=headers, verify=False)
soup = bs4(chars.text, 'html.parser')
# O prettify  é um método específico de objetos bs4 e não pode ser utilizado diretamente em strings. A solução é garantir que você esteja utilizando BeautifulSoup para analisar o conteúdo da página HTML
print(soup.prettify())

# r = requests.get('https://api.github.com', auth=('user', 'pass'))

# print(r.text)
# print(r.headers['content-type'])


# r = requests.get('https://google.com/')
# print(r.text)
# print(r.status_code)

# from requests import Request
# url = Request(None, 'http://youtube.com/?', params={'Data1': 'data'}).prepare().url
# print(url)
