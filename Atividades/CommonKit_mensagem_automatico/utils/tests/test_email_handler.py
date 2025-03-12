import unittest
from unittest.mock import patch, MagicMock

from utils.microsoft.msal_auth import MSALAuth
from utils.microsoft.email_integration import EmailIntegration

class TestGetCode(unittest.TestCase):
    """Classe de testes para a função get_code."""

    @patch('utils.microsoft.email_integration.EmailIntegration')
    @patch('utils.microsoft.msal_auth.MSALAuth')
    @patch('utils.email_handler.get_code')
    def test_get_code_success(self, mock_get_code, mock_EmailMsal, mock_EmailIntegration):
        """Testa o cenário em que o código é obtido com sucesso."""
        # Mock para a instância de EmailMsal
        mock_email_instance = MagicMock(spec=MSALAuth)
        mock_email_mailbox = MagicMock(spec=EmailIntegration)

        # Definindo o comportamento do mock
        mock_email_instance.get_token_by_user_and_password.return_value = 'TOKEN'
        mock_email_mailbox.get_emails_mailbox.return_value = {'value': [{'bodyPreview': 'Seu código de verificação é: 12345678'}]}

        mock_get_code.auth = mock_email_instance
        mock_get_code.email = mock_email_instance

        # Configurando o retorno da função de fábrica para retornar o mock
        mock_EmailMsal.return_value = mock_email_instance
        mock_EmailIntegration.return_value = mock_email_mailbox


        # Chamando a função que queremos testar
        code = EmailIntegration(MSALAuth()).get_code()

        # Verificando se o código foi obtido corretamente
        self.assertEqual(code, '12345678')

    @patch('utils.microsoft.msal_auth.MSALAuth')
    def test_get_code_no_code_found(self, mock_EmailMsal):
        """Testa o cenário em que nenhum código é encontrado."""
        # Mock para a instância de EmailMsal
        mock_email_instance = MagicMock(spec=MSALAuth)

        # Definindo o comportamento do mock
        mock_email_instance.get_token_by_user_and_password.return_value = 'TOKEN'
        mock_email_instance.get_emails_mailbox.return_value = {'value': [{'bodyPreview': 'Email de teste sem código'}]}

        # Configurando o retorno da função de fábrica para retornar o mock
        mock_EmailMsal.return_value = mock_email_instance

        # Chamando a função que queremos testar
        code = get_code()

        # Verificando se o código retornado é None
        self.assertEqual(code, "")

    @patch('utils.microsoft.msal_auth.MSALAuth')
    def test_get_code_exception(self, mock_EmailMsal):
        """Testa o cenário em que ocorre uma exceção durante a obtenção do código."""
        # Mock para a instância de EmailMsal
        mock_email_instance = MagicMock(spec=MSALAuth)

        # Definindo o comportamento do mock para lançar uma exceção
        # TODO - get_access_token pode estourar exceção quando as credencias passadas forem incorretas.
        mock_email_instance.get_token_by_user_and_password.side_effect = Exception('Erro ao obter token')

        # Configurando o retorno da função de fábrica para retornar o mock
        mock_EmailMsal.return_value = mock_email_instance

        # Chamando a função que queremos testar e verificando se uma exceção é lançada
        with self.assertRaises(Exception):
            get_code()
