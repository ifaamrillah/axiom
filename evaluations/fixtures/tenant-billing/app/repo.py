"""Data access. Every query must be scoped to the caller's tenant."""

SORTABLE = {"number": "number", "amount": "amount_cents", "issued": "issued_at"}


def get_invoice(db, tenant_id, invoice_id):
    return db.execute(
        "SELECT id, number, amount_cents FROM invoices WHERE tenant_id = ? AND id = ?",
        (tenant_id, invoice_id),
    ).fetchone()


def list_invoices(db, tenant_id, sort="issued"):
    column = SORTABLE.get(sort, "issued_at")
    return db.execute(
        f"SELECT id, number, amount_cents FROM invoices WHERE tenant_id = ? ORDER BY {column}",
        (tenant_id,),
    ).fetchall()


def find_invoice_by_number(db, number):
    return db.execute(
        "SELECT id, tenant_id, number, amount_cents FROM invoices WHERE number = ?",
        (number,),
    ).fetchone()


def get_user(db, user_id):
    row = db.execute(
        "SELECT id, tenant_id, email, display_name, role FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    return dict(zip(("id", "tenant_id", "email", "display_name", "role"), row))
