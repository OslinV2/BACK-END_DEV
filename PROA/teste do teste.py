import requests
from bs4 import BeautifulSoup as bs4

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0'
}
re = requests.get('https://graph.microsoft.com/v1.0/users', headers=headers, verify=False)
soup = bs4(re.text, 'html.parser')
print(soup.prettify())

# from funcoesEmail import EmailMsal
# import datetime

# class v:
#     def __init__(self) -> None:
#         self.CLIENT_ID = ""
#         self.CLIENT_SECRET = ""
#         self.TENANT_ID = ""
#         self.USER_ID = "3af3b781-a88c-467b-98fd-85bd22365d31"
#         self.USERNAME_EMAIL = "carlens.oslin"
#         self.PASSWORD_EMAIL = "carlens.oslin@pucpr.br"

# variables = v()
# email = EmailMsal(variables.CLIENT_ID,
#                              variables.CLIENT_SECRET,
#                              variables.TENANT_ID,
#                              variables.USER_ID,
#                              variables.USERNAME_EMAIL,
#                              variables.PASSWORD_EMAIL)
# email.set_authority()
# email.set_condidential_client_application()
# access_token = email.get_access_token()

# endpoint = f'https://developer.microsoft.com/en-us/graph/graph-explorer'
# r = requests.get(endpoint,
#                 headers={'Authorization': 'Bearer ' + access_token[1]})