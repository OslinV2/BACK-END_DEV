import requests
from commonKit.utils.microsoft.teams_integrations import TeamsIntegrations
from commonKit.utils.microsoft.msal_auth import MSALAuth
from dotenv import load_dotenv
import os

load_dotenv()

# Criando autenticação
auth = MSALAuth(tenant_id=TENANT_ID)
token = auth.get_token_by_user_and_password()

if not token:
    print("Erro ao obter token de autenticação.")
    exit()

# Enviar e-mail via Graph API
email_url = "https://graph.microsoft.com/v1.0/me/sendMail"
email_data = {
    "message": {
        "subject": "Mensagem Automática",
        "body": {"contentType": "Text", "content": MESSAGE_CONTENT},
        "toRecipients": [{"emailAddress": {"address": USER_EMAIL}}],
    }
}
email_headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

email_response = requests.post(email_url, json=email_data, headers=email_headers)

if email_response.status_code == 202:
    print("E-mail enviado com sucesso!")
else:
    print(f"Erro ao enviar e-mail: {email_response.text}")

# Enviar mensagem no Teams
teams = TeamsIntegrations(auth)
message_sent = teams.send_message(token, TEAM_ID, CHANNEL_ID, MESSAGE_CONTENT, mentions={})

if message_sent:
    print("Mensagem no Teams enviada com sucesso!")
else:
    print("Erro ao enviar mensagem no Teams.")
