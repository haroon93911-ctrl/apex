"""
test_db.py - Automated Verification of Database, Business Logic, Bank Manager Features & Login History
"""

import os
import sys

# Ensure module path is accessible
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import database

def run_tests():
    print("=" * 65)
    print("Testing Apex Bank Management System (Login History & Security Logs)")
    print("=" * 65)

    # 1. Initialize Database & Seed Manager
    database.init_db()
    print("[OK] Database & tables initialized successfully.")

    # 2. Test Account Creation
    success, msg, acc_num = database.create_account(
        name="John Doe",
        phone="9876543210",
        pin="1234",
        initial_balance=500.00
    )
    assert success, f"Account creation failed: {msg}"
    assert acc_num is not None
    print(f"[OK] Customer Account created with Account No: {acc_num}, Initial Balance: $500.00")

    # 3. Test Failed Customer Login & History Logging
    fail_auth, _ = database.authenticate(acc_num, "9999")
    assert not fail_auth, "Auth should fail on wrong PIN"
    print(f"[OK] Failed login blocked for account #{acc_num} (wrong PIN)")

    # 4. Test Successful Customer Login & History Logging
    auth_ok, auth_data = database.authenticate(acc_num, "1234")
    assert auth_ok, "Auth should succeed on correct PIN"
    print(f"[OK] Successful customer login for {auth_data['name']}")

    # 5. Test Manager Authentication & Logging
    admin_ok, admin_data = database.authenticate_admin("admin", "admin123")
    assert admin_ok, "Admin auth should succeed with default credentials"
    print(f"[OK] Successful Manager Login for '{admin_data['name']}' ({admin_data['role']})")

    # 6. Test Login History Records Retrieval
    login_logs = database.get_login_history()
    assert len(login_logs) >= 3, f"Expected at least 3 login logs, got {len(login_logs)}"
    print(f"[OK] Login history fetched {len(login_logs)} log records:")
    for l in login_logs[:4]:
        print(f"    - {l['timestamp']} | {l['role']} | {l['user_identifier']} ({l['user_name']}) | Status: {l['status']} | Notes: {l['failure_reason']}")

    # 7. Test Customer Last Login Retrieval
    last_login = database.get_customer_last_login(acc_num)
    assert last_login is not None
    print(f"[OK] Customer Last Login time retrieved: {last_login}")

    # 8. Test Bank Financial Overview with Security Logins Metrics
    overview = database.get_bank_financial_overview()
    assert overview["total_logins"] >= 2
    assert overview["failed_logins"] >= 1
    print(f"[OK] Security Metrics -> Total Successful Logins: {overview['total_logins']} | Failed Attempts: {overview['failed_logins']}")

    print("\n" + "=" * 65)
    print("ALL LOGIN HISTORY & SYSTEM TESTS PASSED WITH 100% SUCCESS!")
    print("=" * 65)

if __name__ == "__main__":
    run_tests()
