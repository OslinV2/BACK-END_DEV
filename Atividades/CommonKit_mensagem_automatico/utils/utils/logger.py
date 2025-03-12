"""Modulo para gerenciar logs."""
import datetime
import json
import logging
import logging.config
import os
import sys

from uuid import uuid4


class ExcludeAsyncioTestCaseFilter(logging.Filter):  # pylint: disable=too-few-public-methods
    """Filtro personalizado para excluir mensagens geradas por IsolatedAsyncioTestCase._asyncioLoopRunner()."""

    def filter(self, record):
        """Filtrar mensagens baseadas no conteúdo."""
        return "IsolatedAsyncioTestCase._asyncioLoopRunner()" not in record.getMessage()


class Logger:
    """Classe para gerenciar logs."""

    def __init__(self, name="app_name", db_conn=None):
        """
        Inicializa um novo objeto Logger.

        Args:
            name (str): O nome do logger.
            db_conn (DBConnect): Conexão com o banco onde os logs serão salvos.

        Returns:
            None
        """

        if db_conn:
            self.db = db_conn

        self.is_data_saved = bool(db_conn)
        self.name = name
        logging.config.dictConfig({"version": 1, "disable_existing_loggers": True})
        self.logger = logging.getLogger(name)

        log_format = "%(asctime)s [%(levelno)s] %(appname)s %(uuid)s %(message)s"  # Updated log format
        log_level_str = os.environ.get("LOG_LEVEL", "20")
        log_level = int(log_level_str) if log_level_str.isdigit() else logging.INFO
        hdlr = None
        if not self.logger.handlers:
            hdlr = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(log_format)
            hdlr.setFormatter(formatter)
            self.logger.addHandler(hdlr)
        else:
            for handler in self.logger.handlers:
                handler.setFormatter(logging.Formatter(log_format))

        self.logger.setLevel(log_level)
        self.logger.addFilter(ExcludeAsyncioTestCaseFilter())
        self.uuid = self.new_uuid()
        self.info(f"Logger Iniciado. Level: {log_level}")

    def __save_log_on_database(self, message: str, log_level: int) -> None:
        """
        Salva o log no banco de dados.

        Args:
            message (str): A mensagem de log.
            log_level (int): O nível do log.

        Returns:
            None
        """
        if self.is_data_saved:
            format_date = self.format_date(datetime.datetime.now())
            log_query = {
                "log_level": log_level,
                "timestamp": format_date,
                "app_name": self.name,
                "message": message,
                "uuid": self.uuid,
                "log_line": f"{format_date} [{log_level}] {self.name} {self.uuid} {message}"
            }
            self.db.create_document(log_query, container=self.name)

    def new_uuid(self):
        """
        Gera um novo UUID.

        Returns:
            str: O UUID gerado.
        """
        self.uuid = str(uuid4())
        return self.uuid

    @staticmethod
    def format_date(item):
        """
        Formata um item de data/hora.

        Args:
            item: O item a ser formatado.

        Returns:
            str: O item formatado.
        """
        if isinstance(item, (datetime.date, datetime.datetime)):
            return item.isoformat()
        return item

    def log(self, level, message, **kwargs):
        """
        Registra uma mensagem de log.

        Args:
            level (str): O nível do log.
            message: A mensagem a ser registrada.
            **kwargs: Outros argumentos opcionais.

        Returns:
            None
        """
        message_json = json.dumps(message, ensure_ascii=False, sort_keys=True, default=self.format_date)
        log_kwargs = kwargs.copy()
        log_kwargs["extra"] = {
            "uuid": self.uuid,
            "appname": self.name
        }  # Add appname and UUID to the log record
        getattr(self.logger, level)(message_json, **log_kwargs)
        if self.is_data_saved:
            self.__save_log_on_database(message=message, log_level=level)

    def info(self, message, **kwargs):
        """
        Registra uma mensagem de log com nível INFO.

        Args:
            message: A mensagem a ser registrada.
            **kwargs: Outros argumentos opcionais.

        Returns:
            None
        """
        self.log("info", message, **kwargs)

    def warning(self, message, **kwargs):
        """
        Registra uma mensagem de log com nível WARNING.

        Args:
            message: A mensagem a ser registrada.
            **kwargs: Outros argumentos opcionais.

        Returns:
            None
        """
        self.log("warning", message, **kwargs)

    def success(self, message, **kwargs):
        """
        Registra uma mensagem de log com nível INFO (sinônimo de sucesso).

        Args:
            message: A mensagem a ser registrada.
            **kwargs: Outros argumentos opcionais.

        Returns:
            None
        """
        self.log("info", message, **kwargs)

    def error(self, message, **kwargs):
        """
        Registra uma mensagem de log com nível ERROR.

        Args:
            message: A mensagem a ser registrada.
            **kwargs: Outros argumentos opcionais.

        Returns:
            None
        """
        self.log("error", message, **kwargs)

    def critical(self, message, **kwargs):
        """
        Registra uma mensagem de log com nível CRITICAL.

        Args:
            message: A mensagem a ser registrada.
            **kwargs: Outros argumentos opcionais.

        Returns:
            None
        """
        self.log("critical", message, **kwargs)

    def debug(self, message, **kwargs):
        """
        Registra uma mensagem de log com nível WARNING.

        Args:
            message: A mensagem a ser registrada.
            **kwargs: Outros argumentos opcionais.

        Returns:
            None
        """
        self.log("debug", message, **kwargs)
