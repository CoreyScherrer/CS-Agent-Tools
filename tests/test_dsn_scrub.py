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

    def test_keyvalue_escaped_quote_inside_password(self):
        self.assertHidden("password='it\\'s secret' host=db", "password=*** host=db", "secret")

    def test_keyvalue_unterminated_quote_hides_the_rest(self):
        self.assertHidden("host=db password='half secret", "host=db password=***", "secret")

    def test_malformed_uri_still_hides_the_password(self):
        self.assertHidden("postgresql://me:hunter2@[::1/ma", "postgresql://me:***@[::1/ma", "hunter2")

    def test_uri_password_holding_hash_slash_or_question_mark(self):
        # A web URL parser would end the authority at '#', '/' or '?' and print the rest.
        for pw in ("pa#ss", "pa/ss", "pa?ss"):
            self.assertHidden("postgresql://me:{}@db/ma".format(pw), "postgresql://me:***@db/ma", pw)

    def test_uri_percent_encoded_password_key(self):
        self.assertHidden("postgresql://db/ma?pass%77ord=hunter2", "postgresql://db/ma?pass%77ord=***", "hunter2")

    def test_uri_hash_in_query_password(self):
        self.assertHidden("postgresql://db/ma?password=hun#ter2&sslmode=require",
                          "postgresql://db/ma?password=***&sslmode=require", "ter2")

    def test_uri_scheme_is_case_insensitive(self):
        self.assertHidden("PostgreSQL://me:hunter2@db/ma", "PostgreSQL://me:***@db/ma", "hunter2")

    def test_keyvalue_backslash_escaped_space_in_unquoted_password(self):
        self.assertHidden("host=db password=hun\\ ter2 dbname=ma", "host=db password=*** dbname=ma", "ter2")

    def test_keyvalue_backslash_escaped_newline_in_unquoted_password(self):
        self.assertHidden("host=db password=hun\\\nter2 dbname=ma", "host=db password=*** dbname=ma", "ter2")

    def test_uri_question_mark_in_user_name_does_not_hide_the_query(self):
        self.assertHidden("postgresql://u?x@db/ma?password=hunter2", "postgresql://u?x@db/ma?password=***", "hunter2")

    def test_ssl_key_passphrase_is_hidden_too(self):
        self.assertHidden("host=db sslpassword=hunter2", "host=db sslpassword=***", "hunter2")
        self.assertHidden("postgresql://db/ma?sslpassword=hunter2", "postgresql://db/ma?sslpassword=***", "hunter2")

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
