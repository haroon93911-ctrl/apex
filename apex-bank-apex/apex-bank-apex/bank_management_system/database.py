"""
database.py - Database Management for Bank Management System
Comprehensive SQLite operations for both Customer and Bank Manager suites:
- Auto-creating and managing tables (accounts, transactions, admins, login_history)
- Login history logging for both successful and failed attempts (Customer & Manager)
- Advanced manager analytics (vault reserves, inflows, outflows, averages, security metrics)
- Detailed customer queries (with calculated total deposits and withdrawals per customer)
- Global transaction ledger and security audit logs
- Account editing, manager deposits/withdrawals, account deletion
"""

import sqlite3
import random
from datetime import datetime
import os

# Database file location
DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(DB_DIR, "bank.db")


def get_connection():
    """Create and return a SQLite database connection with Row dict factory."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Initializes the SQLite database and creates tables if they don't exist.
    Also handles migrations and seeds default Bank Manager account.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Accounts Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            account_number TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            pin TEXT NOT NULL,
            balance REAL NOT NULL DEFAULT 0.0,
            created_at TEXT NOT NULL
        )
    """)

    # 2. Transactions Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number TEXT NOT NULL,
            transaction_type TEXT NOT NULL,
            amount REAL NOT NULL,
            balance_after REAL NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (account_number) REFERENCES accounts (account_number)
        )
    """)

    # 3. Admins / Bank Managers Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'Bank Manager'
        )
    """)

    # 4. Login History Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS login_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_identifier TEXT NOT NULL,
            user_name TEXT NOT NULL,
            role TEXT NOT NULL,
            status TEXT NOT NULL,
            failure_reason TEXT,
            timestamp TEXT NOT NULL
        )
    """)

    # Migration check for admins.role column
    cursor.execute("PRAGMA table_info(admins)")
    admin_cols = [col[1] for col in cursor.fetchall()]
    if "role" not in admin_cols:
        cursor.execute("ALTER TABLE admins ADD COLUMN role TEXT NOT NULL DEFAULT 'Senior Executive Manager'")

    # Seed Default Bank Manager if not exists
    cursor.execute("SELECT 1 FROM admins WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO admins (username, password, name, role)
            VALUES (?, ?, ?, ?)
        """, ("admin", "admin123", "Chief Branch Manager", "Senior Executive Manager"))
    else:
        cursor.execute("UPDATE admins SET role = 'Senior Executive Manager' WHERE username = 'admin' AND (role IS NULL OR role = '')")

    conn.commit()
    conn.close()


def generate_unique_account_number():
    """Generates a unique 6-digit account number."""
    conn = get_connection()
    cursor = conn.cursor()

    while True:
        acc_num = str(random.randint(100000, 999999))
        cursor.execute("SELECT 1 FROM accounts WHERE account_number = ?", (acc_num,))
        if not cursor.fetchone():
            conn.close()
            return acc_num


def log_login_attempt(user_identifier, user_name, role, status, failure_reason=None):
    """
    Records a login attempt (successful or failed) in the login_history table.
    """
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO login_history (user_identifier, user_name, role, status, failure_reason, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (str(user_identifier), str(user_name), str(role), str(status), failure_reason, now_str))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error logging login attempt: {e}")
    finally:
        conn.close()


