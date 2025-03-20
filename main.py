from fastapi import FastAPI, Query, HTTPException
from datetime import datetime, timedelta, timezone
import sqlite3
import uvicorn

DB_NAME = "logs.db"

app = FastAPI()

def get_db_connection():
    """Cria uma conexão com o banco de dados."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def parse_date(date_str: str) -> str:
    """Tenta converter automaticamente `DD-MM-YYYY` ou `YYYY-MM-DD` para `YYYY-MM-DD`."""
    possible_formats = ["%d-%m-%Y", "%Y-%m-%d"]
    for fmt in possible_formats:
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    raise HTTPException(status_code=400, detail="Formato de data inválido. Use DD-MM-YYYY ou YYYY-MM-DD.")

@app.get("/logs/erro")
def get_logs_erro(
    start_date: str = Query(None, description="Data inicial (DD-MM-YYYY ou YYYY-MM-DD)"),
    end_date: str = Query(None, description="Data final (DD-MM-YYYY ou YYYY-MM-DD)"),
    log_type: str = Query("erro", description="Tipo de log a filtrar"),
):
    """Retorna logs filtrados pelo tipo e período informado."""

    # Se datas não forem fornecidas, assume o intervalo da última semana
    if start_date is None:
        start_date = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%d")
    else:
        start_date = parse_date(start_date)

    if end_date is None:
        end_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    else:
        end_date = parse_date(end_date)

    if start_date > end_date:
        raise HTTPException(status_code=400, detail="A data inicial não pode ser maior que a data final.")

    conn = get_db_connection()
    cursor = conn.cursor()

    query = '''
        SELECT * FROM logs 
        WHERE tipo = ? 
        AND DATE(timestamp) BETWEEN DATE(?) AND DATE(?)
    '''
    cursor.execute(query, (log_type, start_date, end_date))
    logs = cursor.fetchall()
    conn.close()

    if not logs:
        raise HTTPException(status_code=404, detail="Nenhum log encontrado no período especificado.")

    return [
        {
            "id": log["id"],
            "tipo": log["tipo"],
            "timestamp": datetime.fromisoformat(log["timestamp"]).strftime("%d-%m-%Y %H:%M:%S"),
            "mensagem": log["mensagem"]
        }
        for log in logs
    ]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
