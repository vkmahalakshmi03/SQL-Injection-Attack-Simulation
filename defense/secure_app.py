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
    <h2>Bank Balance Lookup (Secure Version)</h2>
    <form action="/balance" method="get">
        Enter Account Number: <input name="account" type="text"/>
        <input type="submit" value="Check Balance"/>
    </form>
    """

@app.route("/balance")
def get_balance():
    account = request.args.get("account", "")

    # SECURE: parameterized query — input is treated as data, not code
    query = "SELECT Account_Num, Description, Balance FROM Accounts WHERE Account_Num = ?"

    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute(query, (account,))
        result = cursor.fetchone()
        conn.close()

        return jsonify({
            "query_template": query,
            "input_received": account,
            "result": result,
            "note": "Injection attempt has no effect — input is never executed as code."
        })

    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True, port=5001)
