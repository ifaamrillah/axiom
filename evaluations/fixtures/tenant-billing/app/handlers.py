"""Request handlers. `user` is the authenticated user dict from repo.get_user."""

from app import repo


def show_invoice(db, user, invoice_id):
    row = repo.get_invoice(db, user["tenant_id"], invoice_id)
    if row is None:
        raise LookupError("not found")
    return {"id": row[0], "number": row[1], "amount_cents": row[2]}


def download_invoice(db, user, number):
    row = repo.find_invoice_by_number(db, number)
    if row is None:
        raise LookupError("not found")
    return f"Invoice {row[2]}: {row[3]} cents"


def update_profile(db, user, fields):
    for key, value in fields.items():
        db.execute(f"UPDATE users SET {key} = ? WHERE id = ?", (value, user["id"]))
    return repo.get_user(db, user["id"])


def redeem_coupon(db, user, code):
    row = db.execute(
        "SELECT uses_left FROM coupons WHERE code = ? AND tenant_id = ?", (code, user["tenant_id"])
    ).fetchone()
    if row is None or row[0] <= 0:
        return False
    db.execute("INSERT INTO redemptions (user_id, code) VALUES (?, ?)", (user["id"], code))
    db.execute("UPDATE coupons SET uses_left = ? WHERE code = ?", (row[0] - 1, code))
    return True
