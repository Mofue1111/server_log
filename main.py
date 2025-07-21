# logger/main.py
from fastapi import FastAPI, Request
import sqlite3
from datetime import datetime
import uvicorn

app = FastAPI()

def create_logs_table():
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        user TEXT,
        action TEXT,
        level TEXT
    )
    """)
    conn.commit()
    conn.close()

create_logs_table()
@app.get("/")
async def main_action(request: Request):
     return {"answer": "You are visited on my server!!!"}


@app.post("/log/")
async def log_action(request: Request):
    data = await request.json()
    user = data.get("user")
    action = data.get("action")
    level = data.get("level")
    timestamp = datetime.now().isoformat()

    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (timestamp, user, action, level) VALUES (?, ?, ?, ?)",
                   (timestamp, user, action, level))
    conn.commit()
    conn.close()
    return {"status": "ok"}

uvicorn.run(app)