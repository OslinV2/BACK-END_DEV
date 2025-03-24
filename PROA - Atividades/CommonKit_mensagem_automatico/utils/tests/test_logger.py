import unittest
import logging
import os
from utils.logger import Logger

os.environ["LOG_LEVEL"] = "10"

class TestLogger(unittest.TestCase):
    """Classe de testes para a classe Logger."""

    def setUp(self):
        """Configurações a serem executadas antes de cada teste."""
        self.logger = Logger()
        self.logger.logger.setLevel(logging.DEBUG)

    def test_log_debug(self):
        """Testa o log debug."""
        with self.assertLogs(self.logger.logger, level="DEBUG") as log:
            self.logger.debug("Teste log debug")
        self.assertIn("Teste log debug", log.output[0])

    def test_log_info(self):
        """Testa o log info."""
        with self.assertLogs(self.logger.logger, level="INFO") as log:
            self.logger.info("Teste log info")
        self.assertIn("Teste log info", log.output[0])

    def test_log_warning(self):
        """Testa o log warning."""
        with self.assertLogs(self.logger.logger, level="WARNING") as log:
            self.logger.warning("Teste log warning")
        self.assertIn("Teste log warning", log.output[0])

    def test_log_error(self):
        """Testa o log error."""
        with self.assertLogs(self.logger.logger, level="ERROR") as log:
            self.logger.error("Teste log error")
        self.assertIn("Teste log error", log.output[0])

    def test_log_critical(self):
        """Testa o log critical."""
        with self.assertLogs(self.logger.logger, level="CRITICAL") as log:
            self.logger.critical("Teste log critical")
        self.assertIn("Teste log critical", log.output[0])
