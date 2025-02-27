import os

from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
from office365.sharepoint.files.move_operations import MoveOperations

from ..logger import Logger
from ..microsoft.msal_auth import MSALAuth


class SharePoint:
    """Classe para integrar com o Microsoft SharePoint."""

    def __init__(self, url: str, auth: MSALAuth, logger: Logger = Logger(name="SharePointIntegration")) -> None:
        """
        Inicializa a integração com o Microsoft SharePoint.

        Args:
            url (str): A URL do site do SharePoint.
            auth (MSALAuth): Instância de MSALAuth para autenticação.
        """
        self.url = url
        self.auth = auth
        self.logger = logger
        self.ctx = self.__authenticate()

    def __authenticate(self) -> ClientContext:
        """Autentica com o SharePoint usando credenciais de usuário."""
        client_credentials = UserCredential(self.auth.username, self.auth.password)
        ctx = ClientContext(self.url).with_credentials(client_credentials)
        self.logger.debug(f"Autenticado com sucesso no SharePoint: {self.url}")
        return ctx

    def upload_file(self, target_folder: str, file_path: str) -> None:
        """
        Faz upload de um arquivo para uma pasta no SharePoint.

        Args:
            target_folder (str): Caminho da pasta de destino no SharePoint.
            file_path (str): Caminho do arquivo a ser carregado.
        """
        folder = self.ctx.web.get_folder_by_server_relative_url(target_folder)
        with open(file_path, 'rb') as content_file:
            file_content = content_file.read()
            folder.upload_file(os.path.basename(file_path), file_content).execute_query()
        self.logger.debug(f"Arquivo {file_path} carregado com sucesso para {target_folder}")

    def list_files(self, target_folder: str) -> list:
        """
        Lista os arquivos em uma pasta no SharePoint.

        Args:
            target_folder (str): Caminho da pasta no SharePoint.

        Returns:
            list: Lista de URLs relativas dos arquivos na pasta.
        """
        folder = self.ctx.web.get_folder_by_server_relative_path(target_folder)
        files = folder.get_files(True).execute_query()
        file_urls = [self.__get_file_url(f) for f in files]
        self.logger.debug(f"Arquivos listados com sucesso na pasta {target_folder}")
        return file_urls

    def __get_file_url(self, file: File) -> str:
        """Obtém a URL relativa de um arquivo."""
        return file.properties['ServerRelativeUrl']

    def delete_file(self, target_file: str) -> None:
        """
        Remove um arquivo no SharePoint.

        Args:
            target_file (str): Caminho do arquivo no SharePoint.
        """
        file = self.ctx.web.get_file_by_server_relative_url(target_file)
        file.delete_object().execute_query()
        self.logger.debug(f"Arquivo {target_file} removido com sucesso")

    def rename_file(self, old_path: str, new_name: str) -> None:
        """
        Renomeia um arquivo no SharePoint.

        Args:
            old_path (str): Caminho atual do arquivo.
            new_name (str): Novo nome para o arquivo.
        """
        file = self.ctx.web.get_file_by_server_relative_url(old_path)
        file.rename(new_name).execute_query()
        self.logger.debug(f"Arquivo {old_path} renomeado para {new_name}")

    def download_file(self, target_file: str, local_folder: str) -> None:
        """
        Faz download de um arquivo do SharePoint.

        Args:
            target_file (str): Caminho do arquivo no SharePoint.
            local_folder (str): Pasta local onde o arquivo será salvo.
        """
        local_file = os.path.join(local_folder, os.path.basename(target_file))
        with open(local_file, 'wb') as local:
            file = self.ctx.web.get_file_by_server_relative_url(target_file)
            file.download(local).execute_query()
        self.logger.debug(f"Arquivo {target_file} baixado com sucesso para {local_file}")

    def get_file_properties(self, target_file: str) -> dict:
        """
        Obtém as propriedades de um arquivo no SharePoint.

        Args:
            target_file (str): Caminho do arquivo no SharePoint.

        Returns:
            dict: Propriedades do arquivo.
        """
        file = self.ctx.web.get_file_by_server_relative_url(target_file).get().execute_query()
        self.logger.debug(f"Propriedades do arquivo {target_file} obtidas com sucesso")
        return file.properties

    def move_file(self, old_path: str, new_path: str) -> None:
        """
        Move um arquivo no SharePoint.

        Args:
            old_path (str): Caminho atual do arquivo.
            new_path (str): Novo caminho para o arquivo.
        """
        file = self.ctx.web.get_file_by_server_relative_url(old_path)
        file.moveto(new_path, MoveOperations.overwrite).execute_query()
        self.logger.debug(f"Arquivo {old_path} movido para {new_path}")

    def delete_all_files_in_folder(self, target_folder: str) -> None:
        """
        Remove todos os arquivos em uma pasta no SharePoint.

        Args:
            target_folder (str): Caminho da pasta no SharePoint.
        """
        folder = self.ctx.web.get_folder_by_server_relative_url(target_folder)
        files = folder.files.get().execute_query()

        for file in files:
            file.delete_object().execute_query()
            self.logger.debug(f"Arquivo {file.properties['Name']} removido da pasta {target_folder}")

        self.logger.debug(f"Todos os arquivos da pasta {target_folder} foram removidos com sucesso")
