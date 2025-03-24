import os
from dotenv import load_dotenv
from commonKit.utils.microsoft.msal_auth import MSALAuth
from commonKit.utils.microsoft.teams_integrations import TeamsIntegrations
from commonKit.utils.microsoft.email_integration import EmailIntegration

# Chamando o .env
load_dotenv()
# puxando os id e infomações do .env
username = os.environ['MSAL_USER']
password = os.environ['MSAL_PASSWORD']
client_id = os.environ['MSAL_CLIENT_ID']
client_secret = os.environ['MSAL_CLIENT_SECRET']
tenant_id = os.environ['MSAL_TENANT_ID']
team_id = os.environ['TEAM_ID']
channel_id = os.environ['CHANNEL_ID']
mensagem = os.environ['MESSAGE_CONTENT']
email_destinatario = os.environ['USER_EMAIL']
# Inicializando a autenticação com o MSAL
msal_auth = MSALAuth()
# Pegando o token
token = msal_auth.get_token_by_user_and_password()

def mensagem_teams():
    """
    Envia uma mensagem para um canal do Teams.
    """
    teams = TeamsIntegrations(auth=msal_auth)  # Passando auth no construtor
    envio_teams = teams.send_message( # Enviando a mensagem no canal
        token=token,
        team_id=team_id,
        channel_id=channel_id,
        message=mensagem,
        mentions=None
    )
    print("Mensagem enviada com sucesso!" if envio_teams else "Erro ao enviar mensagem.")
# Chamando a função de envio
mensagem_teams()

def email_outlook():
    """
    Envia uma mensagem para o próprio email no outlook.
    """
    assunto_email = "Notificação Automática - CommonKit"
    corpo_email = "Esta é uma mensagem automática enviada pelo sistema."
    destinatarios = [{'EmailAddress': {'Address': email_destinatario}}]

    # Enviar e-mail pelo Microsoft Graph API
    outlook = EmailIntegration(auth=msal_auth) # Passando auth no construtor
    envio_sucesso = outlook.send_emails( # Enviando a mensage no email
        access_token=token,
        subject=assunto_email,
        body_content=corpo_email,
        to_recipients=destinatarios
    )

    print("E-mail enviado com sucesso!") if envio_sucesso else print("Falha ao enviar o e-mail:", envio_sucesso)
# Chamando a função de envio
email_outlook()