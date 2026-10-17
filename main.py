import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal

app = FastAPI(title="Helpdesk API")

class Ticket(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1, max_length=2000)

class StatusUpdate(BaseModel):
    status: Literal["open", "closed"]


def connect_db():
    conn = sqlite3.connect("tickets.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.on_event("startup")
def setup_db():
    conn = connect_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'open'
                CHECK (status IN ('open', 'closed'))
        )
    """)
    conn.commit()
    conn.close()

@app.post("/tickets", status_code=201)
def create_ticket(ticket: Ticket):
    conn = connect_db()
    cur = conn.execute(
        "INSERT INTO tickets (title, description) VALUES (?, ?)",
        (ticket.title, ticket.description)
    )
    conn.commit()

    row = conn.execute(
        "SELECT * FROM tickets WHERE id = ?", (cur.lastrowid,)
    ).fetchone()

    conn.close()
    return dict(row)

@app.get("/tickets")
def get_tickets():
    conn = connect_db()
    rows = conn.execute("SELECT * FROM tickets ORDER BY id").fetchall()
    conn.close()
    return [dict(row) for row in rows]


@app.patch("/tickets/{ticket_id}/status")
def update_status(ticket_id: int, ticket: StatusUpdate):
    conn = connect_db()
    cur = conn.execute(
        "UPDATE tickets SET status = ? WHERE id = ?",
        (ticket.status, ticket_id)
    )

    if cur.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Ticket not found")

    conn.commit()
    row = conn.execute(
        "SELECT * FROM tickets WHERE id = ?", (ticket_id,)
    ).fetchone()

    conn.close()
    return dict(row)

@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: int):
    conn = connect_db()
    cur = conn.execute(
        "DELETE FROM tickets WHERE id = ?", (ticket_id,)
    )

    if cur.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Ticket not found")

    conn.commit()
    conn.close()
    return {"message": "Ticket deleted successfully"}
