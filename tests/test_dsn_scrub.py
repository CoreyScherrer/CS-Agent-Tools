"""A DSN printed by `describe()` never shows its password, in either libpq form."""

import unittest

from ma.storage.postgres_backend import PostgresBackend, _scrub_dsn


class ScrubDsnTests(unittest.TestCase):
    def assertHidden(self, dsn, expected, secret):
        out = _scrub_dsn(dsn)
        self.assertEqual(out, expected)
        self.assertNotIn(secret, out)

    def test_uri_password(self):
        self.assertHidden("postgresql://me:hunter2@db:5432/ma",
                          "postgresql://me:***@db:5432/ma", "hunter2")

    def test_uri_password_with_at_sign(self):
        self.assertHidden("postgres://me:p@ss@db/ma", "postgres://me:***@db/ma", "p@ss")

    def test_uri_password_in_query(self):
        self.assertHidden("postgresql://db/ma?sslmode=require&password=hunter2",
                          "postgresql://db/ma?sslmode=require&password=***", "hunter2")

    def test_keyvalue_password(self):
        self.assertHidden("host=db user=me password=hunter2 dbname=ma",
                          "host=db user=me password=*** dbname=ma", "hunter2")

    def test_keyvalue_quoted_password_with_spaces(self):
        self.assertHidden("host=db password = 'my secret' dbname=ma",
                          "host=db password = *** dbname=ma", "secret")

    def test_keyvalue_is_case_insensitive(self):
        self.assertHidden("PASSWORD=hunter2 host=db", "PASSWORD=*** host=db", "hunter2")

    def test_nothing_to_hide_is_unchanged(self):
        for dsn in ("", "host=db dbname=ma", "postgres://me@db/ma", "host=db passfile=/x"):
            self.assertEqual(_scrub_dsn(dsn), dsn)

    def test_describe_uses_the_scrubbed_form(self):
        self.assertEqual(PostgresBackend("host=db password=hunter2").describe(),
                         "postgres: host=db password=***")


if __name__ == "__main__":
    unittest.main()
