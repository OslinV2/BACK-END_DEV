import requests

from ..microsoft.msal_auth import MSALAuth
from ..logger import Logger

class TeamsIntegrations:

    """Classe para integrar com o Microsoft Teams."""

    def __init__(self, auth: MSALAuth, logger: Logger = Logger(name="TeamsIntegrations")) -> None:
        """
        Inicializa a integração com o Microsoft Teams.

        Args:
            auth (MSALAuth): Instância de MSALAuth para autenticação.
        """
        self.auth = auth
        self.logger = logger

    def send_message(self, token: str, team_id: str, channel_id: str, message: str, mentions: dict) -> bool:
        """
        Envia uma mensagem para um canal específico de uma equipe no Microsoft Teams.

        Args:
            token (str): O token de acesso.
            team_id (str): O ID da equipe.
            channel_id (str): O ID do canal.
            message (str): A mensagem a ser enviada.
            mentions (dict): O dicionario de menções.

        Returns:
            bool: True se a mensagem foi enviada com sucesso, False caso contrário.
        """
        headers = {'Authorization': 'Bearer ' + token}
        endpoint = f'https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages'
        body = {
            "body": {
                "content": message,
                "contentType": 'html'
            }
        }

        if mentions:
            body["mentions"] = mentions

        try:
            response = requests.post(endpoint, json=body, headers=headers, timeout=30)
            response.raise_for_status()
            self.logger.debug(f"Mensagem enviada com sucesso: {message}")
            return True
        except requests.exceptions.RequestException as e:
            print(e)
            self.logger.error(f"Erro ao enviar mensagem para o Microsoft Teams: {e}")
            return False

    def get_channel_messages(self, token: str, team_id: str, channel_id: str, filter:str="") -> dict | None:
        """
        Obtém mensagens de um canal específico de uma equipe no Microsoft Teams.

        Args:
            token (str): O token de acesso.
            team_id (str): O ID da equipe.
            channel_id (str): O ID do canal.
            filter (str): O filtro a ser aplicado na busca

        Returns:
            dict: As mensagens do canal.
            None: Se ocorrer um erro durante a requisição.
        """
        url = f"https://graph.microsoft.com/beta/teams/{team_id}/channels/{channel_id}/messages"
        if filter:
            url = f"{url}/delta?$filter={filter}"

        headers = {"Authorization": f"Bearer {token}"}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            self.logger.debug("Mensagens retornadas com sucesso.")
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Erro ao capturar mensagens para o Microsoft Teams: {e}")
            return None
