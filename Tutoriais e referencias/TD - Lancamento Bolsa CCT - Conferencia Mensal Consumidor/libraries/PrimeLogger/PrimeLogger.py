import os
import datetime
import logging
import logging.config

from typing import Any, Optional
from robot.api import logger
from uuid import uuid4

from libraries.Connections.MongoConnect import MongoConnect

HIDE_FLAG = "hide"

class PrimeLogger:
    """Listener e keywords para enviar os logs ao CosmosDB.

    O índice será criado no seguinte padrão:
    "{args} - {asctime} - {self.nome_robo} - {message} - {self.id} - ID: {traceId}"
    Ex.: LEVEL - %Y-%m-%d %H:%M:%S - app_name - Mensagem - UUID4 - ID: 0000000000

    Variáveis de ambiente obrigatórias:
    - ROBOT_NAME: nome do robô
    - CLIENT: nome do cliente
    ...

    Variáveis opcionais:
    - TIMEZONE: padrão > 'America/Sao_Paulo'

    Importação:
    importar PrimeLogger nas bibliotecas do projeto robot.
    Exemplo:
        *** Settings ***
        Library    PrimeLogger

    Keywords:
    - Log Info: enviar o log com o level INFO e os argumentos para o CosmosDB, para apresentar no console -> console=True
        Ex.: Log Info   Mensagem   console=True  traceId=${traceId}  ....  N_ARG:${N_ARG}

    - Log Warn: enviar o log com o level WARN e os argumentos para o CosmosDB
        Ex.: Log Warn   Mensagem   traceId=${traceId}  nome=${nome}  ....  N_ARG:${N_ARG}

    - Log Debug: enviar o log com o level Debug e os argumentos para o CosmosDB
        Ex.: Log Debug   Mensagem   traceId=${traceId}  nome=${nome}  ....  N_ARG:${N_ARG}

    - Log Error: enviar o log com o level Error e os argumentos para o CosmosDB
        Ex.: Log Error   Mensagem   traceId=${traceId}  nome=${nome}  ....  N_ARG:${N_ARG}
    """

    ROBOT_LISTENER_API_VERSION = 2


    def __init__(self) -> None:
        """
        Inicializa uma instância da biblioteca de logs.
        """
        self.ROBOT_LIBRARY_LISTENER = self
        self.log_level = logging._nameToLevel['INFO']
        self.id: str = str(uuid4()).upper()
        self.nome_robo: str = os.path.dirname(__file__).split('\\')[-3]
        self.banco = MongoConnect(is_log=True)

    def log_info(self, message: str = '', traceId: Optional[str] = None, **kwargs: Any):
        """Log level info"""
        kwargs["level"] = 'INFO'
        msg = self._message(message, traceId=traceId, **kwargs)
        also_console = kwargs.pop("console", False)
        logger.info(msg, html=True, also_console=also_console)
        self._insert_log(message, level=kwargs["level"], traceId=traceId)

    def log_warn(self, message: str = '', traceId: Optional[str] = None, **kwargs: Any):
        """Log level warn"""
        kwargs['level'] = 'WARN'
        msg = self._message(message, traceId=traceId, **kwargs)
        logger.warn(msg, html=True)
        self._insert_log(message, level=kwargs["level"], traceId=traceId)

    def log_debug(self, message: str = '', traceId: Optional[str] = None, **kwargs: Any):
        """Log level debug"""
        kwargs['level'] = 'DEBUG'
        msg = self._message(message, traceId=traceId, **kwargs)
        logger.debug(msg, html=True)
        self._insert_log(message, level=kwargs["level"], traceId=traceId)

    def log_error(self, message: str = '', traceId: Optional[str] = None, **kwargs: Any):
        """Log level error"""
        kwargs['level'] = 'ERROR'
        msg = self._message(message, traceId=traceId, **kwargs)
        logger.error(msg, html=True)
        self._insert_log(message, level=kwargs["level"], traceId=traceId)

    def _message(self, message: str = '', traceId: Optional[str] = None, **kwargs: Any):
        """Formata mensagem e argumentos, retornando uma única string"""
        asctime = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        msg = ""
        args = ""
        for key, value in kwargs.items():
            if key == "level":
                args = value
            if key == "mensagem":
                message += f" {value}"

        msg = args if message == '' else f'{msg} | {args}'
        msg = f"{args} - {asctime} - {self.nome_robo} - {message} - {self.id} - ID: {traceId}"
        return msg

    def _insert_log(self, msg: str, **kwargs: Any):
        """Insere o log na coleção 'logs_collection'"""
        if msg:
            self.banco.open_connections()
            msg_split = msg.split("-")
            if len(msg_split) > 9:
                self.banco.insert_one(collection=self.nome_robo, query={
                    "log_level": msg_split[0].strip(),
                    "timestamp": msg_split[1].strip(),
                    "nome_robo": self.nome_robo,
                    "message": msg_split[3].strip(),
                    "id_robo": self.id,
                    "trace_id": msg_split[9].strip(),
                    "log_line": msg
                })

    def start_suite(self, name: str, attributes: dict):
        """Listener Function"""
        info = dict(
            name=name,
            totaltasks=attributes['totaltests'],
            tasks=str(attributes['tests']),
            doc=attributes['doc'],
            starttime=attributes['starttime'],
            trigger_type='start_suite'
        )
        self.log_info(**info)

    def start_test(self, name: str, attributes: dict):
        """Listener Function"""
        info = dict(
            name=name,
            doc=attributes['doc'],
            starttime=attributes['starttime'],
            trigger_type='start_task'
        )
        self.log_info(**info)

    def start_keyword(self, name: str, attributes: dict):
        """Listener Function"""
        info = dict(
            name=name,
            doc=attributes['doc'],
            args=str(attributes['args']),
            starttime=attributes['starttime'],
            trigger_type='start_keyword'
        )
        self.log_debug(**info)

    def end_keyword(self, name: str, attributes: dict):
        """Listener Function"""
        info = dict(
            name=name,
            endtime=attributes['endtime'],
            elapsedtime=attributes['elapsedtime'],
            status=attributes['status'],
            trigger_type='end_keyword'
        )
        self.log_debug(**info)

    def end_test(self, name: str, attributes: dict):
        """Listener Function"""
        info = dict(
            name=name,
            endtime=attributes['endtime'],
            elapsedtime=attributes['elapsedtime'],
            status=attributes['status'],
            sys_message=attributes['message'],
            trigger_type='end_task'
        )
        self.log_info(**info)

    def end_suite(self, name: str, attributes: dict):
        """Listener Function"""
        info = dict(
            name=name,
            endtime=attributes['endtime'],
            elapsedtime=attributes['elapsedtime'],
            status=attributes['status'],
            statistics=attributes['statistics'],
            sys_message=attributes['message'],
            trigger_type='end_suite'
        )
        self.log_info(**info)

    def log_message(self, message):
        """Listener Function"""
        self.log_debug(str(message['message']))
