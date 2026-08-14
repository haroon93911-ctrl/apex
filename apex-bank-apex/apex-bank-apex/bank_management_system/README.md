# 🏛️ Apex National Bank — Executive Management System (Python + Tkinter + SQLite)

A modern, desktop Bank Management System created in Python with Tkinter GUI and SQLite database. Includes a **Full Executive Bank Manager Suite** and **Customer Online Banking Portal**.

---

## 🌟 Executive Bank Manager Suite (Full Bank Authority)

Log in via the **"🏛️ Bank Manager Suite"** tab using:
- **Username**: `admin`
- **Password**: `admin123`

### 1. 📊 Financial Analytics & Executive Overview
- **Bank Vault Reserves**: Total available liquidity across all customer accounts.
- **Active Accounts Count & Average Balance**: Customer population and financial health.
- **Total Inflow (Deposits)**: All-time bank deposit volume.
- **Total Outflow (Withdrawals)**: All-time bank withdrawal volume.
- **Live Activity Feed**: Real-time ticker showing recent transactions across the system.

### 2. 👥 Customer Accounts Directory & Full Dossiers
- Complete directory table showing:
  - Account Number
  - Customer Name
  - Phone Number
  - 4-Digit Security PIN
  - Current Available Balance ($)
  - Lifetime Deposited Amount ($)
  - Lifetime Withdrawn Amount ($)
  - Total Transactions Count
  - Registration Date
- **Quick Filters**:
  - All Accounts
  - VIP / High Balance (`≥ $1,000`)
  - Low Balance (`< $100`)
  - Live Search by Name, Account Number, or Phone.
- **Manager Operations on Selected Account**:
  - 📜 **Full Customer Dossier & Statement**: Interactive pop-up showing customer profile and entire transaction statement.
  - ✏️ **Edit Customer Info**: Update Name, Phone, or reset Security PIN directly.
  - 💵 **Manager Cashier Operations**: Execute Deposits or Withdrawals on behalf of the customer.
  - 🗑️ **Close Account**: Permanently close an account with confirmation.

### 3. 📜 Global System Transaction Ledger (Audit Trail)
- Master audit log of EVERY transaction conducted in the entire bank.
- Filter by transaction type (All, Deposit, Withdrawal, Initial Deposit).
- Instant search by Account Number or Customer Name.

---

## 💳 Customer Online Banking Portal

- **Live Balance Hero Card**: Bold, real-time balance display.
- **Quick Deposit**: Custom amounts with quick preset buttons (`+$50`, `+$100`, `+$500`, `+$1000`).
- **Protected Withdrawal**: With instant overdraft and insufficient funds detection.
- **Personal Statement History**: Color-coded table with timestamps and resulting balances.

---

## 📁 Project Structure

```text
bank_management_system/
│
├── database.py       # SQLite database engine, migrations, and analytics queries
├── main.py           # Tkinter GUI application (Manager Suite & Customer Portal)
├── test_db.py        # Automated test suite for all database and manager functions
├── run_app.bat       # 1-Click Windows launcher script
├── bank.db           # SQLite database file (created automatically)
└── README.md         # Full project documentation & viva guide
```

---

## 🚀 How to Run

### Method 1: Double-Click (Windows)
Double-click `run_app.bat` or `run_bank_system.bat`.

### Method 2: Terminal / Command Prompt
```bash
cd bank_management_system
python main.py
```

### Method 3: Run Verification Test Suite
```bash
cd bank_management_system
python test_db.py
```
