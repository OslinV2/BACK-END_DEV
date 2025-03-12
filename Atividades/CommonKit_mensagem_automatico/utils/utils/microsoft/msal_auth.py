import os
import msal
from ..criptador import decypher
from ..logger import Logger


class MSALAuth:
    """Classe para autenticação com MSAL (Microsoft Authentication Library)."""

    def __init__(self, tenant_id: str = "", scopes: str = "", need_dict: bool=False, logger: Logger = Logger(name="MSALIntegration")) -> None:
        """
        Inicializa a autenticação com MSAL.

        Args:
            tenant_id (str, optional): O ID do locatário (tenant). Se não fornecido, será obtido da variável de ambiente MSAL_TENANT_ID.
            scopes (str, optional): Os escopos para a autorização. Se não fornecido, usará um escopo padrão.
            need_dict (bool, optional): Se True, retorna o dicionário completo. Se False, retorna apenas o token de acesso. Padrão é False.
        """
        self.tenant_id = tenant_id if tenant_id else decypher(os.environ['MSAL_TENANT_ID'])
        self.scopes = scopes if scopes else ["https://graph.microsoft.com/.default"]
        self.client_id = decypher(os.environ['MSAL_CLIENT_ID'])
        self.client_secret = decypher(os.environ['MSAL_CLIENT_SECRET'])
        self.user_id = decypher(os.environ['MSAL_USER_ID'])
        self.username = decypher(os.environ['MSAL_USER'])
        self.password = decypher(os.environ['MSAL_PASSWORD'])
        self.need_dict = need_dict
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.app = msal.ConfidentialClientApplication(
            client_id=self.client_id,
            client_credential=self.client_secret,
            authority=self.authority
        )
        self.logger = logger

    def get_token_by_user_and_password(self) -> str:
        """
        Obtém o token de acesso usando o nome de usuário e senha fornecidos.

        Returns:
            str: O token de acesso.
        """
        result = self.app.acquire_token_by_username_password(
            username=self.username,
            password=self.password,
            scopes=self.scopes
        )
        if "access_token" in result and self.need_dict:
            self.logger.debug(f"Token obtido com sucesso para o usuário {self.username}.")
            return result
        if "access_token" in result:
            self.logger.debug(f"Token obtido com sucesso para o usuário {self.username}.")
            return result["access_token"]
        self.logger.error("Erro ao obter token por nome de usuário e senha.")
        return ""

    def get_token_by_scope(self) -> str:
        """
        Obtém o token de acesso usando os escopos fornecidos.

        Returns:
            str: O token de acesso.
        """
        result = self.app.acquire_token_for_client(scopes=self.scopes)
        if "access_token" in result:
            self.logger.debug(f"Token obtido com sucesso para os escopos {self.scopes}.")
            return result["access_token"]
        self.logger.error("Erro ao obter token por escopos.")
        return ""
