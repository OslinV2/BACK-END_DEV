from ...CommonKit_mensagem_automatico.commonKit.utils.db_connect import DBConnect
from fastapi import FastAPI
from typing import Union
import requests

app = FastAPI()

# Criar uma instância de DBConnect e abrir a conexão
connection = DBConnect().open_connection("mongodb://localhost:27017")

db = connection["Restornos_logs"]
usuarios = db["collections"]
