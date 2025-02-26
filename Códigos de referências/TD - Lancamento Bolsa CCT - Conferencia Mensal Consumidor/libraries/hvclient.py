import os
import hvac
from hvac.exceptions import InvalidPath
from requests.exceptions import ConnectionError


class Hvclient():

    def __init__(self):
        self.client = self.__client()

    def get_credentials(self, secrets_path):
        return self.__get_secrets(secrets_path)

    def __client(self):
        token = os.environ.get('HCV_TOKEN')
        try:
            client = hvac.Client(
                token=token
            )
            if not client.is_authenticated():
                raise ValueError('Verifique o token configurado na variável de ambiente')
            return client
        except ConnectionError as e:
            msg = 'Verifique se o Vault está em execução e se as variáveis de'\
                'ambiente, descritas na documentação dessa'\
                'Lib, estão configuradas.'
            raise f'{e} \n\n{msg}'

    def __get_secrets(self, path):
        try:
            hvreponse = \
                self.client.secrets.kv.read_secret_version(path=path)
            return hvreponse['data']['data']
        except InvalidPath as e:
            raise e
        except KeyError as e:
            raise e
