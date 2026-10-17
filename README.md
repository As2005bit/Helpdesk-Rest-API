# Helpdesk REST API

A REST API for managing support tickets using FastAPI and SQLite.

## Features
- Create support tickets
- View all tickets
- Update ticket status
- Delete tickets

## Tech Stack
- Python
- FastAPI
- SQLite

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/tickets` | Create a ticket |
| GET | `/tickets` | View all tickets |
| PATCH | `/tickets/{ticket_id}/status` | Update ticket status |
| DELETE | `/tickets/{ticket_id}` | Delete a ticket |

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the server:

```bash
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs` to explore and test the API.
