import base64
import os
import requests

from ..microsoft.msal_auth import MSALAuth
from ..logger import Logger

class EmailIntegration:
    """Classe para manipulação de e-mails usando MSAL (Microsoft Authentication Library)."""

    def __init__(self, auth: MSALAuth, logger: Logger = Logger(name="EmailIntegration")) -> None:
        """
        Inicializa a integração de e-mail com MSAL.

        Args:
            auth (MSALAuth): Instância de MSALAuth para autenticação.
        """
        self.auth = auth
        self.logger = logger

    def get_emails_prime_token(self, access_token: str) -> dict:
        """
        Obtém os e-mails da caixa de entrada usando o token de acesso fornecido.

        Args:
            access_token (str): O token de acesso.

        Returns:
            dict: Os e-mails da caixa de entrada em formato JSON.
        """
        user_id = self.auth.user_id
        endpoint = f'https://graph.microsoft.com/v1.0/users/{user_id}/mailFolders/Inbox/messages?$search="subject:Mannesoft Prime - Envio de Token"&$top=1&$select=bodyPreview'
        request = requests.get(
            endpoint,
            headers={'Authorization': f'Bearer {access_token}'},
            timeout=30
        )

        if request.status_code == 200:
            self.logger.debug("E-mails obtidos com sucesso.")
            return request.json()
        self.logger.error(f"Erro ao obter e-mails: {request.status_code}")
        return {'status_code': request.status_code}

    def get_emails_mailbox(self, access_token: str) -> dict:
        """
        Obtém os e-mails da caixa de entrada usando o token de acesso fornecido.

        Args:
            access_token (str): O token de acesso.

        Returns:
            dict: Os e-mails da caixa de entrada em formato JSON.
        """
        user_id = self.auth.user_id
        endpoint = f'https://graph.microsoft.com/v1.0/users/{user_id}/mailFolders/Inbox/'
        request = requests.get(
            endpoint,
            headers={'Authorization': f'Bearer {access_token}'},
            timeout=30
        )

        if request.status_code == 200:
            self.logger.debug("E-mails obtidos com sucesso.")
            return request.json()
        self.logger.error(f"Erro ao obter e-mails: {request.status_code}")
        return {'status_code': request.status_code}

    def send_emails(
        self,
        access_token: str,
        subject: str,
        body_content: str,
        to_recipients: list,
        attachment_path: str = ''
    ) -> bool | dict:
        """
        Envia um e-mail utilizando o Microsoft Graph API.

        Args:
            access_token (str): Token de acesso OAuth para autenticar a requisição no Microsoft Graph.
            subject (str): Assunto do e-mail.
            body_content (str): Conteúdo do corpo do e-mail no formato de texto.
            to_recipients (list): Lista de destinatários no formato esperado pela API.
                                Exemplo: [{'EmailAddress': {'Address': 'email@example.com'}}]

        Returns:
            bool: Retorna True se o e-mail foi enviado com sucesso.
            dict: Retorna o JSON da resposta em caso de falha na requisição.
        """
        user_id = self.auth.user_id
        endpoint = f"https://graph.microsoft.com/v1.0/users/{user_id}/sendMail"

        if attachment_path:
            with open(attachment_path, 'rb') as attachment_file:
                content_bytes = attachment_file.read()

            email_message = {
                "Message": {
                    "Subject": subject,
                    "Body": {
                        "ContentType": "html",
                        "Content": body_content,
                    },
                    "ToRecipients": to_recipients,
                    "attachments": [
                        {
                            "@odata.type": "#microsoft.graph.fileAttachment",
                            "name": os.path.basename(attachment_path),
                            "contentBytes": base64.b64encode(content_bytes).decode('utf-8')
                        }
                    ],
                }
            }
        else:
            email_message = {
                "Message": {
                    "Subject": subject,
                    "Body": {
                        "ContentType": "html",
                        "Content": body_content,
                    },
                    "ToRecipients": to_recipients
                }
            }

        request = requests.post(
            endpoint,
            headers={'Authorization': f'Bearer {access_token}'},
            json=email_message
        )

        if request.ok:
            self.logger.debug("E-mail enviado com sucesso.")
            return True
        return request.json()