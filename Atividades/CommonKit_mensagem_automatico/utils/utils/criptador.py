"""Module criptador.py"""

from base64 import b64decode
import os
from cryptography.fernet import Fernet

def cypher(credential):
    """
    Criptografa uma credencial usando uma chave de criptografia fornecida pelo ambiente.

    Parâmetros:
    credential (str): A credencial a ser criptografada.

    Retorna:
    bytes: A credencial criptografada.
    """
    key = os.environ.get('COORDINATOR')
    real_key = b64decode(key)
    crypto_criteria = Fernet(real_key)
    cyphered = crypto_criteria.encrypt(credential.encode('utf8'))
    return cyphered

def decypher(credential=None):
    """
    Descriptografa a credencial fornecida usando uma chave secreta.

    Args:
        credential (bytes): A credencial criptografada a ser descriptografada.

    Returns:
        O valor descriptografado da credencial.
    """
    key = os.environ.get('COORDINATOR')
    real_key = b64decode(key)
    crypto_criteria = Fernet(real_key)
    return crypto_criteria.decrypt(credential).decode('utf8')
