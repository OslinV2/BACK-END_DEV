import re
from .microsoft.email_integration import EmailIntegration
from .microsoft.msal_auth import MSALAuth


"""
a função getCode tem por objetivo resgatar códigos de verificação de e-mails enviados pelo prime.
para realizar automaticamente a verificação de duas etapas do prime, assim, não é necessária a intervenção humana.
facilitando assim, a automatização do processo.
"""

class EmailHandler:

    def __init__(self, auth: MSALAuth=None) -> None:
        self.auth = auth
        self.email = EmailIntegration(auth=auth)
        pass

    def get_code(self) -> str:
        """
        Obtém o código a partir do corpo de um email.

        Retorna o código de 8 dígitos encontrado no corpo do primeiro email da caixa de correio.
        Caso nenhum código seja encontrado, retorna None.

        Raises:
            Exception: Se ocorrer algum erro durante a obtenção do código.

        Returns:
            str: O código de 8 dígitos encontrado no corpo do email.
        """
        try:
            token = self.auth.get_token_by_user_and_password()
            retorno = self.email.get_emails_prime_token(token)
            mensagem_body = retorno['value'][0]['bodyPreview']
            return re.search('[0-9]{8}', mensagem_body).group()
        except Exception as e:
            print(e)
            return ""
    