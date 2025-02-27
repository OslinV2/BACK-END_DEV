import os
from dotenv import load_dotenv
from commonKit.utils.criptador import cypher

load_dotenv()

USER_EMAIL = os.environ.get("USER_EMAIL")
PASSWORD = os.environ.get("PASSWORD")
USER_ID = os.environ.get("USER_ID")
TEAM_ID = os.environ.get("TEAM_ID")
CHANNEL_ID = os.environ.get("CHANNEL_ID")
TENANT_ID = os.environ.get("TENANT_ID")

encrypted_user_email = cypher(USER_EMAIL)
encrypted_password = cypher(PASSWORD)
encrypted_user_id = cypher(USER_ID)
encrypted_team_id = cypher(TEAM_ID)
encrypted_channel_id = cypher(CHANNEL_ID)
encrypted_tenant_id = cypher(TENANT_ID)

print(f"Encrypted USER_EMAIL: {encrypted_user_email}")
print(f"Encrypted PASSWORD: {encrypted_password}")
print(f"Encrypted USER_ID: {encrypted_user_id}")
print(f"Encrypted TEAM_ID: {encrypted_team_id}")
print(f"Encrypted CHANNEL_ID: {encrypted_channel_id}")
print(f"Encrypted TENANT_ID: {encrypted_tenant_id}")