def get_login_history(limit=150, search_query=None, filter_role=None, filter_status=None):
    """
    Retrieves global login audit history with optional search and filters.
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT id, user_identifier, user_name, role, status, failure_reason, timestamp FROM login_history"
    conditions = []
    params = []

    if filter_role and filter_role != "All":
        conditions.append("role = ?")
        params.append(filter_role)

    if filter_status and filter_status != "All":
        conditions.append("status = ?")
        params.append(filter_status)

    if search_query and search_query.strip():
        q = f"%{search_query.strip()}%"
        conditions.append("(user_identifier LIKE ? OR user_name LIKE ?)")
        params.extend([q, q])

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY id DESC LIMIT ?"
    params.append(limit)

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    conn.close()

    logs = []
    for r in rows:
        logs.append({
            "id": r["id"],
            "user_identifier": r["user_identifier"],
            "user_name": r["user_name"],
            "role": r["role"],
            "status": r["status"],
            "failure_reason": r["failure_reason"] or "N/A",
            "timestamp": r["timestamp"]
        })
    return logs


def get_customer_last_login(account_number):
    """Retrieves timestamp of the previous successful login for a customer."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp FROM login_history
        WHERE user_identifier = ? AND role = 'Customer' AND status = 'SUCCESS'
        ORDER BY id DESC LIMIT 2
    """, (str(account_number),))

    rows = cursor.fetchall()
    conn.close()

    if len(rows) > 1:
        return rows[1]["timestamp"]  # Previous login before current
    elif len(rows) == 1:
        return rows[0]["timestamp"]
    return "First Session"


def create_account(name, phone, pin, initial_balance=0.0, custom_account_number=None):
    """Creates a new customer account."""
    name = name.strip()
    phone = phone.strip()
    pin = str(pin).strip()

    if not name:
        return False, "Customer Name cannot be empty.", None
    if not phone or not phone.isdigit() or len(phone) < 7:
        return False, "Please enter a valid phone number (digits only, at least 7 digits).", None
    if not pin or not pin.isdigit() or len(pin) != 4:
        return False, "Security PIN must be exactly 4 numeric digits.", None
    if initial_balance < 0:
        return False, "Initial deposit cannot be negative.", None

    conn = get_connection()
    cursor = conn.cursor()

    if custom_account_number and str(custom_account_number).strip():
        acc_num = str(custom_account_number).strip()
        cursor.execute("SELECT 1 FROM accounts WHERE account_number = ?", (acc_num,))
        if cursor.fetchone():
            conn.close()
            return False, f"Account number {acc_num} already exists.", None
    else:
        acc_num = generate_unique_account_number()

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        cursor.execute("""
            INSERT INTO accounts (account_number, name, phone, pin, balance, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (acc_num, name, phone, pin, float(initial_balance), now_str))

        if initial_balance > 0:
            cursor.execute("""
                INSERT INTO transactions (account_number, transaction_type, amount, balance_after, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (acc_num, "Initial Deposit", float(initial_balance), float(initial_balance), now_str))

        conn.commit()
        return True, "Account created successfully!", acc_num
    except sqlite3.Error as e:
        return False, f"Database error: {str(e)}", None
    finally:
        conn.close()


def authenticate(account_number, pin):
    """
    Authenticates a customer by Account Number and 4-digit PIN.
    Automatically records SUCCESS or FAILED in login_history.
    """
    acc_num = str(account_number).strip()
    pin = str(pin).strip()

    if not acc_num or not pin:
        log_login_attempt(acc_num or "Unknown", "Unknown", "Customer", "FAILED", "Empty account number or PIN")
        return False, "Account number and PIN are required."

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT account_number, name, phone, pin, balance, created_at
        FROM accounts
        WHERE account_number = ?
    """, (acc_num,))

    account = cursor.fetchone()
    conn.close()

    if not account:
        log_login_attempt(acc_num, "Unknown", "Customer", "FAILED", "Account number not found")
        return False, "Account number not found."

    if account["pin"] != pin:
        log_login_attempt(acc_num, account["name"], "Customer", "FAILED", "Incorrect 4-digit PIN")
        return False, "Incorrect 4-digit PIN."

    # Record successful login
    log_login_attempt(acc_num, account["name"], "Customer", "SUCCESS", "Authentication Verified")

    return True, {
        "account_number": account["account_number"],
        "name": account["name"],
        "phone": account["phone"],
        "pin": account["pin"],
        "balance": float(account["balance"]),
        "created_at": account["created_at"]
    }


