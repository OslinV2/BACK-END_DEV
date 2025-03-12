import base64
import unittest
from cryptography.fernet import Fernet
from unittest.mock import patch

from utils.criptador import cypher, decypher

class TestCriptador(unittest.TestCase):
    """Classe de testes para o criptador.

    o @patch é usado para substituir a função os.environ.get, que é responsável por recuperar variáveis de ambiente, por um objeto mock. 
    Isso nos permite controlar o valor retornado por os.environ.get dentro do teste, garantindo que a função cypher ou decypher seja 
    testada com o ambiente configurado exatamente como desejamos para o teste específico.

    """

    @patch('utils.criptador.os.environ.get')
    def test_cypher_valid_key(self, mock_get):
        """Testa o método de criptografia com uma chave válida."""
        # Gerando uma chave válida
        fernet_key = Fernet.generate_key()
        base64_key = base64.b64encode(fernet_key)
        mock_get.return_value = base64_key  

        # Criando um mock para a credencial
        credential = 'senha123'

        # Chamando o método que queremos testar
        cyphered = cypher(credential)

        # Verificando se a função de criptografia foi chamada corretamente
        self.assertIsNotNone(cyphered)

    @patch('utils.criptador.os.environ.get')
    def test_cypher_invalid_key(self, mock_get):
        """Testa o método de criptografia com uma chave inválida."""
        # Definindo o comportamento do mock para a chave de ambiente
        mock_get.return_value = 'ChaveInvalida'

        # Criando um mock para a credencial
        credential = 'senha123'

        # Verificando se a função de criptografia lança um ValueError com uma chave inválida
        with self.assertRaises(ValueError):
            cypher(credential)

    @patch('utils.criptador.os.environ.get')
    def test_decypher(self, mock_get):
        """Testa o método de descriptografia."""
        # Gerando uma chave válida
        fernet_key = Fernet.generate_key()
        base64_key = base64.b64encode(fernet_key)
        mock_get.return_value = base64_key

        # Criando um mock para a credencial
        credential = 'senha123'

        # Criptografando a credencial
        cyphered = cypher(credential)

        # Descriptografando a credencial
        decrypted = decypher(cyphered)

        # Verificando se a função de descriptografia retorna o valor correto
        self.assertEqual(decrypted, credential)
