"""Schema and connection helpers."""

import sqlite3


def connect(path=":memory:"):
    db = sqlite3.connect(path)
    db.executescript(
        """
        CREATE TABLE tenants (id INTEGER PRIMARY KEY, name TEXT);
        CREATE TABLE users (id INTEGER PRIMARY KEY, tenant_id INTEGER, email TEXT,
                            display_name TEXT, role TEXT DEFAULT 'member');
        CREATE TABLE customers (id INTEGER PRIMARY KEY, tenant_id INTEGER, name TEXT);
        CREATE TABLE invoices (id INTEGER PRIMARY KEY, tenant_id INTEGER, customer_id INTEGER,
                               number TEXT, amount_cents INTEGER, issued_at TEXT);
        CREATE TABLE coupons (code TEXT PRIMARY KEY, tenant_id INTEGER, uses_left INTEGER);
        CREATE TABLE redemptions (id INTEGER PRIMARY KEY, user_id INTEGER, code TEXT);
        """
    )
    return db
