import requests
from commonkit import CommonKit
from bs4 import BeautifulSoup as bs4
import urllib3

# Desativa o aviso de certificado SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0'
}

# Realiza a requisição com verify=False (não verifica o SSL)
response = requests.get('https://learn.microsoft.com/en-us/graph/sdks/create-client?from=snippets&tabs=python', headers=headers, verify=False)
soup = bs4(response.text, 'html.parser')
print(soup.prettify())

# Instancia o CommonKit
commonkit = CommonKit(client_id='3af3b781-a88c-467b-98fd-85bd22365d31',
                    client_secret='',
                    tenant_id='')

assunto = "Mensagem Automática"
conteudo = "Olá, sou o robô. Se eu puder te ajudar, basta me chamar."

# Enviando o e-mail
response = commonkit.send_email(to='carlens.oslin@ucpr.br', subject=assunto, body=conteudo)

if response.status_code == 202:
    print("E-mail enviado com sucesso!")
else:
    print("Falha ao enviar o e-mail.")

team_id = 'f99985a6-9e78-48cc-9df9-2581fd3a8555'
channel_id = '35220046-f566-4a93-b65e-b594e0d84b3b'

# Enviar mensagem para o canal de teste
teams_message = {
    "message": {
        "subject": "Mensagem automática",
        "body": {
            "contentType": "Text",
            "content": "Olá, sou o robô. Se eu puder te ajudar, basta me chamar."
        }
    }
}

# Enviando mensagem para o Teams
response = commonkit.send_message_to_teams(team_id=team_id, channel_id=channel_id, message=teams_message)

if response.status_code == 200:
    print("Mensagem enviada para o Teams com sucesso!")
else:
    print("Falha ao enviar a mensagem para o Teams.")
