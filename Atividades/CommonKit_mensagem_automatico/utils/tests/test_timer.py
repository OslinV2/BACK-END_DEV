import time
import unittest
from unittest.mock import MagicMock
from utils.timer import Timer

class TestTimer(unittest.TestCase):
    """Classe de testes para a classe Timer."""

    def setUp(self):
        """Configurações a serem executadas antes de cada teste."""
        self.logger_mock = MagicMock()
        self.timer = Timer(self.logger_mock)

    def test_start(self):
        """Testa o método start."""
        self.timer.start()
        self.assertTrue(self.timer.start_time != 0.0)

    def test_stop(self):
        """Testa o método stop."""
        self.timer.start()
        self.timer.stop()
        self.assertTrue(self.timer.end_time != 0.0)

    def test_reset(self):
        """Testa o método reset."""
        self.timer.start()
        self.timer.reset()
        self.assertTrue(self.timer.start_time == 0.0)
        self.assertTrue(self.timer.end_time == 0.0)
        self.assertTrue(self.timer.elapsed_time == 0.0)

    def test_get_elapsed_time(self):
        """Testa o método get_elapsed_time."""
        self.timer.reset()
        self.timer.start()
        time.sleep(1.0)
        self.timer.stop()
        self.timer.get_elapsed_time()
        self.logger_mock.info.assert_called_with(f"Tempo decorrido: 1.00 segundos.")

if __name__ == '__main__':
    unittest.main()
