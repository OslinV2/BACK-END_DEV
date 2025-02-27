from dotenv import load_dotenv
import os
from commonKit.utils.microsoft.msal_auth import MSALAuth
from commonKit.utils.microsoft.teams_integrations import TeamsIntegrations
from commonKit.utils.criptador import cypher, decypher
# Carregar variáveis do .env
load_dotenv()

# Obter as variáveis criptografadas diretamente
user = decypher(os.environ['MSAL_USER_ID'])
password = decypher(os.environ['MSAL_PASSWORD'])
client_id = decypher(os.environ['MSAL_CLIENT_ID'])
client_secret = decypher(os.environ['MSAL_CLIENT_SECRET'])
tenant_id = decypher(os.environ['MSAL_TENANT_ID'])
user_id = decypher(os.environ['MSAL_USER_ID'])
team_id = decypher(os.environ['TEAM_ID'])
channel_id = decypher(os.environ['CHANNEL_ID'])
coordinator = decypher(os.environ['COORDINATOR'])
mensagem = decypher(os.environ['MESSAGE_CONTENT'])

# Pegando o token da variável get_token_by_user_and_password(), a partir do username, password, scopes
token = MSALAuth(
    
)

mensagem = TeamsIntegrations(
    token= coordinator,
    team_id= team_id,
    channel_id= channel_id,
    message= mensagem
)

    
# Obter o token de acesso
token = auth.get_token_by_user_and_password()
# Criar uma instância de TeamsIntegrations
teams_integration = TeamsIntegrations(auth=auth)
# Definir a mensagem
message = "Olá, sou o robô. Se eu puder te ajudar, basta me chamar."
# Enviar mensagem no Microsoft Teams
mentions = {}  # Se necessário, adicionar menções
message_sent = teams_integration.send_message(token=token, team_id=team_id, channel_id=channel_id, message=message, mentions=mentions)
if message_sent:
    print("✅ Mensagem enviada com sucesso no Microsoft Teams!")
else:
    print("❌ Falha ao enviar mensagem no Microsoft Teams.")
# Enviar e-mail para o próprio usuário
subject = "Mensagem do Robô"
email_sent = teams_integration.send_email(token=token, subject=subject, content=message, to_email=user)
if email_sent:
    print("✅ E-mail enviado com sucesso!")
else:
    print("❌ Falha ao enviar e-mail.")

def email_outlook()



def mensagem_teams()


# Base Lógico:
# - Objetivo:
# - Enviar mensagem emailno outlook
# - Enviar mensagem no canal de teste do teams

# função mensagem_teams()
# - Chamar a função do get_token_by_user_and_password() do código msal_auth.py, pra pegar o token
# - Inserir o token, team_id, channel_id, message, mentions no Teams_integrations assim completando os requesitos pra enviar a mensagem no canal do teams.

# função email_outlook()
# - Chamar a função de send_emails(), pra enviar a mensagem pro outlook no meu email, comprir os requisitos necessários e prosseguir.......