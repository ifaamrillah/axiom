"""Nightly backup of the SQLite file."""

import subprocess

DB_PATH = "/var/lib/billing/billing.db"


def dump_database():
    result = subprocess.run(["sqlite3", DB_PATH, ".dump"], capture_output=True, text=True, check=True)
    return result.stdout
