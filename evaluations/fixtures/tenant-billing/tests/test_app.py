import unittest

from app import db as dbmod, handlers, repo, reports, tokens, webhooks


class AppTest(unittest.TestCase):
    def setUp(self):
        self.db = dbmod.connect()
        self.db.execute("INSERT INTO tenants (id, name) VALUES (1, 'acme')")
        self.db.execute("INSERT INTO users (id, tenant_id, email, display_name) VALUES (1, 1, 'a@acme.test', 'A')")
        self.db.execute("INSERT INTO customers (id, tenant_id, name) VALUES (1, 1, 'Globex')")
        self.db.execute("INSERT INTO invoices (tenant_id, customer_id, number, amount_cents, issued_at) "
                        "VALUES (1, 1, 'INV-1', 1250, '2026-10-05T10:00:00')")
        self.db.execute("INSERT INTO coupons (code, tenant_id, uses_left) VALUES ('WELCOME', 1, 1)")
        self.user = repo.get_user(self.db, 1)

    def test_show_invoice(self):
        self.assertEqual(handlers.show_invoice(self.db, self.user, 1)["number"], "INV-1")

    def test_download_invoice(self):
        self.assertIn("INV-1", handlers.download_invoice(self.db, self.user, "INV-1"))

    def test_update_profile(self):
        self.assertEqual(handlers.update_profile(self.db, self.user, {"display_name": "Ann"})["display_name"], "Ann")

    def test_redeem_coupon_once(self):
        self.assertTrue(handlers.redeem_coupon(self.db, self.user, "WELCOME"))
        self.assertFalse(handlers.redeem_coupon(self.db, self.user, "WELCOME"))

    def test_signature(self):
        sig = webhooks.sign("s3cret", b"{}")
        self.assertTrue(webhooks.verify_signature("s3cret", b"{}", sig))

    def test_tokens(self):
        self.assertEqual(len(tokens.new_reset_token()), 24)

    def test_monthly_revenue(self):
        self.assertEqual(reports.monthly_revenue(self.db, 1, 2026, 10), {"Globex": 12.5})


if __name__ == "__main__":
    unittest.main()
