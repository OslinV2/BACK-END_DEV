from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from mysql.connector import Error
from selenium import webdriver
import mysql.connector
import time as t

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0'
# }

# Pegaando o html inteiro e formatando-o
# html = driver.page_source
# soup = bs4(html, 'lxml')
# print(soup.prettify())

# Fazendo a requisição para a página do IMDb
# resposta = requests.get('https://www.imdb.com/chart/top/?ref_=nv_mv_250', headers=headers, verify=False)
# soup = bs4(resposta.text, 'lxml')
# titles = soup.find_all('h3', class_='ipc-title__text')
# for title in titles:
#     print(titles.text)

def web_scraping():
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors--')
    chrome_options.add_argument('--ignore_ssl_errors--')
    
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get('https://www.imdb.com/chart/top/?ref_=nv_mv_250')
        t.sleep(2)  
        
        nomes = driver.find_elements(By.XPATH, '//div[@class="ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-3713cfda-2 fSzZES cli-title with-margin"]')
        notas = driver.find_elements(By.XPATH, '//span[@class="ipc-rating-star--rating"]')
        
        filmes = []
        for nome, nota in zip(nomes, notas):
            try:
                filme_nome = nome.text.strip()
                filme_nota = float(nota.text.strip().replace(',', '.'))
                filmes.append((filme_nome, filme_nota))
            except ValueError:
                print(f'Erro ao converter nota; {nota.text}')
                
        return filmes
    finally:
        driver.quit()

def conectar_banco():
    try:
        conexao = mysql.connector.connect(
            host='127.0.0.1',
            database='ATIVIDADES',
            user='root',
            password='root'
        )
        if conexao.is_connected():
            print('Conexão com banco de dados no Mysql estabelecida com sucesso!!!')
            return conexao
    except Error as e:
        print(f"Erro na conexão ano banco no Mysql: {e}")    
    return None

def inserir_dados(filmes):
    conexao = conectar_banco()
    if conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute('DELETE FROM filmes')
            query = 'INSERT INTO filmes (nome, nota) VALUES (%s, %s)'
            for filme in filmes:
                cursor.execute(query, filme)
            conexao.commit()
            print('Dados inseridos com sucesso!!')
        except mysql.connector.Error as err:
            print('Nehum dado foi coletado.')
        finally:
            cursor.close()
            conexao.close()

    
filmes = web_scraping()
inserir_dados(filmes)