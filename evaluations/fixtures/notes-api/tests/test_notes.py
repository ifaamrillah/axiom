import unittest

import notes


class NotesTest(unittest.TestCase):
    def setUp(self):
        self.db = notes.connect()
        self.alice = notes.create_user(self.db, "alice", "pw-a")

    def test_login(self):
        self.assertEqual(notes.login(self.db, "alice", "pw-a"), self.alice)
        self.assertIsNone(notes.login(self.db, "alice", "wrong"))

    def test_create_and_list(self):
        notes.create_note(self.db, self.alice, "groceries", "milk")
        self.assertEqual([n["title"] for n in notes.list_notes(self.db, self.alice)], ["groceries"])

    def test_search(self):
        notes.create_note(self.db, self.alice, "groceries", "milk")
        self.assertEqual(len(notes.search_notes(self.db, self.alice, "groc")), 1)

    def test_read_export(self):
        self.assertIn("exported", notes.read_export("sample.txt"))


if __name__ == "__main__":
    unittest.main()