def authenticate_admin(username, password):
    """
    Authenticates a Bank Manager.
    Automatically records SUCCESS or FAILED in login_history.
    """
    uname = str(username).strip()
    pwd = str(password).strip()

    if not uname or not pwd:
        log_login_attempt(uname or "Unknown", "Unknown", "Bank Manager", "FAILED", "Empty credentials")
        return False, "Manager username and password are required."

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT username, password, name, role
        FROM admins
        WHERE username = ?
    """, (uname,))

    admin = cursor.fetchone()
    conn.close()

    if not admin:
        log_login_attempt(uname, "Unknown", "Bank Manager", "FAILED", "Username not found")
        return False, "Manager username not found."

    if admin["password"] != pwd:
        log_login_attempt(uname, admin["name"], "Bank Manager", "FAILED", "Incorrect password")
        return False, "Incorrect password."

    log_login_attempt(uname, admin["name"], "Bank Manager", "SUCCESS", "Executive Access Granted")

    return True, {
        "username": admin["username"],
        "name": admin["name"],
        "role": admin["role"]
    }


def get_account(account_number):
    """Fetches full account record for a customer."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT account_number, name, phone, pin, balance, created_at
        FROM accounts
        WHERE account_number = ?
    """, (str(account_number).strip(),))

    account = cursor.fetchone()
    conn.close()

    if account:
        return {
            "account_number": account["account_number"],
            "name": account["name"],
            "phone": account["phone"],
            "pin": account["pin"],
            "balance": float(account["balance"]),
            "created_at": account["created_at"]
        }
    return None


def get_all_accounts_detailed(search_query=None, filter_balance=None):
    """Fetches all customer accounts with computed total deposits and withdrawals."""
    conn = get_connection()
    cursor = conn.cursor()

    base_query = """
        SELECT
            a.account_number,
            a.name,
            a.phone,
            a.pin,
            a.balance,
            a.created_at,
            COALESCE((SELECT SUM(amount) FROM transactions WHERE account_number = a.account_number AND transaction_type LIKE '%Deposit%'), 0.0) as total_deposited,
            COALESCE((SELECT SUM(amount) FROM transactions WHERE account_number = a.account_number AND transaction_type = 'Withdrawal'), 0.0) as total_withdrawn,
            COALESCE((SELECT COUNT(*) FROM transactions WHERE account_number = a.account_number), 0) as total_tx_count
        FROM accounts a
    """

    conditions = []
    params = []

    if search_query and search_query.strip():
        q = f"%{search_query.strip()}%"
        conditions.append("(a.account_number LIKE ? OR a.name LIKE ? OR a.phone LIKE ?)")
        params.extend([q, q, q])

    if filter_balance == "high":
        conditions.append("a.balance >= 1000")
    elif filter_balance == "low":
        conditions.append("a.balance < 100")

    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)

    base_query += " ORDER BY a.created_at DESC"

    cursor.execute(base_query, tuple(params))
    rows = cursor.fetchall()
    conn.close()

    accounts = []
    for r in rows:
        accounts.append({
            "account_number": r["account_number"],
            "name": r["name"],
            "phone": r["phone"],
            "pin": r["pin"],
            "balance": float(r["balance"]),
            "created_at": r["created_at"],
            "total_deposited": float(r["total_deposited"]),
            "total_withdrawn": float(r["total_withdrawn"]),
            "total_tx_count": int(r["total_tx_count"])
        })
    return accounts


def get_bank_financial_overview():
    """Computes comprehensive Bank Executive Financial Overview & Security Counts."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*), COALESCE(SUM(balance), 0.0), COALESCE(AVG(balance), 0.0) FROM accounts")
    acc_row = cursor.fetchone()
    total_accounts = acc_row[0] if acc_row else 0
    total_balance = float(acc_row[1]) if acc_row else 0.0
    avg_balance = float(acc_row[2]) if acc_row else 0.0

    cursor.execute("SELECT COALESCE(SUM(amount), 0.0) FROM transactions WHERE transaction_type LIKE '%Deposit%'")
    inflow = float(cursor.fetchone()[0] or 0.0)

    cursor.execute("SELECT COALESCE(SUM(amount), 0.0) FROM transactions WHERE transaction_type = 'Withdrawal'")
    outflow = float(cursor.fetchone()[0] or 0.0)

    cursor.execute("SELECT COUNT(*) FROM transactions")
    total_tx = int(cursor.fetchone()[0] or 0)

    # Login counts
    cursor.execute("SELECT COUNT(*) FROM login_history WHERE status = 'SUCCESS'")
    total_logins = int(cursor.fetchone()[0] or 0)

    cursor.execute("SELECT COUNT(*) FROM login_history WHERE status = 'FAILED'")
    failed_logins = int(cursor.fetchone()[0] or 0)

    conn.close()

    return {
        "total_accounts": total_accounts,
        "total_balance": total_balance,
        "avg_balance": avg_balance,
        "total_inflow": inflow,
        "total_outflow": outflow,
        "total_transactions": total_tx,
        "total_logins": total_logins,
        "failed_logins": failed_logins
    }


