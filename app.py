from flask import Flask, request, jsonify
from database import get_connection, init_db

app = Flask(__name__)
init_db()

@app.route("/")
def home():
    return {"message": "Expense Tracker API is running"}


@app.route("/expenses", methods=["POST"])
def add_expense():
    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON body required"}), 400
    
    required = ["title", "amount", "category", "date"]
    missing = [f for f in required if f not in data or data[f] in {"", None}]
    if missing:
        return jsonify({"error": f"Missing fields: {','.join(missing)}"}), 400
    
    if not isinstance(data["amount"], (int, float)) or data["amount"] <= 0:
        return jsonify({"error": "amount must be a positive number"}), 400
    
    title = data["title"]
    amount = data["amount"]
    category = data["category"]
    date = data["date"]
    
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO expenses (title, amount, category, date) VALUES (?,?,?,?)",
        (title, amount, category, date)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    
    return jsonify({
        "id": new_id,
        "title": title,
        "amount": amount,
        "category": category,
        "date": date
    }), 201
    
@app.route("/expenses", methods=["GET"])
def get_expenses():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM expenses ORDER BY date DESC"). fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route("/expenses/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    conn = get_connection()
    cursor = conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    if deleted == 0:
        return jsonify({"error": "Expense not found"}), 404
    return jsonify({"message": "Deleted"}), 200

@app.route("/summary", methods=["GET"])
def get_summary():
    conn = get_connection()
    total = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses"). fetchone()[0]
    rows = conn.execute(
        "SELECT category, SUM(amount) AS total fROM expenses GROUP BY category"
    ).fetchall()
    conn.close()
    return jsonify({"total": total, "by_category": {r["category"]: r["total"] for r in rows}})


if __name__ == "__main__":
    app.run(debug=True)