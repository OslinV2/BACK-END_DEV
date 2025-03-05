import msal
import requests

class EmailMsal:

    def __init__(self, client_id, client_secret, tenant_id, user_id, username, password):
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.user_id = user_id
        self.username = username
        self.password = password
        self.scopes = ["https://graph.microsoft.com/.default"]
    
    def set_authority(self):
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
    
    def set_condidential_client_application(self):
        self.app = msal.ConfidentialClientApplication( client_id=self.client_id,
                                                       client_credential=self.client_secret,
                                                       authority=self.authority )

    def get_access_token(self):
        result = self.app.acquire_token_by_username_password( username = self.username,
                                                              password = self.password,
                                                              scopes = self.scopes )
        if not result:
            return (False, "")
        if "access_token" in result:
            return (True, result["access_token"])
    
    def get_emails_mailbox(self, access_token):
        userId = self.user_id
        headers= {'Authorization': 'Bearer ' + access_token}
        endpoint = f'https://graph.microsoft.com/v1.0/users/{userId}/mailFolders/Inbox/messages?$search="subject:Mannesoft Prime - Envio de Token"&$top=1&$select=bodyPreview'
        r = requests.get(endpoint,
                    headers={'Authorization': 'Bearer ' + access_token})
        if r.status_code == 200:
            return (True, r.json())
        else:
            return (False, r)