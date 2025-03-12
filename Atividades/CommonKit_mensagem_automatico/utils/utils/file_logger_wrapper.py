from datetime import datetime

from .logger import Logger


class FileLoggerWrapper:
    """
    Um wrapper para a classe Logger que adiciona funcionalidade de persistência de logs em um arquivo.

    A classe encapsula um objeto Logger e garante que cada mensagem de log também seja salva 
    em um arquivo especificado.

    Attributes:
        log_file (str): O caminho do arquivo onde os logs serão armazenados.
        logger (Logger): Instância da classe Logger original.
    """

    def __init__(self, app_name: str, log_file=str):
        """
        Inicializa o FileLoggerWrapper com um arquivo de log específico.

        Args:
            log_file (str): O caminho do arquivo de log. Padrão é "app.log".
        """
        self.logger = Logger(name=app_name)  # Instancia o Logger original
        self.log_file = log_file


    def _save_to_file(self, level, message):
        """
        Salva uma mensagem de log no arquivo especificado.

        Args:
            level (str): O nível do log (INFO, ERROR, DEBUG).
            message (str): A mensagem de log a ser salva.
        """
        now = datetime.now()
        
        with open(self.log_file, "a", encoding="utf-8") as file:
            file.write(f"{now} - {level} - {message}\n")

    def info(self, message):
        """
        Registra uma mensagem de informação no logger e no arquivo.

        Args:
            message (str): A mensagem a ser registrada.
        """
        self.logger.info(message)  # Chama o método original
        self._save_to_file("INFO", message)  # Salva no arquivo

    def error(self, message):
        """
        Registra uma mensagem de erro no logger e no arquivo.

        Args:
            message (str): A mensagem de erro a ser registrada.
        """
        self.logger.error(message)
        self._save_to_file("ERROR", message)

    def debug(self, message):
        """
        Registra uma mensagem de depuração no logger e no arquivo.

        Args:
            message (str): A mensagem de depuração a ser registrada.
        """
        self.logger.debug(message)
        self._save_to_file("DEBUG", message)
