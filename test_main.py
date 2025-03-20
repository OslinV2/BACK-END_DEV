from fastapi import FastAPI, Query, HTTPException
from datetime import datetime, timedelta
import sqlite3
from typing import Optional, List, Dict
import uvicorn

app = FastAPI()

def get_db_connection():
    """Cria uma conexão com o banco de dados SQLite."""
    conn = sqlite3.connect("logs.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/logs/erro", response_model=List[Dict])
def get_logs_erro(
    start_date: Optional[str] = Query(None, description="Data inicial (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Data final (YYYY-MM-DD)"),
    log_type: str = Query("erro", description="Filtrar por tipo de log"),
):
    """Retorna logs filtrados pelo tipo e período informado."""
    if not start_date:
        start_date = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d")
    if not end_date:
        end_date = datetime.utcnow().strftime("%Y-%m-%d")

    try:
        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido. Use YYYY-MM-DD.")

    query = """
        SELECT * FROM logs WHERE tipo = ? AND timestamp BETWEEN ? AND ?
    """
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (log_type, start_date, end_date))
        logs = cursor.fetchall()

    if not logs:
        raise HTTPException(status_code=404, detail="Nenhum log encontrado no período especificado.")

    return [
        {"id": log["id"], "tipo": log["tipo"], "timestamp": log["timestamp"], "mensagem": log["mensagem"]}
        for log in logs
    ]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)