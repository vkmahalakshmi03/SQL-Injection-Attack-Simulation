from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), "../bank.db")

def get_db():
    return sqlite3.connect(DB_PATH)

@app.route("/")
def home():
    return """
    <h2>Bank Balance Lookup</h2>
    <form action="/balance" method="get">
        Enter Account Number: <input name="account" type="text"/>
        <input type="submit" value="Check Balance"/>
    </form>
    """

@app.route("/balance")
def get_balance():
    account = request.args.get("account", "")
    query = f"SELECT Account_Num, Description, Balance FROM Accounts WHERE Account_Num = {account}"
    conn = get_db()
    cursor = conn.cursor()
    try:
        statements = [s.strip() for s in query.split(";") if s.strip() and not s.strip().startswith("--")]
        for stmt in statements:
            cursor.execute(stmt)
        conn.commit()
        cursor.execute("SELECT Account_Num, Description, Balance FROM Accounts")
        all_accounts = cursor.fetchall()
        conn.close()
        return jsonify({
            "query_executed": query,
            "all_balances_after": all_accounts
        })
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e), "query_attempted": query})

if __name__ == "__main__":
    app.run(debug=True)
