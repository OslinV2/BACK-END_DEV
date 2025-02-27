"""Classe de conexão com CosmosDB e métodos para interagir com o banco."""
from typing import List
import os
import pymongo

from .logger import Logger


class DBConnect:
    """Classe de conexão do CosmosDB"""
    def __init__(self, uri=os.getenv("CONNECTION_STRING"), database_name="", logger: Logger = Logger(name="MongoDB")):
        """
        Inicializa o objeto CosmosConnect.

        Args:
            uri (str): O URI do MongoDB. Se não fornecido, será obtido da variável de ambiente CONNECTION_STRING.
            database_name (str): O nome do banco de dados MongoDB.
            container_name (str): O nome da coleção MongoDB (contêiner).
        """
        self.client = self.__open_connection(uri)
        self.database = self.client[database_name]
        self.logger = logger

    def __open_connection(self, uri=None):
        """
        Abre uma conexão com o servidor MongoDB.

        Args:
            uri (str): O URI do MongoDB. Se não fornecido, será obtido da variável de ambiente CONNECTION_STRING.

        Returns:
            pymongo.MongoClient: Um objeto MongoClient representando a conexão com o servidor MongoDB.
        """
        if uri is None:
            uri = os.getenv("CONNECTION_STRING")
        if uri is None:
            raise ValueError("URI do MongoDB não fornecido.")
        return pymongo.MongoClient(uri)

    def is_connected(self) -> bool:
        """
        Verifica se a conexão com o banco de dados está ativa.

        Returns:
            bool: True se a conexão estiver ativa, False caso contrário.
        """
        try:
            server_info = self.client.server_info()
            self.logger.debug(message=f"Conexão com o MongoDB está ativa. {server_info}")
            return True
        except pymongo.errors.ServerSelectionTimeoutError:
            return False

    def create_document(self, document: dict, container: str) -> str:
        """
        Cria um novo documento na coleção.

        Args:
            document (dict): O documento a ser inserido na coleção.
            container (str): O container onde estão os dados.

        Returns:
            str: O _id do documento inserido.
        """
        self.container = self.database[container]
        insert_id = self.container.insert_one(document).inserted_id
        self.logger.debug(message=f"Id inserido: {insert_id}")
        return insert_id

    def get_document(self, document_id: str, container: str) -> dict:
        """
        Recupera um documento da coleção.

        Args:
            document_id (str): O _id do documento a ser recuperado.
            container (str): O container onde estão os dados.

        Returns:
            dict: O documento correspondente ao _id fornecido, ou None se não encontrado.
        """
        self.container = self.database[container]
        result = self.container.find_one({"_id": document_id})
        self.logger.debug(message=f"Retorno da busca pelo id {document_id}: {result}")
        return result

    def update_document(self, document_id: str, update_data: dict, container: str) -> None:
        """
        Atualiza um documento na coleção.

        Args:
            document_id (str): O _id do documento a ser atualizado.
            update_data (dict): Os dados a serem atualizados no documento.
            container (str): O container onde estão os dados.
        """
        self.container = self.database[container]
        result = self.container.update_one({"_id": document_id}, {"$set": update_data})
        self.logger.debug(message=f"Documento com id {document_id} atualizado. Resultado: {result.modified_count} documentos modificados.")

    def delete_document(self, document_id: str, container: str) -> None:
        """
        Exclui um documento da coleção.

        Args:
            document_id (str): O _id do documento a ser excluído.
            container (str): O container onde estão os dados.
        """
        self.container = self.database[container]
        result = self.container.delete_one({"_id": document_id})
        self.logger.debug(message=f"Documento com id {document_id} excluído. Resultado: {result.deleted_count} documentos excluídos.")

    def list_documents(self, container: str, filter_mongo:dict|None=None, projection:dict|None=None) -> pymongo.cursor.Cursor:
        """
        Lista todos os documentos na coleção, seguindo um filtro ou não.

        Args:
            container (str): O container onde estão os dados.
            filter_mongo (dict | None, optional): filtro para listar os documentos
            projection (dict | None, optional): Projeção para listar os documentos

        Returns:
            pymongo.cursor.Cursor: Um cursor para iterar sobre os documentos na coleção.
        """
        self.container = self.database[container]
        cursor = self.container.find(filter=filter_mongo, projection=projection)
        self.logger.debug(message=f"Documentos listados na coleção {container}. Filtro: {filter_mongo}, Projeção: {projection}")
        return cursor

    def insert_many_documents(self, documents: List[dict], container: str):
        """
        Insere vários documentos na coleção.

        Args:
            documents (list): Uma lista de documentos a serem inseridos na coleção.
            container (str): O container onde estão os dados.
        """
        self.container = self.database[container]
        result = self.container.insert_many(documents)
        self.logger.debug(message=f"{len(result.inserted_ids)} documentos inseridos na coleção {container}.")

    def drop_collection(self, container: str):
        """
        Exclui uma coleção do banco de dados.

        Args:
            container (str): O nome da coleção a ser excluída.
        """
        self.database.drop_collection(container)
        self.logger.debug(message=f"A coleção {container} foi excluída com sucesso.")

    def clear_collection(self, container: str):
        """
        Limpa todos os dados de uma coleção sem dropar a coleção.

        Args:
            container (str): O nome da coleção a ser limpa.
        """
        self.container = self.database[container]
        result = self.container.delete_many({})
        self.logger.debug(message=f"Todos os documentos da coleção {container} foram removidos. Total de documentos removidos: {result.deleted_count}.")

    def aggregate_documents(self, container: str, pipeline: List[dict]) -> list:
        """
        Executa uma agregação na coleção.

        Args:
            container (str): O container onde estão os dados.
            pipeline (list): Uma lista de etapas de agregação.

        Returns:
            pymongo.command_cursor.CommandCursor: Um cursor para iterar sobre os documentos agregados.
        """
        self.container = self.database[container]
        result = self.container.aggregate(pipeline)
        self.logger.debug(message=f"Agregação executada na coleção {container}. Pipeline: {pipeline}")
        return list(result)

    def find_one_and_delete(self, filter_mongo: dict, container: str) -> dict | None:
        """
        Encontra e exclui um único documento na coleção.

        Args:
            filter_mongo (dict): O filtro para encontrar o documento.
            container (str): O container onde estão os dados.

        Returns:
            dict | None: O documento excluído ou None se não encontrado.
        """
        self.container = self.database[container]
        result = self.container.find_one_and_delete(filter_mongo)
        self.logger.debug(message=f"Documento encontrado e excluído na coleção {container} com o filtro: {filter_mongo}. Resultado: {result}")
        return result

    def find_one_and_update(self, filter_mongo: dict, update_data: dict, container: str, return_new: bool = False) -> dict | None:
        """
        Encontra e atualiza um único documento na coleção.

        Args:
            filter_mongo (dict): O filtro para encontrar o documento.
            update_data (dict): Os dados a serem atualizados no documento.
            container (str): O container onde estão os dados.
            return_new (bool): Se True, retorna o documento após a atualização. Se False, retorna o documento antes da atualização. Padrão é False.

        Returns:
            dict | None: O documento atualizado (ou original) ou None se não encontrado.
        """
        self.container = self.database[container]
        return_document = pymongo.ReturnDocument.AFTER if return_new else pymongo.ReturnDocument.BEFORE
        result = self.container.find_one_and_update(filter_mongo, {"$set": update_data}, return_document=return_document)
        self.logger.debug(message=f"Documento encontrado e atualizado na coleção {container} com o filtro: {filter_mongo}. Atualizações: {update_data}. Resultado: {result}")
        return result