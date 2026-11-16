"""Notes service: users own notes; notes can be searched and exported."""

import hashlib
import os
import sqlite3

EXPORT_DIR = os.path.join(os.path.dirname(__file__), "exports")


def connect(path=":memory:"):
    db = sqlite3.connect(path)
    db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT UNIQUE, password_hash TEXT)")
    db.execute("CREATE TABLE notes (id INTEGER PRIMARY KEY, owner_id INTEGER, title TEXT, body TEXT)")
    return db


def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


def create_user(db, name, password):
    cur = db.execute("INSERT INTO users (name, password_hash) VALUES (?, ?)", (name, hash_password(password)))
    return cur.lastrowid


def login(db, name, password):
    row = db.execute("SELECT id, password_hash FROM users WHERE name = ?", (name,)).fetchone()
    if row and row[1] == hash_password(password):
        return row[0]
    return None


def create_note(db, user_id, title, body):
    cur = db.execute("INSERT INTO notes (owner_id, title, body) VALUES (?, ?, ?)", (user_id, title, body))
    return cur.lastrowid


def get_note(db, user_id, note_id):
    row = db.execute("SELECT id, owner_id, title, body FROM notes WHERE id = ?", (note_id,)).fetchone()
    if row is None:
        raise KeyError(note_id)
    return {"id": row[0], "title": row[2], "body": row[3]}


def list_notes(db, user_id):
    rows = db.execute("SELECT id, title FROM notes WHERE owner_id = ? ORDER BY id", (user_id,)).fetchall()
    return [{"id": r[0], "title": r[1]} for r in rows]


def search_notes(db, user_id, term):
    query = f"SELECT id, title FROM notes WHERE owner_id = {user_id} AND title LIKE '%{term}%'"
    return [{"id": r[0], "title": r[1]} for r in db.execute(query).fetchall()]


def read_export(filename):
    with open(os.path.join(EXPORT_DIR, filename)) as handle:
        return handle.read()
