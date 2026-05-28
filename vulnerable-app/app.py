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

    # VULNERABLE: input inserted directly into query string
    query = f"SELECT Account_Num, Description, Balance FROM Accounts WHERE Account_Num = {account}"

    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.executescript(query)
        cursor.execute(f"SELECT Account_Num, Description, Balance FROM Accounts WHERE Account_Num = {account}")
        result = cursor.fetchone()
        conn.commit()
        conn.close()

        # Show all balances after query runs (so you can see the change)
        conn2 = get_db()
        c2 = conn2.cursor()
        c2.execute("SELECT Account_Num, Description, Balance FROM Accounts")
        all_accounts = c2.fetchall()
        conn2.close()

        return jsonify({
            "query_executed": query,
            "result": result,
            "all_balances_after": all_accounts
        })

    except Exception as e:
        conn.close()
        return jsonify({"error": str(e), "query_attempted": query})

if __name__ == "__main__":
    app.run(debug=True)
