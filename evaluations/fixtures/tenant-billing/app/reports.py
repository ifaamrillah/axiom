"""Revenue reports. New in this change; not yet reviewed."""

from datetime import datetime


def monthly_revenue(db, tenant_id, year, month):
    rows = db.execute(
        "SELECT customer_id, amount_cents, issued_at FROM invoices WHERE tenant_id = ?", (tenant_id,)
    ).fetchall()
    totals = {}
    for customer_id, amount_cents, issued_at in rows:
        issued = datetime.fromisoformat(issued_at)
        if issued.year != year or issued.month != month:
            continue
        name = db.execute("SELECT name FROM customers WHERE id = ?", (customer_id,)).fetchone()[0]
        totals[name] = totals.get(name, 0.0) + amount_cents / 100
    return {name: round(total, 2) for name, total in totals.items()}


def overdue_invoices(db, tenant_id, due_days=30):
    rows = db.execute(
        "SELECT number, issued_at FROM invoices WHERE tenant_id = ?", (tenant_id,)
    ).fetchall()
    now = datetime.now()
    return [number for number, issued_at in rows
            if (now - datetime.fromisoformat(issued_at)).days > due_days]


def invoice_page(db, tenant_id, page, size=20):
    offset = page * size
    return db.execute(
        "SELECT number FROM invoices WHERE tenant_id = ? ORDER BY id LIMIT ? OFFSET ?",
        (tenant_id, size, offset),
    ).fetchall()
