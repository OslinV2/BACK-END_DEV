import sqlite3
from datetime import datetime, timedelta
import random

DB_NAME = "logs.db"

LOG_TIPOS = ["erro", "aviso", "informação", "debug"]
MENSAGENS_ERRO = [
    "Falha ao acessar banco de dados",
    "Dados não encontrados",
    "Conexão perdida",
    "Falha ao tentar gravar no banco",
    "Erro interno do servidor",
    "Erro na autenticação do usuário",
    "Erro ao processar solicitação de dados",
    "Erro ao gerar relatório",
    "Erro de permissão",
    "Log de debug ativado",
    "Falha ao enviar e-mail",
    "Erro ao acessar o arquivo de log",
    "Servidor em manutenção",
    "Requisição mal formatada",
    "Erro de sintaxe em SQL",
    "Falha na comunicação com API externa",
    "Token de autenticação expirado",
    "Recurso não encontrado",
    "Falha ao carregar configurações",
    "Erro na criptografia de dados",
]

def create_db():
    """Cria o banco de dados e a tabela `logs` do zero."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS logs")  # Remove a tabela existente
        cursor.execute('''
            CREATE TABLE logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                mensagem TEXT NOT NULL
            )
        ''')
        conn.commit()
        print("Banco de dados criado com sucesso!")

def generate_logs(n=50):
    """Gera `n` logs aleatórios entre 01/01/2025 e 31/03/2025."""
    logs = []
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 3, 31)
    delta = (end_date - start_date).days

    for _ in range(n):
        random_days = random.randint(0, delta)  # Escolhe um dia aleatório entre jan e mar
        random_time = timedelta(
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59),
        )
        timestamp = (start_date + timedelta(days=random_days) + random_time).strftime("%Y-%m-%d %H:%M:%S")  # Mantém formato SQLite
        
        tipo = random.choices(LOG_TIPOS, weights=[70, 15, 10, 5])[0]  # 70% erros
        mensagem = random.choice(MENSAGENS_ERRO) if tipo == "erro" else "Mensagem genérica"

        logs.append((tipo, timestamp, mensagem))

    return logs

def insert_logs():
    """Insere logs aleatórios no banco de dados."""
    logs = generate_logs(50)
    
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.executemany("INSERT INTO logs (tipo, timestamp, mensagem) VALUES (?, ?, ?)", logs)
        conn.commit()

    print("Banco de dados populado com 50 logs!")

if __name__ == "__main__":
    create_db()
    insert_logs()
