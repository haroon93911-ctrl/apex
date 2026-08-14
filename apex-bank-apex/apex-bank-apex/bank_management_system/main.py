"""
=============================================================================
         APEX NATIONAL BANK — EXECUTIVE BANK MANAGEMENT SYSTEM
=============================================================================
A modern, feature-rich desktop banking application built with:
- Python 3 standard library
- SQLite3 (database.py) for persistent relational storage
- Tkinter & ttk with custom executive styling

Includes:
1. 🏛️ Complete Bank Manager Portal (Executive Suite):
   - Real-Time Bank Financial Analytics (Vault Reserves, Inflows, Outflows, Averages)
   - Comprehensive Customer Directory (Balances, Inflows, Outflows, Activity, PIN)
   - Live Search, VIP & Low Balance Filters
   - Customer Dossier & Statement Inspector Modal
   - Account Editor (Update Name, Phone, Security PIN)
   - Direct Manager Cashier Operations (Deposit / Withdraw / Adjustments)
   - Global System Transaction Audit Ledger
   - 🔐 Security & Login History Audit Trail (Tracks all Successful & Failed Logins)
   - Customer Account Opening
2. 💳 Customer Online Banking Portal:
   - Account Balance & Details Dashboard with Last Login timestamp
   - Quick Preset Deposits & Overdraft-Protected Withdrawals
   - Real-time Personal Statement Table
   - Personal Login History Audit
3. 100% Offline, Zero External Dependencies, Beginner-Friendly Architecture
=============================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

# Add local path for database module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import database


# =============================================================================
# THEME TOKENS & COLOR PALETTE
# =============================================================================
PRIMARY_DARK    = "#0f172a"   # Deep Slate / Executive Navy
PRIMARY_BAR     = "#1e293b"   # Slate Navigation Bar
ACCENT_BLUE     = "#2563eb"   # Royal Blue
ACCENT_HOVER    = "#1d4ed8"   # Darker Blue
ACCENT_INDIGO   = "#4f46e5"   # Indigo for Manager Highlights
SUCCESS_EMERALD = "#059669"   # Emerald Green for Deposits / Positive Balances
SUCCESS_BG      = "#ecfdf5"   # Light Emerald
DANGER_CRIMSON  = "#dc2626"   # Crimson for Withdrawals / Deletes / Failed Logins
DANGER_BG       = "#fef2f2"   # Light Crimson
WARNING_AMBER   = "#d97706"   # Amber for Warnings / Low Balances
PURPLE_COLOR    = "#7c3aed"   # Security / Audit Accent
CARD_BG         = "#ffffff"   # Pure White Card Background
BG_CANVAS       = "#f8fafc"   # Soft Slate App Canvas
TEXT_MAIN       = "#0f172a"   # Dark Heading / Main Text
TEXT_MUTED      = "#64748b"   # Secondary Slate Subtitle
BORDER_LINE     = "#e2e8f0"   # Clean Separator Line


class BankManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window Settings
        self.title("Apex National Bank — Executive Management System")
        self.geometry("1140x780")
        self.minsize(1040, 700)
        self.configure(bg=BG_CANVAS)

        # Center Window on Screen
        self.center_window(1140, 780)

        # Session State
        self.current_user = None   # Logged-in Customer dictionary
        self.current_admin = None  # Logged-in Manager dictionary

        # Initialize SQLite Database
        database.init_db()

        # Apply Modern TTK Styles
        self.setup_styles()

        # Root Container
        self.container = tk.Frame(self, bg=BG_CANVAS)
        self.container.pack(fill="both", expand=True)

        # Launch with Auth screen
        self.show_auth_screen()

    def center_window(self, width, height):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = max(0, (sw - width) // 2)
        y = max(0, (sh - height) // 2 - 25)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Tab Notebook
        style.configure("TNotebook", background=BG_CANVAS, borderwidth=0)
        style.configure("TNotebook.Tab",
                        font=("Segoe UI", 10, "bold"),
                        padding=[16, 9],
                        background="#e2e8f0",
                        foreground=TEXT_MAIN)
        style.map("TNotebook.Tab",
                  background=[("selected", CARD_BG)],
                  foreground=[("selected", ACCENT_BLUE)])

        # Data Tables (Treeview)
        style.configure("Treeview",
                        background="#ffffff",
                        foreground=TEXT_MAIN,
                        rowheight=29,
                        fieldbackground="#ffffff",
                        font=("Segoe UI", 10))
        style.configure("Treeview.Heading",
                        background="#f1f5f9",
                        foreground=PRIMARY_DARK,
                        font=("Segoe UI", 10, "bold"),
                        padding=[8, 8])
        style.map("Treeview",
                  background=[("selected", "#dbeafe")],
                  foreground=[("selected", PRIMARY_DARK)])

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    # =========================================================================
    # SCREEN 1: AUTHENTICATION & PORTAL SELECTION
    # =========================================================================
    def show_auth_screen(self, default_tab=0, prefill_acc=""):
        self.clear_container()
        self.current_user = None
        self.current_admin = None

        # Executive Top Banner
        header = tk.Frame(self.container, bg=PRIMARY_DARK, height=105)
        header.pack(fill="x", side="top")

        title_box = tk.Frame(header, bg=PRIMARY_DARK)
        title_box.pack(pady=16)

        tk.Label(title_box, text="🏛️", font=("Segoe UI Emoji", 26), bg=PRIMARY_DARK, fg="#ffffff").pack(side="left", padx=(0, 12))
        tk.Label(title_box, text="APEX NATIONAL BANK", font=("Segoe UI", 22, "bold"), bg=PRIMARY_DARK, fg="#ffffff").pack(side="left")

        tk.Label(header, text="Enterprise Banking, Audit Security & Management System",
                 font=("Segoe UI", 10), bg=PRIMARY_DARK, fg="#94a3b8").pack()

        # Body Canvas
        body = tk.Frame(self.container, bg=BG_CANVAS)
        body.pack(fill="both", expand=True, padx=40, pady=25)

        card = tk.Frame(body, bg=CARD_BG, relief="flat", highlightthickness=1,
                        highlightbackground=BORDER_LINE, bd=0)
        card.place(relx=0.5, rely=0.5, anchor="center", width=640, height=530)

        notebook = ttk.Notebook(card)
        notebook.pack(fill="both", expand=True, padx=16, pady=16)

        # 1. Bank Manager Login Tab
        admin_tab = tk.Frame(notebook, bg=CARD_BG, padx=25, pady=18)
        notebook.add(admin_tab, text="  🏛️ Bank Manager Suite  ")
        self.build_manager_login_tab(admin_tab)

        # 2. Customer Login Tab
        cust_tab = tk.Frame(notebook, bg=CARD_BG, padx=25, pady=18)
        notebook.add(cust_tab, text="  💳 Customer Login  ")
        self.build_customer_login_tab(cust_tab, prefill_acc)

        # 3. Open Account Tab
        reg_tab = tk.Frame(notebook, bg=CARD_BG, padx=25, pady=18)
        notebook.add(reg_tab, text="  ➕ Open New Account  ")
        self.build_register_tab(reg_tab)

        notebook.select(default_tab)

    # -------------------------------------------------------------------------
    # TAB: MANAGER LOGIN
    # -------------------------------------------------------------------------
    def build_manager_login_tab(self, parent):
        tk.Label(parent, text="Bank Executive / Manager Access", font=("Segoe UI", 16, "bold"),
                 bg=CARD_BG, fg=PRIMARY_DARK).pack(anchor="w", pady=(0, 2))
        tk.Label(parent, text="Full authority to view all accounts, vault reserves, customer dossiers, & login audit logs.",
                 font=("Segoe UI", 9), bg=CARD_BG, fg=TEXT_MUTED).pack(anchor="w", pady=(0, 16))

        tk.Label(parent, text="Manager Username", font=("Segoe UI", 10, "bold"),
                 bg=CARD_BG, fg=TEXT_MAIN).pack(anchor="w", pady=(0, 3))
        ent_uname = tk.Entry(parent, font=("Segoe UI", 11), bg="#f8fafc", relief="solid", bd=1)
        ent_uname.insert(0, "admin")
        ent_uname.pack(fill="x", ipady=6, pady=(0, 12))

        tk.Label(parent, text="Manager Password", font=("Segoe UI", 10, "bold"),
                 bg=CARD_BG, fg=TEXT_MAIN).pack(anchor="w", pady=(0, 3))
        ent_pwd = tk.Entry(parent, font=("Segoe UI", 11), bg="#f8fafc", relief="solid", bd=1, show="*")
        ent_pwd.insert(0, "admin123")
        ent_pwd.pack(fill="x", ipady=6, pady=(0, 4))

        show_var = tk.BooleanVar(value=False)
        def toggle_pwd():
            ent_pwd.config(show="" if show_var.get() else "*")
        tk.Checkbutton(parent, text="Show Password", variable=show_var, command=toggle_pwd,
                       bg=CARD_BG, activebackground=CARD_BG, font=("Segoe UI", 9), fg=TEXT_MUTED).pack(anchor="w", pady=(0, 18))

        def on_manager_login():
            u = ent_uname.get().strip()
            p = ent_pwd.get().strip()
            if not u or not p:
                messagebox.showwarning("Input Required", "Please enter Manager Username and Password.")
                return
            success, res = database.authenticate_admin(u, p)
            if success:
                self.current_admin = res
                messagebox.showinfo("Executive Login", f"Access Granted!\nWelcome, {res['name']} ({res['role']}).\n(Login attempt logged in security history)")
                self.show_manager_portal_screen()
            else:
                messagebox.showerror("Access Denied", res)

        btn_login = tk.Button(parent, text="Access Bank Manager Suite 🏛️ →", font=("Segoe UI", 11, "bold"),
                              bg=ACCENT_INDIGO, fg="#ffffff", activebackground="#4338ca",
                              activeforeground="#ffffff", relief="flat", cursor="hand2",
                              command=on_manager_login)
        btn_login.pack(fill="x", ipady=8)

        ent_uname.bind("<Return>", lambda e: on_manager_login())
        ent_pwd.bind("<Return>", lambda e: on_manager_login())

        lbl_hint = tk.Label(parent, text="🔑 Default Manager Login: username: admin  |  password: admin123",
                            font=("Segoe UI", 9, "italic"), bg=CARD_BG, fg=TEXT_MUTED)
        lbl_hint.pack(side="bottom", pady=4)

    # -------------------------------------------------------------------------
    # TAB: CUSTOMER LOGIN
    # -------------------------------------------------------------------------
    def build_customer_login_tab(self, parent, prefill_acc=""):
        tk.Label(parent, text="Customer Online Banking", font=("Segoe UI", 16, "bold"),
                 bg=CARD_BG, fg=PRIMARY_DARK).pack(anchor="w", pady=(0, 2))
        tk.Label(parent, text="Access personal account, balance, deposits, withdrawals, & login activity.",
                 font=("Segoe UI", 9), bg=CARD_BG, fg=TEXT_MUTED).pack(anchor="w", pady=(0, 16))

        tk.Label(parent, text="6-Digit Account Number", font=("Segoe UI", 10, "bold"),
                 bg=CARD_BG, fg=TEXT_MAIN).pack(anchor="w", pady=(0, 3))
        ent_acc = tk.Entry(parent, font=("Segoe UI", 11), bg="#f8fafc", relief="solid", bd=1)
        ent_acc.pack(fill="x", ipady=6, pady=(0, 12))
        if prefill_acc:
            ent_acc.insert(0, prefill_acc)

        tk.Label(parent, text="4-Digit Security PIN", font=("Segoe UI", 10, "bold"),
                 bg=CARD_BG, fg=TEXT_MAIN).pack(anchor="w", pady=(0, 3))
        ent_pin = tk.Entry(parent, font=("Segoe UI", 11), bg="#f8fafc", relief="solid", bd=1, show="*")
        ent_pin.pack(fill="x", ipady=6, pady=(0, 4))

        show_var = tk.BooleanVar(value=False)
        def toggle_pin():
            ent_pin.config(show="" if show_var.get() else "*")
        tk.Checkbutton(parent, text="Show PIN", variable=show_var, command=toggle_pin,
                       bg=CARD_BG, activebackground=CARD_BG, font=("Segoe UI", 9), fg=TEXT_MUTED).pack(anchor="w", pady=(0, 18))

        def on_cust_login():
            acc = ent_acc.get().strip()
            pin = ent_pin.get().strip()
            if not acc or not pin:
                messagebox.showwarning("Input Required", "Please enter Account Number and 4-digit PIN.")
                return
            success, res = database.authenticate(acc, pin)
            if success:
                self.current_user = res
                messagebox.showinfo("Login Successful", f"Welcome back, {res['name']}!\n(Login activity saved to security history)")
                self.show_customer_portal_screen()
            else:
                messagebox.showerror("Login Failed", res)

        btn_cust_login = tk.Button(parent, text="Log In to Customer Account →", font=("Segoe UI", 11, "bold"),
                                   bg=ACCENT_BLUE, fg="#ffffff", activebackground=ACCENT_HOVER,
                                   activeforeground="#ffffff", relief="flat", cursor="hand2",
                                   command=on_cust_login)
        btn_cust_login.pack(fill="x", ipady=8)

        ent_acc.bind("<Return>", lambda e: on_cust_login())
        ent_pin.bind("<Return>", lambda e: on_cust_login())

    # -------------------------------------------------------------------------
    # TAB: OPEN ACCOUNT
    # -------------------------------------------------------------------------
    def build_register_tab(self, parent):
        tk.Label(parent, text="Open a New Bank Account", font=("Segoe UI", 15, "bold"),
                 bg=CARD_BG, fg=PRIMARY_DARK).pack(anchor="w", pady=(0, 2))
        tk.Label(parent, text="Fill out customer details. A unique 6-digit account number is auto-created.",
                 font=("Segoe UI", 9), bg=CARD_BG, fg=TEXT_MUTED).pack(anchor="w", pady=(0, 10))

        form = tk.Frame(parent, bg=CARD_BG)
        form.pack(fill="both", expand=True)

        tk.Label(form, text="Customer Full Name", font=("Segoe UI", 9, "bold"),
                 bg=CARD_BG, fg=TEXT_MAIN).grid(row=0, column=0, sticky="w", pady=(2, 2))
        ent_name = tk.Entry(form, font=("Segoe UI", 10), bg="#f8fafc", relief="solid", bd=1)
        ent_name.grid(row=1, column=0, columnspan=2, sticky="ew", ipady=4, pady=(0, 6))

        tk.Label(form, text="Phone Number (Digits)", font=("Segoe UI", 9, "bold"),
                 bg=CARD_BG, fg=TEXT_MAIN).grid(row=2, column=0, sticky="w", pady=(2, 2))
        ent_phone = tk.Entry(form, font=("Segoe UI", 10), bg="#f8fafc", relief="solid", bd=1)
        ent_phone.grid(row=3, column=0, columnspan=2, sticky="ew", ipady=4, pady=(0, 6))

        tk.Label(form, text="4-Digit Security PIN", font=("Segoe UI", 9, "bold"),
                 bg=CARD_BG, fg=TEXT_MAIN).grid(row=4, column=0, sticky="w", pady=(2, 2), padx=(0, 6))
        ent_pin = tk.Entry(form, font=("Segoe UI", 10), bg="#f8fafc", relief="solid", bd=1, show="*")
        ent_pin.grid(row=5, column=0, sticky="ew", ipady=4, pady=(0, 10), padx=(0, 6))

        tk.Label(form, text="Initial Deposit ($)", font=("Segoe UI", 9, "bold"),
                 bg=CARD_BG, fg=TEXT_MAIN).grid(row=4, column=1, sticky="w", pady=(2, 2), padx=(6, 0))
        ent_dep = tk.Entry(form, font=("Segoe UI", 10), bg="#f8fafc", relief="solid", bd=1)
        ent_dep.insert(0, "150.00")
        ent_dep.grid(row=5, column=1, sticky="ew", ipady=4, pady=(0, 10), padx=(6, 0))

        form.columnconfigure(0, weight=1)
        form.columnconfigure(1, weight=1)

        def on_create_account():
            name = ent_name.get().strip()
            phone = ent_phone.get().strip()
            pin = ent_pin.get().strip()
            dep_val = ent_dep.get().strip()

            if not name:
                messagebox.showwarning("Validation Error", "Full Name cannot be empty.")
                return
            if not phone or not phone.isdigit() or len(phone) < 7:
                messagebox.showwarning("Validation Error", "Please enter a valid numeric phone number (minimum 7 digits).")
                return
            if not pin or not pin.isdigit() or len(pin) != 4:
                messagebox.showwarning("Validation Error", "Security PIN must be exactly 4 numeric digits.")
                return

            try:
                initial_deposit = float(dep_val) if dep_val else 0.0
                if initial_deposit < 0:
                    messagebox.showwarning("Validation Error", "Initial deposit cannot be negative.")
                    return
            except ValueError:
                messagebox.showwarning("Validation Error", "Please enter a valid numeric amount.")
                return

            success, msg, acc_num = database.create_account(name, phone, pin, initial_deposit)
            if success:
                messagebox.showinfo(
                    "Account Created Successfully!",
                    f"🎉 Account Registered!\n\n"
                    f"Account Holder:  {name}\n"
                    f"Account Number:  {acc_num}\n"
                    f"Security PIN:    {pin}\n"
                    f"Initial Balance: ${initial_deposit:,.2f}\n\n"
                    f"You can now log in using Account Number '{acc_num}' and your PIN."
                )
                self.show_auth_screen(default_tab=1, prefill_acc=acc_num)
            else:
                messagebox.showerror("Error", msg)

        btn_create = tk.Button(parent, text="Create Bank Account ✓", font=("Segoe UI", 11, "bold"),
                               bg=SUCCESS_EMERALD, fg="#ffffff", activebackground="#047857",
                               activeforeground="#ffffff", relief="flat", cursor="hand2",
                               command=on_create_account)
        btn_create.pack(fill="x", ipady=7, pady=(6, 0))

    # =========================================================================
    # SCREEN 2: 🏛️ BANK MANAGER EXECUTIVE SUITE
    # =========================================================================
    def show_manager_portal_screen(self):
        self.clear_container()

        # Top Executive Header
        top_header = tk.Frame(self.container, bg=PRIMARY_DARK, height=65)
        top_header.pack(fill="x", side="top")

        left_brand = tk.Frame(top_header, bg=PRIMARY_DARK)
        left_brand.pack(side="left", padx=20, pady=12)

        tk.Label(left_brand, text="🏛️", font=("Segoe UI Emoji", 20), bg=PRIMARY_DARK, fg="#ffffff").pack(side="left", padx=(0, 8))
        tk.Label(left_brand, text="APEX NATIONAL BANK", font=("Segoe UI", 15, "bold"), bg=PRIMARY_DARK, fg="#ffffff").pack(side="left")
        tk.Label(left_brand, text=" |  EXECUTIVE MANAGER PORTAL", font=("Segoe UI", 11), bg=PRIMARY_DARK, fg="#94a3b8").pack(side="left")

        right_brand = tk.Frame(top_header, bg=PRIMARY_DARK)
        right_brand.pack(side="right", padx=20, pady=12)

        tk.Label(right_brand, text=f"👑 {self.current_admin['name']} ({self.current_admin['role']})",
                 font=("Segoe UI", 10, "bold"), bg=PRIMARY_DARK, fg="#c084fc").pack(side="left", padx=(0, 15))

        btn_logout = tk.Button(right_brand, text="🚪 Exit Portal", font=("Segoe UI", 9, "bold"),
                               bg="#334155", fg="#ffffff", activebackground=DANGER_CRIMSON,
                               activeforeground="#ffffff", relief="flat", padx=12, pady=4,
                               cursor="hand2", command=self.handle_logout)
        btn_logout.pack(side="left")

        # Manager Body Notebook (Tabs)
        body = tk.Frame(self.container, bg=BG_CANVAS)
        body.pack(fill="both", expand=True, padx=20, pady=15)

        manager_notebook = ttk.Notebook(body)
        manager_notebook.pack(fill="both", expand=True)

        # Tab 1: Executive Financial Overview
        tab_overview = tk.Frame(manager_notebook, bg=BG_CANVAS, padx=15, pady=15)
        manager_notebook.add(tab_overview, text="  📊 Financial Analytics & Overview  ")
        self.build_manager_overview_view(tab_overview)

        # Tab 2: Customer Directory & Dossiers
        tab_directory = tk.Frame(manager_notebook, bg=BG_CANVAS, padx=15, pady=15)
        manager_notebook.add(tab_directory, text="  👥 Customer Accounts Directory  ")
        self.build_manager_directory_view(tab_directory)

        # Tab 3: Global System Ledger (Audit Trail)
        tab_ledger = tk.Frame(manager_notebook, bg=BG_CANVAS, padx=15, pady=15)
        manager_notebook.add(tab_ledger, text="  📜 Global System Transaction Ledger  ")
        self.build_manager_ledger_view(tab_ledger)

        # Tab 4: 🔐 Security & Login History Audit
        tab_security = tk.Frame(manager_notebook, bg=BG_CANVAS, padx=15, pady=15)
        manager_notebook.add(tab_security, text="  🔐 Security & Login Audit Logs  ")
        self.build_manager_security_view(tab_security)

    # -------------------------------------------------------------------------
    # MANAGER VIEW 1: FINANCIAL ANALYTICS & OVERVIEW
    # -------------------------------------------------------------------------
    def build_manager_overview_view(self, parent):
        stats = database.get_bank_financial_overview()

        # Top 4 KPI Metrics Grid
        kpi_frame = tk.Frame(parent, bg=BG_CANVAS)
        kpi_frame.pack(fill="x", pady=(0, 16))

        # KPI 1: Vault Reserves
        self.make_metric_card(kpi_frame, "TOTAL BANK VAULT RESERVES", f"${stats['total_balance']:,.2f}",
                              f"Avg per account: ${stats['avg_balance']:,.2f}", SUCCESS_EMERALD, col=0)

        # KPI 2: Customer Accounts
        self.make_metric_card(kpi_frame, "ACTIVE CUSTOMER ACCOUNTS", f"{stats['total_accounts']} Accounts",
                              f"Total Bank System Transactions: {stats['total_transactions']}", ACCENT_BLUE, col=1)

        # KPI 3: Inflows (Deposits)
        self.make_metric_card(kpi_frame, "TOTAL DEPOSITS (INFLOWS)", f"+${stats['total_inflow']:,.2f}",
                              f"Successful Logins: {stats['total_logins']}", ACCENT_INDIGO, col=2)

        # KPI 4: Outflows & Security
        self.make_metric_card(kpi_frame, "TOTAL WITHDRAWALS (OUTFLOWS)", f"-${stats['total_outflow']:,.2f}",
                              f"Security Alerts (Failed Logins): {stats['failed_logins']}", DANGER_CRIMSON, col=3)

        kpi_frame.columnconfigure(0, weight=1)
        kpi_frame.columnconfigure(1, weight=1)
        kpi_frame.columnconfigure(2, weight=1)
        kpi_frame.columnconfigure(3, weight=1)

        # Bottom Split: Recent Transactions + Quick Actions
        split_box = tk.Frame(parent, bg=BG_CANVAS)
        split_box.pack(fill="both", expand=True)

        # Left: Recent Global Transactions Feed
        feed_card = tk.Frame(split_box, bg=CARD_BG, relief="flat", highlightthickness=1,
                             highlightbackground=BORDER_LINE, padx=16, pady=12)
        feed_card.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(feed_card, text="⚡ Live Bank Activity Feed (Latest System Transactions)",
                 font=("Segoe UI", 12, "bold"), bg=CARD_BG, fg=PRIMARY_DARK).pack(anchor="w", pady=(0, 8))

        recent_tree = ttk.Treeview(feed_card, columns=("time", "acc", "name", "type", "amt"), show="headings", height=10)
        recent_tree.heading("time", text="Timestamp")
        recent_tree.heading("acc", text="Account No.")
        recent_tree.heading("name", text="Customer")
        recent_tree.heading("type", text="Type")
        recent_tree.heading("amt", text="Amount ($)")

        recent_tree.column("time", width=140, anchor="center")
        recent_tree.column("acc", width=100, anchor="center")
        recent_tree.column("name", width=140, anchor="w")
        recent_tree.column("type", width=110, anchor="center")
        recent_tree.column("amt", width=100, anchor="e")

        recent_tree.pack(fill="both", expand=True)

        recent_txs = database.get_global_transactions(limit=12)
        for t in recent_txs:
            recent_tree.insert("", "end", values=(
                t["timestamp"],
                t["account_number"],
                t["customer_name"],
                t["type"],
                f"${t['amount']:,.2f}"
            ))

        # Right: Quick Manager Tool Panel
        tools_card = tk.Frame(split_box, bg=CARD_BG, relief="flat", highlightthickness=1,
                              highlightbackground=BORDER_LINE, padx=18, pady=14, width=320)
        tools_card.pack(side="right", fill="y", padx=(10, 0))
        tools_card.pack_propagate(False)

        tk.Label(tools_card, text="🛠️ Manager Quick Actions", font=("Segoe UI", 12, "bold"),
                 bg=CARD_BG, fg=PRIMARY_DARK).pack(anchor="w", pady=(0, 12))

        btn_open = tk.Button(tools_card, text="➕ Open New Customer Account", font=("Segoe UI", 10, "bold"),
                             bg=SUCCESS_EMERALD, fg="#ffffff", relief="flat", cursor="hand2",
                             command=self.open_manager_new_account_modal)
        btn_open.pack(fill="x", ipady=8, pady=(0, 10))

        btn_refresh = tk.Button(tools_card, text="🔄 Refresh Financial Overview", font=("Segoe UI", 10, "bold"),
                                bg=PRIMARY_BAR, fg="#ffffff", relief="flat", cursor="hand2",
                                command=self.show_manager_portal_screen)
        btn_refresh.pack(fill="x", ipady=8, pady=(0, 10))

        btn_cust_mode = tk.Button(tools_card, text="💳 Switch to Customer View", font=("Segoe UI", 10, "bold"),
                                  bg=ACCENT_BLUE, fg="#ffffff", relief="flat", cursor="hand2",
                                  command=lambda: self.show_auth_screen(default_tab=1))
        btn_cust_mode.pack(fill="x", ipady=8)

    def make_metric_card(self, parent, title, value, subtitle, accent_color, col):
        card = tk.Frame(parent, bg=CARD_BG, relief="flat", highlightthickness=1,
                        highlightbackground=BORDER_LINE, padx=16, pady=12)
        card.grid(row=0, column=col, sticky="nsew", padx=4)

        tk.Label(card, text=title, font=("Segoe UI", 8, "bold"), bg=CARD_BG, fg=TEXT_MUTED).pack(anchor="w")
        tk.Label(card, text=value, font=("Segoe UI", 18, "bold"), bg=CARD_BG, fg=accent_color).pack(anchor="w", pady=(4, 2))
        tk.Label(card, text=subtitle, font=("Segoe UI", 8), bg=CARD_BG, fg=TEXT_MUTED).pack(anchor="w")

    # -------------------------------------------------------------------------
    # MANAGER VIEW 2: CUSTOMER ACCOUNTS DIRECTORY
    # -------------------------------------------------------------------------
    def build_manager_directory_view(self, parent):
        top_bar = tk.Frame(parent, bg=CARD_BG, relief="flat", highlightthickness=1,
                           highlightbackground=BORDER_LINE, padx=16, pady=10)
        top_bar.pack(fill="x", pady=(0, 12))

        tk.Label(top_bar, text="👥 Customer Accounts Directory", font=("Segoe UI", 13, "bold"),
                 bg=CARD_BG, fg=PRIMARY_DARK).pack(side="left")

        search_box = tk.Frame(top_bar, bg=CARD_BG)
        search_box.pack(side="right")

        tk.Label(search_box, text="🔍 Search:", font=("Segoe UI", 9, "bold"), bg=CARD_BG, fg=TEXT_MAIN).pack(side="left", padx=(0, 6))

        ent_search = tk.Entry(search_box, font=("Segoe UI", 10), bg="#f8fafc", relief="solid", bd=1, width=22)
        ent_search.pack(side="left", ipady=3, padx=(0, 6))

        filter_var = tk.StringVar(value="all")

        def apply_directory_filter():
            q = ent_search.get().strip()
            f = filter_var.get()
            self.load_directory_data(search_query=q, filter_balance=f)

        btn_filter = tk.Button(search_box, text="Filter", font=("Segoe UI", 9, "bold"),
                               bg=ACCENT_BLUE, fg="#ffffff", relief="flat", cursor="hand2",
                               padx=10, pady=2, command=apply_directory_filter)
        btn_filter.pack(side="left", padx=(0, 6))

        btn_reset = tk.Button(search_box, text="Reset", font=("Segoe UI", 9),
                              bg="#f1f5f9", fg=PRIMARY_DARK, relief="flat", cursor="hand2",
                              padx=8, pady=2, command=lambda: [ent_search.delete(0, tk.END), filter_var.set("all"), apply_directory_filter()])
        btn_reset.pack(side="left")

        ent_search.bind("<Return>", lambda e: apply_directory_filter())

        # Filter Radio / Preset Pills
        filter_pills = tk.Frame(parent, bg=BG_CANVAS)
        filter_pills.pack(fill="x", pady=(0, 8))

        tk.Label(filter_pills, text="Quick Filters:", font=("Segoe UI", 9, "bold"), bg=BG_CANVAS, fg=TEXT_MUTED).pack(side="left", padx=(0, 8))

        for label, val in [("All Accounts", "all"), ("VIP / High Balance (≥ $1,000)", "high"), ("Low Balance (< $100)", "low")]:
            rb = tk.Radiobutton(filter_pills, text=label, variable=filter_var, value=val,
                                bg=BG_CANVAS, activebackground=BG_CANVAS, font=("Segoe UI", 9),
                                command=apply_directory_filter)
            rb.pack(side="left", padx=6)

        # Main Accounts Table
        tbl_container = tk.Frame(parent, bg=CARD_BG, relief="flat", highlightthickness=1,
                                 highlightbackground=BORDER_LINE)
        tbl_container.pack(fill="both", expand=True)

        cols = ("acc", "name", "phone", "pin", "balance", "deposited", "withdrawn", "tx_count", "date")
        self.dir_tree = ttk.Treeview(tbl_container, columns=cols, show="headings", selectmode="browse")

        self.dir_tree.heading("acc", text="Account No.")
        self.dir_tree.heading("name", text="Customer Full Name")
        self.dir_tree.heading("phone", text="Phone Number")
        self.dir_tree.heading("pin", text="PIN")
        self.dir_tree.heading("balance", text="Current Balance ($)")
        self.dir_tree.heading("deposited", text="Total Deposited ($)")
        self.dir_tree.heading("withdrawn", text="Total Withdrawn ($)")
        self.dir_tree.heading("tx_count", text="Transactions")
        self.dir_tree.heading("date", text="Registration Date")

        self.dir_tree.column("acc", width=105, anchor="center")
        self.dir_tree.column("name", width=160, anchor="w")
        self.dir_tree.column("phone", width=120, anchor="center")
        self.dir_tree.column("pin", width=65, anchor="center")
        self.dir_tree.column("balance", width=130, anchor="e")
        self.dir_tree.column("deposited", width=130, anchor="e")
        self.dir_tree.column("withdrawn", width=130, anchor="e")
        self.dir_tree.column("tx_count", width=95, anchor="center")
        self.dir_tree.column("date", width=140, anchor="center")

        scroll_y = ttk.Scrollbar(tbl_container, orient="vertical", command=self.dir_tree.yview)
        self.dir_tree.configure(yscrollcommand=scroll_y.set)

        self.dir_tree.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

        action_bar = tk.Frame(parent, bg=BG_CANVAS, pady=10)
        action_bar.pack(fill="x")

        btn_dossier = tk.Button(action_bar, text="📜 View Full Statement & Dossier", font=("Segoe UI", 10, "bold"),
                                bg=PRIMARY_DARK, fg="#ffffff", relief="flat", cursor="hand2",
                                padx=12, pady=6, command=self.manager_view_dossier)
        btn_dossier.pack(side="left", padx=(0, 8))

        btn_edit = tk.Button(action_bar, text="✏️ Edit Customer Info", font=("Segoe UI", 10, "bold"),
                             bg=ACCENT_BLUE, fg="#ffffff", relief="flat", cursor="hand2",
                             padx=12, pady=6, command=self.manager_edit_account)
        btn_edit.pack(side="left", padx=(0, 8))

        btn_ops = tk.Button(action_bar, text="💵 Manager Deposit / Withdraw", font=("Segoe UI", 10, "bold"),
                            bg=SUCCESS_EMERALD, fg="#ffffff", relief="flat", cursor="hand2",
                            padx=12, pady=6, command=self.manager_cashier_operations)
        btn_ops.pack(side="left", padx=(0, 8))

        btn_del = tk.Button(action_bar, text="🗑️ Close Account", font=("Segoe UI", 10, "bold"),
                            bg=DANGER_CRIMSON, fg="#ffffff", relief="flat", cursor="hand2",
                            padx=12, pady=6, command=self.manager_delete_account)
        btn_del.pack(side="left")

        self.dir_tree.bind("<Double-1>", lambda e: self.manager_view_dossier())
        self.load_directory_data()

    def load_directory_data(self, search_query=None, filter_balance=None):
        for item in self.dir_tree.get_children():
            self.dir_tree.delete(item)

        accounts = database.get_all_accounts_detailed(search_query=search_query, filter_balance=filter_balance)

        for a in accounts:
            self.dir_tree.insert("", "end", values=(
                a["account_number"],
                a["name"],
                a["phone"],
                a["pin"],
                f"${a['balance']:,.2f}",
                f"${a['total_deposited']:,.2f}",
                f"${a['total_withdrawn']:,.2f}",
                f"{a['total_tx_count']} txs",
                a["created_at"]
            ))

    # -------------------------------------------------------------------------
    # MANAGER VIEW 3: GLOBAL SYSTEM TRANSACTION LEDGER
    # -------------------------------------------------------------------------
    def build_manager_ledger_view(self, parent):
        top_bar = tk.Frame(parent, bg=CARD_BG, relief="flat", highlightthickness=1,
                           highlightbackground=BORDER_LINE, padx=16, pady=10)
        top_bar.pack(fill="x", pady=(0, 12))

        tk.Label(top_bar, text="📜 Global Bank System Ledger (Audit Trail)", font=("Segoe UI", 13, "bold"),
                 bg=CARD_BG, fg=PRIMARY_DARK).pack(side="left")

        ctrl_box = tk.Frame(top_bar, bg=CARD_BG)
        ctrl_box.pack(side="right")

        tk.Label(ctrl_box, text="Filter Type:", font=("Segoe UI", 9, "bold"), bg=CARD_BG, fg=TEXT_MAIN).pack(side="left", padx=(0, 4))
        type_var = tk.StringVar(value="All")
        cmb_type = ttk.Combobox(ctrl_box, textvariable=type_var, values=["All", "Deposit", "Withdrawal", "Initial Deposit"],
                                state="readonly", width=14)
        cmb_type.pack(side="left", padx=(0, 10))

        tk.Label(ctrl_box, text="Search Account/Name:", font=("Segoe UI", 9, "bold"), bg=CARD_BG, fg=TEXT_MAIN).pack(side="left", padx=(0, 4))
        ent_ledger_search = tk.Entry(ctrl_box, font=("Segoe UI", 10), bg="#f8fafc", relief="solid", bd=1, width=16)
        ent_ledger_search.pack(side="left", ipady=3, padx=(0, 6))

        def apply_ledger_filter():
            t_filter = type_var.get()
            q = ent_ledger_search.get().strip()
            self.load_ledger_data(filter_type=t_filter, search_query=q)

        btn_apply = tk.Button(ctrl_box, text="Apply", font=("Segoe UI", 9, "bold"),
                              bg=ACCENT_INDIGO, fg="#ffffff", relief="flat", cursor="hand2",
                              padx=10, pady=2, command=apply_ledger_filter)
        btn_apply.pack(side="left")

        cmb_type.bind("<<ComboboxSelected>>", lambda e: apply_ledger_filter())
        ent_ledger_search.bind("<Return>", lambda e: apply_ledger_filter())

        tbl_container = tk.Frame(parent, bg=CARD_BG, relief="flat", highlightthickness=1,
                                 highlightbackground=BORDER_LINE)
        tbl_container.pack(fill="both", expand=True)

        l_cols = ("id", "time", "acc", "customer", "type", "amount", "balance_after")
        self.ledger_tree = ttk.Treeview(tbl_container, columns=l_cols, show="headings", selectmode="browse")

        self.ledger_tree.heading("id", text="Tx ID")
        self.ledger_tree.heading("time", text="Date & Time")
        self.ledger_tree.heading("acc", text="Account No.")
        self.ledger_tree.heading("customer", text="Customer Name")
        self.ledger_tree.heading("type", text="Transaction Type")
        self.ledger_tree.heading("amount", text="Amount ($)")
        self.ledger_tree.heading("balance_after", text="Balance After ($)")

        self.ledger_tree.column("id", width=65, anchor="center")
        self.ledger_tree.column("time", width=150, anchor="center")
        self.ledger_tree.column("acc", width=110, anchor="center")
        self.ledger_tree.column("customer", width=180, anchor="w")
        self.ledger_tree.column("type", width=130, anchor="center")
        self.ledger_tree.column("amount", width=120, anchor="e")
        self.ledger_tree.column("balance_after", width=130, anchor="e")

        scroll_l = ttk.Scrollbar(tbl_container, orient="vertical", command=self.ledger_tree.yview)
        self.ledger_tree.configure(yscrollcommand=scroll_l.set)

        self.ledger_tree.pack(side="left", fill="both", expand=True)
        scroll_l.pack(side="right", fill="y")

        self.ledger_tree.tag_configure("deposit", foreground="#047857")
        self.ledger_tree.tag_configure("withdrawal", foreground="#b91c1c")

        self.load_ledger_data()

    def load_ledger_data(self, filter_type=None, search_query=None):
        for item in self.ledger_tree.get_children():
            self.ledger_tree.delete(item)

        transactions = database.get_global_transactions(limit=250, filter_type=filter_type, search_query=search_query)

        for t in transactions:
            tag = "deposit" if "Deposit" in t["type"] else "withdrawal"
            amt_str = f"+${t['amount']:,.2f}" if "Deposit" in t["type"] else f"-${t['amount']:,.2f}"

            self.ledger_tree.insert("", "end", values=(
                f"#{t['id']}",
                t["timestamp"],
                t["account_number"],
                t["customer_name"],
                t["type"],
                amt_str,
                f"${t['balance_after']:,.2f}"
            ), tags=(tag,))

    # -------------------------------------------------------------------------
    # MANAGER VIEW 4: 🔐 SECURITY & LOGIN AUDIT HISTORY
    # -------------------------------------------------------------------------
    def build_manager_security_view(self, parent):
        top_bar = tk.Frame(parent, bg=CARD_BG, relief="flat", highlightthickness=1,
                           highlightbackground=BORDER_LINE, padx=16, pady=10)
        top_bar.pack(fill="x", pady=(0, 12))

        tk.Label(top_bar, text="🔐 Security & Login Audit History", font=("Segoe UI", 13, "bold"),
                 bg=CARD_BG, fg=PRIMARY_DARK).pack(side="left")

        ctrl_box = tk.Frame(top_bar, bg=CARD_BG)
        ctrl_box.pack(side="right")

        # Filter by Role
        tk.Label(ctrl_box, text="Role:", font=("Segoe UI", 9, "bold"), bg=CARD_BG, fg=TEXT_MAIN).pack(side="left", padx=(0, 4))
        role_var = tk.StringVar(value="All")
        cmb_role = ttk.Combobox(ctrl_box, textvariable=role_var, values=["All", "Customer", "Bank Manager"],
                                state="readonly", width=12)
        cmb_role.pack(side="left", padx=(0, 8))

        # Filter by Status
        tk.Label(ctrl_box, text="Status:", font=("Segoe UI", 9, "bold"), bg=CARD_BG, fg=TEXT_MAIN).pack(side="left", padx=(0, 4))
        status_var = tk.StringVar(value="All")
        cmb_status = ttk.Combobox(ctrl_box, textvariable=status_var, values=["All", "SUCCESS", "FAILED"],
                                  state="readonly", width=10)
        cmb_status.pack(side="left", padx=(0, 8))

        # Search Query
        tk.Label(ctrl_box, text="Search:", font=("Segoe UI", 9, "bold"), bg=CARD_BG, fg=TEXT_MAIN).pack(side="left", padx=(0, 4))
        ent_sec_search = tk.Entry(ctrl_box, font=("Segoe UI", 10), bg="#f8fafc", relief="solid", bd=1, width=16)
        ent_sec_search.pack(side="left", ipady=3, padx=(0, 6))

        def apply_security_filter():
            r = role_var.get()
            s = status_var.get()
            q = ent_sec_search.get().strip()
            self.load_security_data(filter_role=r, filter_status=s, search_query=q)

        btn_filter = tk.Button(ctrl_box, text="Filter", font=("Segoe UI", 9, "bold"),
                               bg=PURPLE_COLOR, fg="#ffffff", relief="flat", cursor="hand2",
                               padx=10, pady=2, command=apply_security_filter)
        btn_filter.pack(side="left")

        cmb_role.bind("<<ComboboxSelected>>", lambda e: apply_security_filter())
        cmb_status.bind("<<ComboboxSelected>>", lambda e: apply_security_filter())
        ent_sec_search.bind("<Return>", lambda e: apply_security_filter())

        # Security Tree Table
        tbl_container = tk.Frame(parent, bg=CARD_BG, relief="flat", highlightthickness=1,
                                 highlightbackground=BORDER_LINE)
        tbl_container.pack(fill="both", expand=True)

        s_cols = ("id", "time", "user_id", "name", "role", "status", "reason")
        self.sec_tree = ttk.Treeview(tbl_container, columns=s_cols, show="headings", selectmode="browse")

        self.sec_tree.heading("id", text="Log ID")
        self.sec_tree.heading("time", text="Timestamp")
        self.sec_tree.heading("user_id", text="Account / Username")
        self.sec_tree.heading("name", text="User / Holder Name")
        self.sec_tree.heading("role", text="Role")
        self.sec_tree.heading("status", text="Login Status")
        self.sec_tree.heading("reason", text="Audit Details / Notes")

        self.sec_tree.column("id", width=65, anchor="center")
        self.sec_tree.column("time", width=150, anchor="center")
        self.sec_tree.column("user_id", width=140, anchor="center")
        self.sec_tree.column("name", width=160, anchor="w")
        self.sec_tree.column("role", width=120, anchor="center")
        self.sec_tree.column("status", width=110, anchor="center")
        self.sec_tree.column("reason", width=220, anchor="w")

        scroll_s = ttk.Scrollbar(tbl_container, orient="vertical", command=self.sec_tree.yview)
        self.sec_tree.configure(yscrollcommand=scroll_s.set)

        self.sec_tree.pack(side="left", fill="both", expand=True)
        scroll_s.pack(side="right", fill="y")

        self.sec_tree.tag_configure("success", foreground="#047857")
        self.sec_tree.tag_configure("failed", foreground="#dc2626")

        self.load_security_data()

    def load_security_data(self, filter_role=None, filter_status=None, search_query=None):
        for item in self.sec_tree.get_children():
            self.sec_tree.delete(item)

        logs = database.get_login_history(limit=250, search_query=search_query, filter_role=filter_role, filter_status=filter_status)

        for l in logs:
            tag = "success" if l["status"] == "SUCCESS" else "failed"
            status_text = "✓ SUCCESS" if l["status"] == "SUCCESS" else "✗ FAILED"

            self.sec_tree.insert("", "end", values=(
                f"#{l['id']}",
                l["timestamp"],
                l["user_identifier"],
                l["user_name"],
                l["role"],
                status_text,
                l["failure_reason"]
            ), tags=(tag,))

    # -------------------------------------------------------------------------
    # MANAGER ACTION MODALS (DOSSIER, EDIT, CASHIER, OPEN)
    # -------------------------------------------------------------------------
    def manager_view_dossier(self):
        sel = self.dir_tree.selection()
        if not sel:
            messagebox.showwarning("Selection Required", "Please select a customer account from the directory table.")
            return

        vals = self.dir_tree.item(sel[0], "values")
        acc_num = vals[0]
        acc_info = database.get_account(acc_num)
        if not acc_info:
            messagebox.showerror("Error", "Account details not found.")
            return

        modal = tk.Toplevel(self)
        modal.title(f"Customer Dossier — Account #{acc_num} ({acc_info['name']})")
        modal.geometry("820x600")
        modal.minsize(720, 520)
        modal.configure(bg=BG_CANVAS)

        hdr = tk.Frame(modal, bg=PRIMARY_DARK, padx=20, pady=14)
        hdr.pack(fill="x")

        tk.Label(hdr, text=f"👤 Customer Dossier: {acc_info['name']}", font=("Segoe UI", 13, "bold"),
                 bg=PRIMARY_DARK, fg="#ffffff").pack(side="left")
        tk.Label(hdr, text=f"Current Balance: ${acc_info['balance']:,.2f}", font=("Segoe UI", 12, "bold"),
                 bg=PRIMARY_DARK, fg=SUCCESS_EMERALD).pack(side="right")

        stats_box = tk.Frame(modal, bg=CARD_BG, relief="flat", highlightthickness=1,
                             highlightbackground=BORDER_LINE, padx=16, pady=10)
        stats_box.pack(fill="x", padx=16, pady=12)

        last_login_time = database.get_customer_last_login(acc_num)
        tk.Label(stats_box, text=f"Account No: {acc_info['account_number']}  |  Phone: {acc_info['phone']}  |  PIN: {acc_info['pin']}\nOpened: {acc_info['created_at']}  |  Last Recorded Login: {last_login_time}",
                 font=("Segoe UI", 9, "bold"), bg=CARD_BG, fg=TEXT_MAIN).pack(anchor="w")

        # Dossier Notebook (Statement + Login History)
        dossier_nb = ttk.Notebook(modal)
        dossier_nb.pack(fill="both", expand=True, padx=16, pady=(0, 12))

        # Statement Tab
        stmt_tab = tk.Frame(dossier_nb, bg=CARD_BG, padx=10, pady=8)
        dossier_nb.add(stmt_tab, text="  📜 Transaction Statement  ")

        s_cols = ("time", "type", "amount", "balance")
        tree_stmt = ttk.Treeview(stmt_tab, columns=s_cols, show="headings", selectmode="browse")
        tree_stmt.heading("time", text="Date & Time")
        tree_stmt.heading("type", text="Type")
        tree_stmt.heading("amount", text="Amount ($)")
        tree_stmt.heading("balance", text="Resulting Balance ($)")

        tree_stmt.column("time", width=160, anchor="center")
        tree_stmt.column("type", width=120, anchor="center")
        tree_stmt.column("amount", width=120, anchor="e")
        tree_stmt.column("balance", width=130, anchor="e")

        s_scroll = ttk.Scrollbar(stmt_tab, orient="vertical", command=tree_stmt.yview)
        tree_stmt.configure(yscrollcommand=s_scroll.set)

        tree_stmt.pack(side="left", fill="both", expand=True)
        s_scroll.pack(side="right", fill="y")

        tree_stmt.tag_configure("deposit", foreground="#047857")
        tree_stmt.tag_configure("withdrawal", foreground="#b91c1c")

        txs = database.get_transactions(acc_num)
        for t in txs:
            tag = "deposit" if "Deposit" in t["type"] else "withdrawal"
            amt_s = f"+${t['amount']:,.2f}" if "Deposit" in t["type"] else f"-${t['amount']:,.2f}"
            tree_stmt.insert("", "end", values=(
                t["timestamp"],
                t["type"],
                amt_s,
                f"${t['balance_after']:,.2f}"
            ), tags=(tag,))

        # Customer Login History Tab
        log_tab = tk.Frame(dossier_nb, bg=CARD_BG, padx=10, pady=8)
        dossier_nb.add(log_tab, text="  🔐 Login History Audit  ")

        l_cols = ("time", "status", "notes")
        tree_log = ttk.Treeview(log_tab, columns=l_cols, show="headings", selectmode="browse")
        tree_log.heading("time", text="Timestamp")
        tree_log.heading("status", text="Login Status")
        tree_log.heading("notes", text="Audit Details")

        tree_log.column("time", width=160, anchor="center")
        tree_log.column("status", width=120, anchor="center")
        tree_log.column("notes", width=240, anchor="w")

        l_scroll = ttk.Scrollbar(log_tab, orient="vertical", command=tree_log.yview)
        tree_log.configure(yscrollcommand=l_scroll.set)

        tree_log.pack(side="left", fill="both", expand=True)
        l_scroll.pack(side="right", fill="y")

        tree_log.tag_configure("success", foreground="#047857")
        tree_log.tag_configure("failed", foreground="#dc2626")

        cust_logs = database.get_login_history(search_query=acc_num)
        for cl in cust_logs:
            tag = "success" if cl["status"] == "SUCCESS" else "failed"
            st = "✓ SUCCESS" if cl["status"] == "SUCCESS" else "✗ FAILED"
            tree_log.insert("", "end", values=(cl["timestamp"], st, cl["failure_reason"]), tags=(tag,))

        tk.Button(modal, text="Close Dossier", font=("Segoe UI", 9, "bold"),
                  bg="#e2e8f0", fg=PRIMARY_DARK, relief="flat", cursor="hand2",
                  command=modal.destroy, padx=14, pady=5).pack(pady=(0, 10))

    def manager_edit_account(self):
        sel = self.dir_tree.selection()
        if not sel:
            messagebox.showwarning("Selection Required", "Please select a customer account to edit.")
            return

        vals = self.dir_tree.item(sel[0], "values")
        acc_num = vals[0]
        acc_info = database.get_account(acc_num)

        modal = tk.Toplevel(self)
        modal.title(f"Edit Account #{acc_num}")
        modal.geometry("450x380")
        modal.configure(bg=CARD_BG)

        tk.Label(modal, text=f"Edit Customer Account #{acc_num}", font=("Segoe UI", 13, "bold"),
                 bg=CARD_BG, fg=PRIMARY_DARK).pack(pady=12)

        form = tk.Frame(modal, bg=CARD_BG, padx=25)
        form.pack(fill="both", expand=True)

        tk.Label(form, text="Full Name", font=("Segoe UI", 9, "bold"), bg=CARD_BG, fg=TEXT_MAIN).pack(anchor="w", pady=(4, 2))
        ent_name = tk.Entry(form, font=("Segoe UI", 10), bg="#f8fafc", relief="solid", bd=1)
        ent_name.insert(0, acc_info["name"])
        ent_name.pack(fill="x", ipady=4, pady=(0, 8))

        tk.Label(form, text="Phone Number", font=("Segoe UI", 9, "bold"), bg=CARD_BG, fg=TEXT_MAIN).pack(anchor="w", pady=(4, 2))
        ent_phone = tk.Entry(form, font=("Segoe UI", 10), bg="#f8fafc", relief="solid", bd=1)
        ent_phone.insert(0, acc_info["phone"])
        ent_phone.pack(fill="x", ipady=4, pady=(0, 8))

        tk.Label(form, text="4-Digit PIN", font=("Segoe UI", 9, "bold"), bg=CARD_BG, fg=TEXT_MAIN).pack(anchor="w", pady=(4, 2))
        ent_pin = tk.Entry(form, font=("Segoe UI", 10), bg="#f8fafc", relief="solid", bd=1)
        ent_pin.insert(0, acc_info["pin"])
        ent_pin.pack(fill="x", ipady=4, pady=(0, 16))

        def save_changes():
            n = ent_name.get().strip()
            p = ent_phone.get().strip()
            pi = ent_pin.get().strip()
            success, msg = database.update_account(acc_num, n, p, pi)
            if success:
                messagebox.showinfo("Saved", msg)
                modal.destroy()
                self.load_directory_data()
            else:
                messagebox.showerror("Error", msg)

        tk.Button(modal, text="Save Changes ✓", font=("Segoe UI", 10, "bold"),
                  bg=SUCCESS_EMERALD, fg="#ffffff", relief="flat", cursor="hand2",
                  command=save_changes).pack(fill="x", padx=25, ipady=6, pady=(0, 16))

    def manager_cashier_operations(self):
        sel = self.dir_tree.selection()
        if not sel:
            messagebox.showwarning("Selection Required", "Please select a customer account for cashier operations.")
            return

        vals = self.dir_tree.item(sel[0], "values")
        acc_num = vals[0]
        name = vals[1]

        modal = tk.Toplevel(self)
        modal.title(f"Manager Cashier — Account #{acc_num}")
        modal.geometry("460x360")
        modal.configure(bg=CARD_BG)

        tk.Label(modal, text=f"Manager Cashier: {name}", font=("Segoe UI", 13, "bold"),
                 bg=CARD_BG, fg=PRIMARY_DARK).pack(pady=(14, 2))
        tk.Label(modal, text=f"Account #{acc_num}", font=("Segoe UI", 10),
                 bg=CARD_BG, fg=TEXT_MUTED).pack(pady=(0, 12))

        box = tk.Frame(modal, bg=CARD_BG, padx=25)
        box.pack(fill="both", expand=True)

        tk.Label(box, text="Transaction Type:", font=("Segoe UI", 9, "bold"), bg=CARD_BG, fg=TEXT_MAIN).pack(anchor="w", pady=(4, 2))
        op_var = tk.StringVar(value="Deposit")
        cmb_op = ttk.Combobox(box, textvariable=op_var, values=["Deposit", "Withdrawal"], state="readonly")
        cmb_op.pack(fill="x", ipady=3, pady=(0, 10))

        tk.Label(box, text="Amount ($):", font=("Segoe UI", 9, "bold"), bg=CARD_BG, fg=TEXT_MAIN).pack(anchor="w", pady=(4, 2))
        ent_amt = tk.Entry(box, font=("Segoe UI", 11), bg="#f8fafc", relief="solid", bd=1)
        ent_amt.pack(fill="x", ipady=5, pady=(0, 16))

        def execute_op():
            op = op_var.get()
            amt_str = ent_amt.get().strip()
            try:
                amt = float(amt_str)
                if amt <= 0:
                    messagebox.showwarning("Invalid Amount", "Amount must be greater than $0.00.")
                    return
            except ValueError:
                messagebox.showwarning("Invalid Amount", "Please enter a valid numeric amount.")
                return

            if op == "Deposit":
                ok, res = database.deposit(acc_num, amt, note="Manager Deposit")
            else:
                ok, res = database.withdraw(acc_num, amt, note="Manager Withdrawal")

            if ok:
                messagebox.showinfo("Success", f"{op} of ${amt:,.2f} completed successfully!\nNew Balance: ${res:,.2f}")
                modal.destroy()
                self.load_directory_data()
            else:
                messagebox.showerror("Failed", str(res))

        tk.Button(modal, text="Execute Transaction ✓", font=("Segoe UI", 10, "bold"),
                  bg=ACCENT_INDIGO, fg="#ffffff", relief="flat", cursor="hand2",
                  command=execute_op).pack(fill="x", padx=25, ipady=6, pady=(0, 16))

    def manager_delete_account(self):
        sel = self.dir_tree.selection()
        if not sel:
            messagebox.showwarning("Selection Required", "Please select an account to close.")
            return

        vals = self.dir_tree.item(sel[0], "values")
        acc_num = vals[0]
        name = vals[1]

        if messagebox.askyesno("Confirm Account Closure",
                               f"⚠️ Are you sure you want to permanently close Account #{acc_num} ({name})?\n\nAll data will be purged."):
            ok, msg = database.delete_account(acc_num)
            if ok:
                messagebox.showinfo("Account Closed", msg)
                self.load_directory_data()
            else:
                messagebox.showerror("Error", msg)

    def open_manager_new_account_modal(self):
        modal = tk.Toplevel(self)
        modal.title("Open Customer Account as Manager")
        modal.geometry("480x420")
        modal.configure(bg=CARD_BG)

        tk.Label(modal, text="➕ Open Customer Bank Account", font=("Segoe UI", 13, "bold"),
                 bg=CARD_BG, fg=PRIMARY_DARK).pack(pady=(14, 10))

        form = tk.Frame(modal, bg=CARD_BG, padx=25)
        form.pack(fill="both", expand=True)

        tk.Label(form, text="Customer Full Name", font=("Segoe UI", 9, "bold"), bg=CARD_BG, fg=TEXT_MAIN).pack(anchor="w")
        ent_n = tk.Entry(form, font=("Segoe UI", 10), bg="#f8fafc", relief="solid", bd=1)
        ent_n.pack(fill="x", ipady=4, pady=(2, 8))

        tk.Label(form, text="Phone Number", font=("Segoe UI", 9, "bold"), bg=CARD_BG, fg=TEXT_MAIN).pack(anchor="w")
        ent_p = tk.Entry(form, font=("Segoe UI", 10), bg="#f8fafc", relief="solid", bd=1)
        ent_p.pack(fill="x", ipady=4, pady=(2, 8))

        tk.Label(form, text="4-Digit Security PIN", font=("Segoe UI", 9, "bold"), bg=CARD_BG, fg=TEXT_MAIN).pack(anchor="w")
        ent_pi = tk.Entry(form, font=("Segoe UI", 10), bg="#f8fafc", relief="solid", bd=1)
        ent_pi.insert(0, "1234")
        ent_pi.pack(fill="x", ipady=4, pady=(2, 8))

        tk.Label(form, text="Initial Deposit ($)", font=("Segoe UI", 9, "bold"), bg=CARD_BG, fg=TEXT_MAIN).pack(anchor="w")
        ent_d = tk.Entry(form, font=("Segoe UI", 10), bg="#f8fafc", relief="solid", bd=1)
        ent_d.insert(0, "200.00")
        ent_d.pack(fill="x", ipady=4, pady=(2, 14))

        def create():
            n = ent_n.get().strip()
            p = ent_p.get().strip()
            pi = ent_pi.get().strip()
            d = ent_d.get().strip()
            try:
                d_val = float(d) if d else 0.0
            except ValueError:
                messagebox.showwarning("Error", "Invalid deposit.")
                return
            ok, msg, acc = database.create_account(n, p, pi, d_val)
            if ok:
                messagebox.showinfo("Success", f"Account created with Account No: {acc}!")
                modal.destroy()
                self.show_manager_portal_screen()
            else:
                messagebox.showerror("Error", msg)

        tk.Button(modal, text="Create Account ✓", font=("Segoe UI", 10, "bold"),
                  bg=SUCCESS_EMERALD, fg="#ffffff", relief="flat", cursor="hand2",
                  command=create).pack(fill="x", padx=25, ipady=6, pady=(0, 16))

    # =========================================================================
    # SCREEN 3: 💳 CUSTOMER ONLINE BANKING PORTAL
    # =========================================================================
    def show_customer_portal_screen(self):
        self.clear_container()

        # Top Nav
        nav = tk.Frame(self.container, bg=PRIMARY_DARK, height=65)
        nav.pack(fill="x", side="top")

        left = tk.Frame(nav, bg=PRIMARY_DARK)
        left.pack(side="left", padx=25, pady=12)

        tk.Label(left, text="🏦", font=("Segoe UI Emoji", 20), bg=PRIMARY_DARK, fg="#ffffff").pack(side="left", padx=(0, 8))
        tk.Label(left, text="APEX NATIONAL BANK", font=("Segoe UI", 15, "bold"), bg=PRIMARY_DARK, fg="#ffffff").pack(side="left")

        right = tk.Frame(nav, bg=PRIMARY_DARK)
        right.pack(side="right", padx=25, pady=12)

        tk.Label(right, text=f"👤 {self.current_user['name']}", font=("Segoe UI", 11, "bold"),
                 bg=PRIMARY_DARK, fg="#93c5fd").pack(side="left", padx=(0, 15))

        btn_logout = tk.Button(right, text="🚪 Logout", font=("Segoe UI", 9, "bold"),
                               bg="#334155", fg="#ffffff", activebackground=DANGER_CRIMSON,
                               activeforeground="#ffffff", relief="flat", padx=12, pady=4,
                               cursor="hand2", command=self.handle_logout)
        btn_logout.pack(side="left")

        # Body
        body = tk.Frame(self.container, bg=BG_CANVAS)
        body.pack(fill="both", expand=True, padx=30, pady=20)

        # Top Hero Card (Balance & Last Login)
        hero = tk.Frame(body, bg=CARD_BG, relief="flat", highlightthickness=1,
                        highlightbackground=BORDER_LINE, bd=0)
        hero.pack(fill="x", pady=(0, 16), ipady=12, padx=2)

        h_left = tk.Frame(hero, bg=CARD_BG)
        h_left.pack(side="left", padx=25, pady=5)

        tk.Label(h_left, text="TOTAL AVAILABLE BALANCE", font=("Segoe UI", 9, "bold"), bg=CARD_BG, fg=TEXT_MUTED).pack(anchor="w")
        self.lbl_cust_bal = tk.Label(h_left, text=f"${self.current_user['balance']:,.2f}",
                                     font=("Segoe UI", 26, "bold"), bg=CARD_BG, fg=SUCCESS_EMERALD)
        self.lbl_cust_bal.pack(anchor="w", pady=(2, 0))

        last_login_time = database.get_customer_last_login(self.current_user["account_number"])
        tk.Label(h_left, text=f"🔐 Last Login: {last_login_time}", font=("Segoe UI", 8), bg=CARD_BG, fg=TEXT_MUTED).pack(anchor="w", pady=(2, 0))

        h_right = tk.Frame(hero, bg=CARD_BG)
        h_right.pack(side="right", padx=25, pady=5)

        tk.Label(h_right, text=f"Account No: {self.current_user['account_number']}", font=("Segoe UI", 11, "bold"),
                 bg=CARD_BG, fg=PRIMARY_DARK).pack(anchor="e")
        tk.Label(h_right, text=f"Registered Phone: {self.current_user['phone']}", font=("Segoe UI", 9),
                 bg=CARD_BG, fg=TEXT_MUTED).pack(anchor="e")
        tk.Label(h_right, text=f"Member Since: {self.current_user['created_at'].split()[0]}", font=("Segoe UI", 8),
                 bg=CARD_BG, fg=TEXT_MUTED).pack(anchor="e", pady=(2, 0))

        # Split Operations & Statement
        split = tk.Frame(body, bg=BG_CANVAS)
        split.pack(fill="both", expand=True)

        left_ops = tk.Frame(split, bg=BG_CANVAS, width=380)
        left_ops.pack(side="left", fill="both", padx=(0, 10))
        left_ops.pack_propagate(False)

        # Deposit Card
        self.build_cust_deposit_card(left_ops)

        # Withdraw Card
        self.build_cust_withdraw_card(left_ops)

        # Statement Card (Right)
        right_stmt = tk.Frame(split, bg=CARD_BG, relief="flat", highlightthickness=1, highlightbackground=BORDER_LINE)
        right_stmt.pack(side="right", fill="both", expand=True, padx=(10, 0))

        self.build_cust_statement_card(right_stmt)

    def build_cust_deposit_card(self, parent):
        card = tk.Frame(parent, bg=CARD_BG, relief="flat", highlightthickness=1,
                        highlightbackground=BORDER_LINE, padx=18, pady=14)
        card.pack(fill="x", pady=(0, 12))

        tk.Label(card, text="💰 Deposit Money", font=("Segoe UI", 12, "bold"), bg=CARD_BG, fg=PRIMARY_DARK).pack(anchor="w", pady=(0, 8))

        inp_frame = tk.Frame(card, bg=CARD_BG)
        inp_frame.pack(fill="x", pady=(0, 8))

        tk.Label(inp_frame, text="Amount ($):", font=("Segoe UI", 10, "bold"), bg=CARD_BG, fg=TEXT_MAIN).pack(side="left", padx=(0, 8))
        ent_dep = tk.Entry(inp_frame, font=("Segoe UI", 11), bg="#f8fafc", relief="solid", bd=1)
        ent_dep.pack(side="left", fill="x", expand=True, ipady=4)

        presets = tk.Frame(card, bg=CARD_BG)
        presets.pack(fill="x", pady=(0, 10))

        for amt in [50, 100, 500, 1000]:
            tk.Button(presets, text=f"+${amt}", font=("Segoe UI", 8, "bold"), bg="#f1f5f9", fg=PRIMARY_DARK,
                      relief="flat", cursor="hand2", padx=6, pady=2,
                      command=lambda a=amt: [ent_dep.delete(0, tk.END), ent_dep.insert(0, str(a))]).pack(side="left", padx=2)

        def do_deposit():
            amt_str = ent_dep.get().strip()
            try:
                amt = float(amt_str)
                if amt <= 0:
                    messagebox.showwarning("Error", "Amount must be > $0.00.")
                    return
            except ValueError:
                messagebox.showwarning("Error", "Please enter a valid numeric amount.")
                return

            ok, res = database.deposit(self.current_user["account_number"], amt)
            if ok:
                ent_dep.delete(0, tk.END)
                self.refresh_cust_portal()
                messagebox.showinfo("Success", f"Deposited ${amt:,.2f}!\nNew Balance: ${res:,.2f}")
            else:
                messagebox.showerror("Error", str(res))

        btn = tk.Button(card, text="Confirm Deposit", font=("Segoe UI", 10, "bold"),
                        bg=SUCCESS_EMERALD, fg="#ffffff", relief="flat", cursor="hand2", command=do_deposit)
        btn.pack(fill="x", ipady=6)
        ent_dep.bind("<Return>", lambda e: do_deposit())

    def build_cust_withdraw_card(self, parent):
        card = tk.Frame(parent, bg=CARD_BG, relief="flat", highlightthickness=1,
                        highlightbackground=BORDER_LINE, padx=18, pady=14)
        card.pack(fill="x")

        tk.Label(card, text="💳 Withdraw Money", font=("Segoe UI", 12, "bold"), bg=CARD_BG, fg=PRIMARY_DARK).pack(anchor="w", pady=(0, 8))

        inp_frame = tk.Frame(card, bg=CARD_BG)
        inp_frame.pack(fill="x", pady=(0, 8))

        tk.Label(inp_frame, text="Amount ($):", font=("Segoe UI", 10, "bold"), bg=CARD_BG, fg=TEXT_MAIN).pack(side="left", padx=(0, 8))
        ent_w = tk.Entry(inp_frame, font=("Segoe UI", 11), bg="#f8fafc", relief="solid", bd=1)
        ent_w.pack(side="left", fill="x", expand=True, ipady=4)

        presets = tk.Frame(card, bg=CARD_BG)
        presets.pack(fill="x", pady=(0, 10))

        for amt in [20, 50, 100, 200]:
            tk.Button(presets, text=f"${amt}", font=("Segoe UI", 8, "bold"), bg="#f1f5f9", fg=PRIMARY_DARK,
                      relief="flat", cursor="hand2", padx=8, pady=2,
                      command=lambda a=amt: [ent_w.delete(0, tk.END), ent_w.insert(0, str(a))]).pack(side="left", padx=2)

        def do_withdraw():
            amt_str = ent_w.get().strip()
            try:
                amt = float(amt_str)
                if amt <= 0:
                    messagebox.showwarning("Error", "Amount must be > $0.00.")
                    return
            except ValueError:
                messagebox.showwarning("Error", "Please enter a valid numeric amount.")
                return

            if amt > self.current_user["balance"]:
                messagebox.showwarning("Insufficient Funds",
                                       f"❌ Insufficient balance!\n\nAvailable: ${self.current_user['balance']:,.2f}\nRequested: ${amt:,.2f}")
                return

            ok, res = database.withdraw(self.current_user["account_number"], amt)
            if ok:
                ent_w.delete(0, tk.END)
                self.refresh_cust_portal()
                messagebox.showinfo("Success", f"Withdrew ${amt:,.2f}!\nNew Balance: ${res:,.2f}")
            else:
                messagebox.showerror("Error", str(res))

        btn = tk.Button(card, text="Confirm Withdrawal", font=("Segoe UI", 10, "bold"),
                        bg=DANGER_CRIMSON, fg="#ffffff", relief="flat", cursor="hand2", command=do_withdraw)
        btn.pack(fill="x", ipady=6)
        ent_w.bind("<Return>", lambda e: do_withdraw())

    def build_cust_statement_card(self, parent):
        hdr = tk.Frame(parent, bg=CARD_BG, padx=16, pady=12)
        hdr.pack(fill="x")

        tk.Label(hdr, text="📊 Personal Statement History", font=("Segoe UI", 12, "bold"),
                 bg=CARD_BG, fg=PRIMARY_DARK).pack(side="left")

        btn_box = tk.Frame(hdr, bg=CARD_BG)
        btn_box.pack(side="right")

        tk.Button(btn_box, text="🔐 My Login Activity", font=("Segoe UI", 9, "bold"), bg="#f1f5f9",
                  fg=PURPLE_COLOR, relief="flat", cursor="hand2", padx=8, pady=4,
                  command=self.customer_view_my_login_history).pack(side="left", padx=(0, 6))

        tk.Button(btn_box, text="🔄 Refresh Balance", font=("Segoe UI", 9, "bold"), bg="#f1f5f9",
                  fg=PRIMARY_DARK, relief="flat", cursor="hand2", padx=8, pady=4,
                  command=self.refresh_cust_portal).pack(side="left")

        tbl_frame = tk.Frame(parent, bg=CARD_BG, padx=14, pady=6)
        tbl_frame.pack(fill="both", expand=True)

        cols = ("datetime", "type", "amount", "balance")
        self.cust_tree = ttk.Treeview(tbl_frame, columns=cols, show="headings", selectmode="browse")

        self.cust_tree.heading("datetime", text="Date & Time")
        self.cust_tree.heading("type", text="Type")
        self.cust_tree.heading("amount", text="Amount ($)")
        self.cust_tree.heading("balance", text="Balance After ($)")

        self.cust_tree.column("datetime", width=150, anchor="center")
        self.cust_tree.column("type", width=110, anchor="center")
        self.cust_tree.column("amount", width=100, anchor="e")
        self.cust_tree.column("balance", width=120, anchor="e")

        sc = ttk.Scrollbar(tbl_frame, orient="vertical", command=self.cust_tree.yview)
        self.cust_tree.configure(yscrollcommand=sc.set)

        self.cust_tree.pack(side="left", fill="both", expand=True)
        sc.pack(side="right", fill="y")

        self.cust_tree.tag_configure("deposit", foreground="#047857")
        self.cust_tree.tag_configure("withdrawal", foreground="#b91c1c")

        self.load_cust_transactions()

    def customer_view_my_login_history(self):
        """Shows customer their personal login audit trail."""
        modal = tk.Toplevel(self)
        modal.title("My Security & Login Activity")
        modal.geometry("640x440")
        modal.configure(bg=CARD_BG)

        tk.Label(modal, text=f"🔐 Security & Login Activity for Acc #{self.current_user['account_number']}",
                 font=("Segoe UI", 12, "bold"), bg=CARD_BG, fg=PRIMARY_DARK).pack(pady=12)

        tbl_frame = tk.Frame(modal, bg=CARD_BG, padx=14, pady=8)
        tbl_frame.pack(fill="both", expand=True)

        cols = ("time", "status", "notes")
        tree_log = ttk.Treeview(tbl_frame, columns=cols, show="headings", selectmode="browse")
        tree_log.heading("time", text="Date & Time")
        tree_log.heading("status", text="Status")
        tree_log.heading("notes", text="Audit Details")

        tree_log.column("time", width=160, anchor="center")
        tree_log.column("status", width=120, anchor="center")
        tree_log.column("notes", width=260, anchor="w")

        sc = ttk.Scrollbar(tbl_frame, orient="vertical", command=tree_log.yview)
        tree_log.configure(yscrollcommand=sc.set)

        tree_log.pack(side="left", fill="both", expand=True)
        sc.pack(side="right", fill="y")

        tree_log.tag_configure("success", foreground="#047857")
        tree_log.tag_configure("failed", foreground="#dc2626")

        logs = database.get_login_history(search_query=self.current_user["account_number"])
        for l in logs:
            tag = "success" if l["status"] == "SUCCESS" else "failed"
            st = "✓ SUCCESS" if l["status"] == "SUCCESS" else "✗ FAILED"
            tree_log.insert("", "end", values=(l["timestamp"], st, l["failure_reason"]), tags=(tag,))

        tk.Button(modal, text="Close", font=("Segoe UI", 9, "bold"),
                  bg="#e2e8f0", fg=PRIMARY_DARK, relief="flat", cursor="hand2",
                  command=modal.destroy, padx=12, pady=4).pack(pady=10)

    def load_cust_transactions(self):
        for item in self.cust_tree.get_children():
            self.cust_tree.delete(item)

        txs = database.get_transactions(self.current_user["account_number"])
        for t in txs:
            tag = "deposit" if "Deposit" in t["type"] else "withdrawal"
            amt_s = f"+${t['amount']:,.2f}" if "Deposit" in t["type"] else f"-${t['amount']:,.2f}"
            self.cust_tree.insert("", "end", values=(
                t["timestamp"],
                t["type"],
                amt_s,
                f"${t['balance_after']:,.2f}"
            ), tags=(tag,))

    def refresh_cust_portal(self):
        upd = database.get_account(self.current_user["account_number"])
        if upd:
            self.current_user = upd
            self.lbl_cust_bal.config(text=f"${self.current_user['balance']:,.2f}")
            self.load_cust_transactions()

    def handle_logout(self):
        if messagebox.askyesno("Confirm Exit", "Are you sure you want to log out?"):
            self.current_user = None
            self.current_admin = None
            self.show_auth_screen()


# =============================================================================
# APPLICATION LAUNCHER
# =============================================================================
if __name__ == "__main__":
    app = BankManagementApp()
    app.mainloop()
