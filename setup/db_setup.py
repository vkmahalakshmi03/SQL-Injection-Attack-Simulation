import sqlite3

conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS Customers (
    SSN TEXT PRIMARY KEY,
    Name TEXT,
    Address TEXT
);

CREATE TABLE IF NOT EXISTS Customer_Account (
    Customer TEXT,
    Account INTEGER
);

CREATE TABLE IF NOT EXISTS Accounts (
    Account_Num INTEGER PRIMARY KEY,
    Description TEXT,
    Balance REAL
);

INSERT OR IGNORE INTO Customers VALUES ('123-45-6789', 'John Doe', '4400 University Dr, Fairfax, VA');
INSERT OR IGNORE INTO Customers VALUES ('987-65-4321', 'Homer Simpson', '10 First St, Springfield, OH');

INSERT OR IGNORE INTO Customer_Account VALUES ('123-45-6789', 256101);
INSERT OR IGNORE INTO Customer_Account VALUES ('123-45-6789', 256202);
INSERT OR IGNORE INTO Customer_Account VALUES ('987-65-4321', 256304);

INSERT OR IGNORE INTO Accounts VALUES (256101, 'Checking', 10000.00);
INSERT OR IGNORE INTO Accounts VALUES (256202, 'Savings', 12000.00);
INSERT OR IGNORE INTO Accounts VALUES (256304, 'Checking', 10300.00);
""")

conn.commit()
conn.close()
print("Database created: bank.db")
print("Accounts seeded successfully.")
