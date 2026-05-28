# SQL Injection Attack Simulation — Banking Environment

A hands-on lab simulating a SQL injection attack on a vulnerable banking application.
Built to understand how unsanitized input leads to unauthorized data manipulation,
and how parameterized queries eliminate the risk at the source.

---

## Scenario

A banking portal allows users to look up their account balance by entering an account number.
The backend query concatenates user input directly into SQL — no validation, no sanitization.

An attacker exploits this to inject additional SQL statements, transferring $500 from
another customer's account into their own — with no credentials, no authorization,
and no trace in the app logic.

---

## Environment

| Tool | Version |
|------|---------|
| Python | 3.x |
| Flask | 2.x |
| SQLite3 | Built-in |

---

## Repo Structure

    sql-injection-lab/
    ├── README.md
    ├── setup/
    │   └── db_setup.py
    ├── vulnerable-app/
    │   └── app.py
    ├── attacks/
    │   └── injection_payload.sql
    ├── defense/
    │   └── secure_app.py
    └── screenshots/
        └── attack_demo.png

---

## How to Run

**1. Install dependencies**

    pip install flask

**2. Set up the database**

    python setup/db_setup.py

**3. Run the vulnerable app**

    python vulnerable-app/app.py

Visit: http://localhost:5000

**4. Test the injection**

Enter this entire string in the account number field:

    256304; UPDATE Accounts SET Balance = Balance - 500 WHERE Account_Num = 256304; UPDATE Accounts SET Balance = Balance + 500 WHERE Account_Num = 256101; --

Check `all_balances_after` in the JSON response — the transfer executed.

**5. Run the secure version**

    python defense/secure_app.py

Run the same payload. Input is treated as data — no transfer occurs.

---

## Attack Breakdown

| | Before | After |
|---|---|---|
| John Doe (256101) | $10,000 | $10,500 |
| Homer Simpson (256304) | $10,300 | $9,800 |

Full payload documented in `/attacks/injection_payload.sql`

---

## Defense

Switching from string interpolation to a parameterized query is the fix.

Vulnerable:

    query = f"SELECT Balance FROM Accounts WHERE Account_Num = {account}"

Secure:

    query = "SELECT Balance FROM Accounts WHERE Account_Num = ?"
    cursor.execute(query, (account,))

The database engine receives the input as a value — it cannot be interpreted as SQL code.

---

## Relevance to Security Operations

Understanding injection mechanics matters beyond just web app testing.
SOC analysts use this knowledge for:

- Writing SIEM detection rules for stacked query patterns
- Identifying WAF bypass attempts in web traffic logs
- Reviewing application logs for anomalous query structures
