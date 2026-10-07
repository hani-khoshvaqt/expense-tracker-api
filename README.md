# Expense Tracker API

A simple REST API for tracking personal expenses, built with Flask and SQLite.

## Features
- Add, list, and delete expenses
- Spending summary (total and per category)
- Input validation with clear error messages

## Setup
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
The server runs at http://127.0.0.1:5000

## Endpoints
| Method | Endpoint | Description |
| -------|----------|-------------|
| POST | /expenses | Add an expense |
| GET | /expenses | List all expenses (newest first) |
| DELETE | /expenses/<id> | Delete an expense |
| GET | /summary | Total and per-category totals |

## Example
```
POST /expenses
{"title": "Lunch", "amount": 12.5, "category": "food", "date": "2026-10-05"}
```

## Tech
Python, Flask, SQLite