import os
import base64
from dotenv import load_dotenv
from commonKit.utils.microsoft.msal_auth import MSALAuth
from commonKit.utils.microsoft.teams_integrations import TeamsIntegrations
from commonKit.utils.criptador import decypher

load_dotenv()

# Obter as variáveis descriptografadas diretamente
user = decypher(os.environ['MSAL_USER_ID'])
password = decypher(os.environ['MSAL_PASSWORD'])
client_id = decypher(os.environ['MSAL_CLIENT_ID'])
client_secret = decypher(os.environ['MSAL_CLIENT_SECRET'])
tenant_id = decypher(os.environ['MSAL_TENANT_ID'])
team_id = decypher(os.environ['TEAM_ID'])
channel_id = decypher(os.environ['CHANNEL_ID'])
mensagem = decypher(os.environ['MESSAGE_CONTENT'])
email_destinatario = decypher(os.environ['EMAIL_DESTINATARIO'])  # Exemplo: 'email@example.com'
assunto_email = "Notificação Automática"
corpo_email = "Esta é uma mensagem automática enviada pelo sistema."

# Criando uma instância de MSALAuth para autenticação
msal_auth = MSALAuth(
    username=user,
    password=password,
    client_id=client_id,
    client_secret=client_secret,
    tenant_id=tenant_id
)

# Pegando o token
token = msal_auth.get_token_by_user_and_password()

def mensagem_teams():
    """
    Envia uma mensagem para o canal do Teams e também chama a função de enviar e-mail.
    """
    # Criando instância de TeamsIntegrations com o token
    teams = TeamsIntegrations(token=token, team_id=team_id, channel_id=channel_id, message=mensagem)

    # Enviar a mensagem no canal do Teams
    try:
        teams.send_message()
        print("Mensagem enviada com sucesso para o Teams!")
    except Exception as e:
        print(f"Erro ao enviar mensagem para o Teams: {e}")

    # Chama a função de enviar e-mail após enviar a mensagem no Teams
    email_outlook()

def email_outlook():
    """
    Envia um e-mail usando a função send_emails().
    """
    # Definindo os destinatários do e-mail no formato esperado
    destinatarios = [{'EmailAddress': {'Address': email_destinatario}}]

    # Enviar e-mail pelo Microsoft Graph API
    envio_sucesso = msal_auth.send_emails(
        access_token=token,
        subject=assunto_email,
        body_content=corpo_email,
        to_recipients=destinatarios
    )

    if envio_sucesso:
        print("E-mail enviado com sucesso!")
    else:
        print("Falha ao enviar o e-mail:", envio_sucesso)


# Base Lógico:
# - Objetivo:
# - Enviar mensagem/email no outlook
# - Enviar mensagem no canal de teste do teams

# função mensagem_teams()
# - Chamar a função do get_token_by_user_and_password() do código msal_auth.py, pra pegar o token
# - Inserir o token, team_id, channel_id, message, mentions no Teams_integrations assim completando os requesitos pra enviar a mensagem no canal do teams.

# função email_outlook()
# - Chamar a função de send_emails(), pra enviar a mensagem pro outlook no meu email, comprir os requisitos necessários e prosseguir.......