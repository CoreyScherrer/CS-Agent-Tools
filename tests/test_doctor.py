"""Doctor tests.

The contract under test is resilience: on an unknown machine every probe must
produce a result rather than an exception, and a raising probe must not take the
run down with it.
"""

import os
import tempfile
import unittest

from ma.core import doctor


class TestProbesNeverRaise(unittest.TestCase):
    """Each probe runs against this real machine and must return a Probe."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = self._tmp.name

    def test_all_probes_return_results(self):
        for probe in doctor.run_all(self.root):
            self.assertIsInstance(probe, doctor.Probe)
            self.assertIn(probe.status, (doctor.OK, doctor.WARN, doctor.FAIL, doctor.SKIP))
            self.assertTrue(probe.summary)

    def test_run_all_covers_every_probe(self):
        keys = {p.key for p in doctor.run_all(self.root)}
        self.assertEqual(
            keys, {"python", "pip", "postgres", "filesystem", "editor", "hooks", "egress", "git"}
        )

    def test_a_raising_probe_becomes_a_warning(self):
        def explode():
            raise RuntimeError("simulated hostile environment")

        probe = doctor._safe("boom", explode)
        self.assertEqual(probe.status, doctor.WARN)
        self.assertIn("simulated hostile environment", probe.detail["error"])

    def test_probe_serialises_to_dict(self):
        self.assertEqual(
            set(doctor.Probe("k", doctor.OK, "s").as_dict()),
            {"key", "status", "summary", "detail"},
        )


class TestFilesystemProbe(unittest.TestCase):
    def test_writable_directory_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            probe = doctor.probe_filesystem(tmp)
            self.assertEqual(probe.status, doctor.OK)
            self.assertTrue(probe.detail["writable"])

    def test_synced_folder_is_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            synced = os.path.join(tmp, "OneDrive", "repo")
            os.makedirs(synced)
            probe = doctor.probe_filesystem(synced)
            self.assertEqual(probe.status, doctor.WARN)
            self.assertTrue(probe.detail["synced_folder"])

    def test_unwritable_directory_fails_cleanly(self):
        probe = doctor.probe_filesystem("/proc/nonexistent-ma-probe")
        self.assertEqual(probe.status, doctor.FAIL)


class TestBackendRecommendation(unittest.TestCase):
    """Postgres only when usable end to end; otherwise SQLite, always."""

    def _probe(self, status, **detail):
        base = {"server_reachable": False, "driver_installed": False, "can_create_db": False}
        base.update(detail)
        return doctor.Probe("postgres", status, "", base)

    def test_fully_usable_postgres_is_selected(self):
        probes = [self._probe(doctor.OK, server_reachable=True,
                              driver_installed=True, can_create_db=True)]
        backend, _ = doctor.recommend_backend(probes)
        self.assertEqual(backend, "postgres")

    def test_no_server_falls_back_to_sqlite(self):
        backend, reason = doctor.recommend_backend([self._probe(doctor.SKIP)])
        self.assertEqual(backend, "sqlite")
        self.assertIn("no reachable", reason)

    def test_server_without_driver_falls_back(self):
        probes = [self._probe(doctor.WARN, server_reachable=True)]
        backend, reason = doctor.recommend_backend(probes)
        self.assertEqual(backend, "sqlite")
        self.assertIn("driver", reason)

    def test_server_without_auth_falls_back(self):
        probes = [self._probe(doctor.WARN, server_reachable=True, driver_installed=True)]
        backend, reason = doctor.recommend_backend(probes)
        self.assertEqual(backend, "sqlite")
        self.assertIn("authentication", reason)

    def test_missing_postgres_probe_still_yields_a_backend(self):
        backend, _ = doctor.recommend_backend([])
        self.assertEqual(backend, "sqlite")


class TestReportFormatting(unittest.TestCase):
    def test_report_lists_every_probe_and_the_decision(self):
        probes = [doctor.Probe("python", doctor.OK, "Python 3.11"),
                  doctor.Probe("postgres", doctor.SKIP, "no server")]
        report = doctor.format_report(probes, "sqlite", "no server")
        self.assertIn("python", report)
        self.assertIn("postgres", report)
        self.assertIn("Selected backend: sqlite", report)

    def test_blocking_failures_are_called_out(self):
        probes = [doctor.Probe("filesystem", doctor.FAIL, "cannot write")]
        self.assertIn("Blocking problems", doctor.format_report(probes, "sqlite", "x"))




class TestPostgresProbeUsesConfiguredDsn(unittest.TestCase):
    """A configured DSN is what the archive will use, so it is what gets tested."""

    def setUp(self):
        from unittest import mock
        self.mock = mock
        # Pretend a server answers and a driver is importable.
        self.patches = [
            mock.patch.object(doctor.socket, "create_connection", mock.MagicMock()),
            mock.patch("ma.storage.postgres_backend.driver_available", return_value=True),
        ]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in self.patches:
            p.stop()

    def test_working_dsn_is_selected_without_psql(self):
        with self.mock.patch.object(doctor, "_try_dsn", return_value=(True, "")), \
             self.mock.patch.object(doctor.shutil, "which", return_value=None):
            probe = doctor.probe_postgres("postgresql://u:pw@127.0.0.1:5433/db")
        self.assertEqual(probe.status, doctor.OK)
        backend, _ = doctor.recommend_backend([probe])
        self.assertEqual(backend, "postgres")

    def test_rejected_dsn_falls_back_and_never_echoes_it(self):
        with self.mock.patch.object(doctor, "_try_dsn", return_value=(False, "OperationalError")):
            probe = doctor.probe_postgres("postgresql://u:s3cret@127.0.0.1/db")
        self.assertEqual(probe.status, doctor.WARN)
        self.assertNotIn("s3cret", probe.summary + repr(probe.detail))
        self.assertEqual(doctor.recommend_backend([probe])[0], "sqlite")

    def test_configured_dsn_is_tested_by_the_driver_not_a_guessed_host(self):
        # A web URL parser reads "me:12/ss@db" as host "me", port 12 (part of the
        # password), and a key/value DSN has no URL host at all. Neither may be
        # probed or printed: the driver connect decides.
        for dsn in ("postgresql://me:12/ss@db/ma", "host=db.internal port=6543 password=12ss"):
            with self.mock.patch.object(doctor, "_try_dsn", return_value=(False, "OperationalError")):
                probe = doctor.probe_postgres(dsn)
            doctor.socket.create_connection.assert_not_called()
            self.assertNotIn("12", probe.summary + repr(probe.detail))
            self.assertEqual(probe.status, doctor.WARN)

    def test_configured_dsn_without_a_driver_says_so(self):
        with self.mock.patch("ma.storage.postgres_backend.driver_available", return_value=False):
            probe = doctor.probe_postgres("host=db password=s3cret")
        self.assertEqual(probe.status, doctor.WARN)
        self.assertIn("no psycopg driver", probe.summary)
        self.assertNotIn("s3cret", probe.summary + repr(probe.detail))
        backend, reason = doctor.recommend_backend([probe])
        self.assertEqual(backend, "sqlite")
        self.assertIn("no psycopg driver", reason)

    def test_no_dsn_and_no_psql_says_why(self):
        with self.mock.patch.object(doctor.shutil, "which", return_value=None):
            probe = doctor.probe_postgres(None)
        self.assertEqual(probe.status, doctor.WARN)
        self.assertIn("psql is not on PATH", probe.summary)


class TestLocalConfigPermissions(unittest.TestCase):
    def test_saved_config_is_owner_only(self):
        import stat
        import tempfile
        from unittest import mock
        from ma import config as config_mod
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "config.local.json")
            with mock.patch.object(config_mod, "LOCAL_CONFIG", path):
                config_mod.save_local({"storage": {"postgres_dsn": "postgresql://u:pw@h/d"}})
            self.assertEqual(stat.S_IMODE(os.stat(path).st_mode), 0o600)


if __name__ == "__main__":
    unittest.main()
