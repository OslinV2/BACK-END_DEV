import os
import requests
from commonKit.utils.microsoft.msal_auth import MSALAuth
from commonKit.utils.microsoft.teams_integrations import TeamsIntegrations
from commonKit.utils.logger import Logger

# instância de logger
logger = Logger(name="EnvioMensagemLogger")
# Inicializar MSALAuth com os valores criptografados do .env
auth = MSALAuth(
    logger=logger,
    user=os.environ['MSAL_USER'],
    password=os.environ['MSAL_PASSWORD'],
    client_id=os.environ['MSAL_CLIENT_ID'],
    client_secret=os.environ['MSAL_CLIENT_SECRET'],
    tenant_id=os.environ['MSAL_TENANT_ID'],
    user_id=os.environ['MSAL_USER_ID']
)

# Obter o token de acesso
token = auth.get_token_by_user_and_password()
# Criar uma instância de TeamsIntegrations
teams_integration = TeamsIntegrations(auth=auth, logger=logger)
message = "Olá, sou o robô. Se eu puder te ajudar, basta me chamar."

# Enviar mensagem no Microsoft Teams
team_id = os.environ['TEAM_ID']
channel_id = os.environ['CHANNEL_ID']
mentions = {}

message_sent = teams_integration.send_message(token=token, team_id=team_id, channel_id=channel_id, message=message, mentions=mentions)

if message_sent:
    logger.debug("Mensagem enviada com sucesso no Microsoft Teams.")
else:
    logger.error("Falha ao enviar mensagem no Microsoft Teams.")


def send_email(token: str, subject: str, content: str, to_email: str) -> bool:
    endpoint = "https://graph.microsoft.com/v1.0/me/sendMail"
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }
    
    body = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": content
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": to_email
                    }
                }
            ]
        }
    }
    
    try:
        response = requests.post(endpoint, json=body, headers=headers)
        response.raise_for_status()
        logger.debug(f"E-mail enviado para {to_email}.")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao enviar e-mail: {e}")
        return False

# Enviar o e-mail para o próprio usuário
user_email = os.environ['USER_EMAIL']
subject = "Mensagem do Robô"
email_sent = send_email(token, subject, message, user_email)

if email_sent:
    logger.debug("E-mail enviado com sucesso.")
else:
    logger.error("Falha ao enviar e-mail.")
