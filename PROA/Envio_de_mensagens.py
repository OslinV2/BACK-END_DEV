import requests
from commonkit import CommonKit
from bs4 import BeautifulSoup as bs4

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0'
}
re = requests.get('https://graph.microsoft.com/v1.0/groups/{group-id-for-teams}/members', headers=headers, verify=False)
soup = bs4(re.text, 'html.parser')
print(soup.prettify())


commonkit = CommonKit(client_id='',
                    client_secret='CLIENT_SECRET',
                    tenant_id='TENANT_ID')
# Canal - Testes
# id: f99985a6-9e78-48cc-9df9-2581fd3a8555
# tenant_id: 8a1ef6c3-8324-4103-bf4a-1328c5dc3653

# Meu
# id: 3af3b781-a88c-467b-98fd-85bd22365d31

assunto = "Mensagem Automática"
conteudo = "Olá, sou o robô. Se eu puder te ajudar, basta me chamar."

response = commonkit.send_email(to='carlens.oslin@ucpr.br', subject=assunto, body=conteudo)

if response.status_code == 202:
    print("E-mail enviado com sucesso!")
else:
    print("Falha ao enviar o e-mail.")

team_id = 'f99985a6-9e78-48cc-9df9-2581fd3a8555'
channel_id = ''

# Enviar mensagem para o canal de teste
teams_message = {
    "message": {
        "subject": "Mensagem automáttica",
        "body": {
            "contentType": "Text",
        "content": "Olá, sou o robô. Se eu puder te ajudar, basta me chamar."
    }
        }
        
}

response = commonkit.send_message_to_teams(team_id=team_id, channel_id=channel_id, message=teams_message)

if response.status_code == 200:
    print("Mensagem enviada para o Teams com sucesso!")
else:
    print("Falha ao enviar a mensagem para o Teams.")



# """
# ### **Requisitos:**
# 1. **Acesso à biblioteca CommonKit**.
# 2. **Credenciais de acesso ao Microsoft Graph API** (Client ID, Client Secret, Tenant ID).
# 3. **Acesso ao Microsoft Teams** e um canal de teste configurado.
# 4. **Conta de e-mail no Microsoft Outlook** ou similar.

# ### **Passos Seguidos:**

# 2. **Autenticação no Microsoft Graph API**:
#    - Registrar um aplicativo no **Azure Active Directory** para obter **Client ID**, **Client Secret** e **Tenant ID**.
#    - Conceder permissões de envio de e-mails e leitura de mensagens do Teams.

# 3. **Enviar E-mail**:
#    - Configurar o CommonKit com as credenciais obtidas.
#    - Usar o método `send_email()` para enviar um e-mail para o próprio usuário.

# 4. **Enviar Mensagem no Microsoft Teams**:
#    - Usar o método `send_message_to_teams()` do CommonKit para enviar uma mensagem ao canal de teste no Teams.

# 5. **Verificação**:
#    - Verificar o recebimento do e-mail na caixa de entrada.
#    - Confirmar que a mensagem foi postada corretamente no canal do Teams.
# """