"""Classe para controle de tempo."""
import time

from .logger import Logger


class Timer:
    """Classe para controle de tempo de execução do código."""

    def __init__(self, logger: Logger) -> None:
        """
        Inicializa o timer.

        Args:
            logger (Logger): Objeto Logger para salvar logs.

        Returns:
            None
        """
        self.start_time: float = 0.0
        self.end_time: float = 0.0
        self.elapsed_time: float = 0.0
        self.logger = logger

    def __is_timer_started(self) -> bool:
        """Verifica se o temporizador foi iniciado.

        Verifica se o temporizador foi iniciado e retorna True se estiver em execução,
        False caso contrário.

        Returns:
            bool: True se o temporizador estiver em execução, False caso contrário.
        """
        message = "O timer não foi iniciado."
        if self.start_time == 0.0:
            self.logger.error(message=message)
            return False
        return True

    def start(self) -> None:
        """Inicia o contador de tempo."""
        if self.start_time != 0.0:
            self.logger.info("Timer já iniciado.")
            return

        self.start_time = time.time()
        self.logger.info("Timer iniciado.")

    def stop(self) -> None:
        """Para o contador de tempo."""
        if not self.__is_timer_started():
            return

        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time
        self.logger.info(f"Timer parado. Tempo decorrido: {self.elapsed_time:.2f} segundos.")

    def reset(self) -> None:
        """Reinicia o contador de tempo."""
        if not self.__is_timer_started():
            return

        self.start_time = 0.0
        self.end_time = 0.0
        self.elapsed_time = 0.0
        self.logger.info("Timer resetado.")

    def get_elapsed_time(self) -> None:
        """Retorna o tempo decorrido desde o inicio do contador de tempo."""
        if not self.__is_timer_started():
            return

        if self.end_time == 0.0:
            self.elapsed_time = time.time() - self.start_time

        self.logger.info(f"Tempo decorrido: {self.elapsed_time:.2f} segundos.")