def get_global_transactions(limit=100, filter_type=None, search_query=None):
    """Fetches system-wide global transactions joining customer names."""
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            t.id,
            t.timestamp,
            t.account_number,
            COALESCE(a.name, 'Deleted Account') as customer_name,
            t.transaction_type,
            t.amount,
            t.balance_after
        FROM transactions t
        LEFT JOIN accounts a ON t.account_number = a.account_number
    """

    conditions = []
    params = []

    if filter_type and filter_type != "All":
        conditions.append("t.transaction_type LIKE ?")
        params.append(f"%{filter_type}%")

    if search_query and search_query.strip():
        q = f"%{search_query.strip()}%"
        conditions.append("(t.account_number LIKE ? OR a.name LIKE ?)")
        params.extend([q, q])

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY t.id DESC LIMIT ?"
    params.append(limit)

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    conn.close()

    transactions = []
    for r in rows:
        transactions.append({
            "id": r["id"],
            "timestamp": r["timestamp"],
            "account_number": r["account_number"],
            "customer_name": r["customer_name"],
            "type": r["transaction_type"],
            "amount": float(r["amount"]),
            "balance_after": float(r["balance_after"])
        })
    return transactions


def update_account(account_number, name, phone, pin):
    """Updates customer profile details."""
    acc_num = str(account_number).strip()
    name = name.strip()
    phone = phone.strip()
    pin = str(pin).strip()

    if not name:
        return False, "Customer Name cannot be empty."
    if not phone or not phone.isdigit() or len(phone) < 7:
        return False, "Please enter a valid phone number (digits only, at least 7 digits)."
    if not pin or not pin.isdigit() or len(pin) != 4:
        return False, "Security PIN must be exactly 4 digits."

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE accounts
            SET name = ?, phone = ?, pin = ?
            WHERE account_number = ?
        """, (name, phone, pin, acc_num))
        conn.commit()
        return True, f"Account #{acc_num} updated successfully."
    except sqlite3.Error as e:
        conn.rollback()
        return False, f"Failed to update account: {str(e)}"
    finally:
        conn.close()


def delete_account(account_number):
    """Deletes an account and its associated transactions."""
    acc_num = str(account_number).strip()
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM transactions WHERE account_number = ?", (acc_num,))
        cursor.execute("DELETE FROM accounts WHERE account_number = ?", (acc_num,))
        conn.commit()
        return True, f"Account #{acc_num} permanently deleted."
    except sqlite3.Error as e:
        conn.rollback()
        return False, f"Failed to delete account: {str(e)}"
    finally:
        conn.close()


def deposit(account_number, amount, note="Deposit"):
    """Deposits money into an account and records transaction."""
    acc_num = str(account_number).strip()

    try:
        amount = float(amount)
    except (ValueError, TypeError):
        return False, "Please enter a valid numeric amount."

    if amount <= 0:
        return False, "Deposit amount must be greater than $0.00."

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT balance FROM accounts WHERE account_number = ?", (acc_num,))
        row = cursor.fetchone()
        if not row:
            return False, "Account not found."

        current_balance = float(row["balance"])
        new_balance = round(current_balance + amount, 2)
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("UPDATE accounts SET balance = ? WHERE account_number = ?", (new_balance, acc_num))
        cursor.execute("""
            INSERT INTO transactions (account_number, transaction_type, amount, balance_after, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (acc_num, note, amount, new_balance, now_str))

        conn.commit()
        return True, new_balance
    except sqlite3.Error as e:
        conn.rollback()
        return False, f"Database transaction failed: {str(e)}"
    finally:
        conn.close()


def withdraw(account_number, amount, note="Withdrawal"):
    """Withdraws money from an account if sufficient balance is available."""
    acc_num = str(account_number).strip()

    try:
        amount = float(amount)
    except (ValueError, TypeError):
        return False, "Please enter a valid numeric amount."

    if amount <= 0:
        return False, "Withdrawal amount must be greater than $0.00."

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT balance FROM accounts WHERE account_number = ?", (acc_num,))
        row = cursor.fetchone()
        if not row:
            return False, "Account not found."

        current_balance = float(row["balance"])

        if amount > current_balance:
            return False, f"Insufficient balance! Current balance: ${current_balance:,.2f}"

        new_balance = round(current_balance - amount, 2)
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("UPDATE accounts SET balance = ? WHERE account_number = ?", (new_balance, acc_num))
        cursor.execute("""
            INSERT INTO transactions (account_number, transaction_type, amount, balance_after, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (acc_num, note, amount, new_balance, now_str))

        conn.commit()
        return True, new_balance
    except sqlite3.Error as e:
        conn.rollback()
        return False, f"Database transaction failed: {str(e)}"
    finally:
        conn.close()


def get_transactions(account_number):
    """Retrieves all transactions for an account."""
    acc_num = str(account_number).strip()
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, transaction_type, amount, balance_after, timestamp
        FROM transactions
        WHERE account_number = ?
        ORDER BY id DESC
    """, (acc_num,))

    rows = cursor.fetchall()
    conn.close()

    transactions = []
    for r in rows:
        transactions.append({
            "id": r["id"],
            "type": r["transaction_type"],
            "amount": float(r["amount"]),
            "balance_after": float(r["balance_after"]),
            "timestamp": r["timestamp"]
        })
    return transactions


# Initialize database
init_db()
