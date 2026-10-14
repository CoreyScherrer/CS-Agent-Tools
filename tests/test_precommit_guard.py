"""Pre-commit guard behavior in isolated repositories."""

import os
import shutil
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from ma.cli import main as main_mod


GUARD_SOURCE = Path(__file__).resolve().parents[1] / "scripts" / "pre-commit-guard.sh"


class GitRepoCase(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.repo = Path(temporary.name)
        subprocess.run(
            ["git", "init", "-q", str(self.repo)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    def _install_guard(self):
        hook = self.repo / ".git" / "hooks" / "pre-commit"
        shutil.copyfile(str(GUARD_SOURCE), str(hook))
        os.chmod(str(hook), 0o755)
        return hook

    def _git(self, *args):
        return subprocess.run(
            ["git", "-C", str(self.repo)] + list(args),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    def _commit(self, message):
        return self._git(
            "-c", "user.name=Test User",
            "-c", "user.email=test@example.com",
            "commit", "-m", message,
        )


@unittest.skipUnless(shutil.which("git"), "git is required")
class TestPrecommitGuard(GitRepoCase):
    def setUp(self):
        super().setUp()
        self._install_guard()

    def test_normal_file_commits(self):
        (self.repo / "safe.txt").write_text("safe\n", encoding="utf-8")
        self.assertEqual(self._git("add", "--", "safe.txt").returncode, 0)
        result = self._commit("add safe file")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_data_file_is_blocked(self):
        data_dir = self.repo / "data"
        data_dir.mkdir()
        (data_dir / "x.md").write_text("captured\n", encoding="utf-8")
        self.assertEqual(self._git("add", "--", "data/x.md").returncode, 0)
        result = self._commit("add captured content")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("captured content", result.stdout + result.stderr)

    def test_renamed_file_into_data_is_blocked(self):
        (self.repo / "tracked.md").write_text("captured\n", encoding="utf-8")
        self.assertEqual(self._git("add", "--", "tracked.md").returncode, 0)
        initial = self._commit("add tracked file")
        self.assertEqual(initial.returncode, 0, initial.stdout + initial.stderr)

        (self.repo / "data").mkdir()
        self.assertEqual(self._git("mv", "tracked.md", "data/x.md").returncode, 0)
        result = self._commit("move captured content")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("captured content", result.stdout + result.stderr)

    def test_guard_exemption_commits(self):
        exempt = self.repo / "product-discovery" / "protocol"
        exempt.mkdir(parents=True)
        (exempt / "assumptions.md").write_text("framework protocol\n", encoding="utf-8")
        self.assertEqual(
            self._git("add", "--", "product-discovery/protocol/assumptions.md").returncode, 0
        )
        result = self._commit("add protocol assumptions")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


@unittest.skipUnless(shutil.which("git"), "git is required")
class TestInstallPrecommitGuard(GitRepoCase):
    def setUp(self):
        super().setUp()
        source = self.repo / "scripts" / "pre-commit-guard.sh"
        source.parent.mkdir()
        shutil.copyfile(str(GUARD_SOURCE), str(source))
        config_patch = mock.patch.object(main_mod.config_mod, "REPO_ROOT", str(self.repo))
        config_patch.start()
        self.addCleanup(config_patch.stop)
        self.hooks = self.repo / ".git" / "hooks"
        self.target = self.hooks / "pre-commit"
        self.local = self.hooks / "pre-commit.local"

    def test_fresh_install(self):
        result = main_mod._install_precommit_guard()
        self.assertEqual(result, "Installed pre-commit guard (blocks committing data/ and *.db)")
        self.assertIn("Pre-commit guard — blocks captured content", self.target.read_text(encoding="utf-8"))
        self.assertTrue(os.access(str(self.target), os.X_OK))

    def test_foreign_hook_is_kept_and_runs(self):
        foreign = "#!/bin/sh\ntouch hook-ran\n"
        self.target.write_text(foreign, encoding="utf-8")
        os.chmod(str(self.target), 0o755)

        result = main_mod._install_precommit_guard()
        self.assertEqual(
            result,
            "Installed pre-commit guard; your existing hook was kept as "
            ".git/hooks/pre-commit.local and still runs",
        )
        self.assertEqual(self.local.read_text(encoding="utf-8"), foreign)

        (self.repo / "safe.txt").write_text("safe\n", encoding="utf-8")
        self.assertEqual(self._git("add", "--", "safe.txt").returncode, 0)
        commit = self._commit("add safe file")
        self.assertEqual(commit.returncode, 0, commit.stdout + commit.stderr)
        marker = self.repo / "hook-ran"
        self.assertTrue(marker.is_file())

        marker.unlink()
        empty_commit = self._git(
            "-c", "user.name=Test User",
            "-c", "user.email=test@example.com",
            "commit", "--allow-empty", "-m", "empty commit",
        )
        self.assertEqual(empty_commit.returncode, 0, empty_commit.stdout + empty_commit.stderr)
        self.assertTrue(marker.is_file())

    def test_reinstall_refreshes_guard_without_creating_local_hook(self):
        first = main_mod._install_precommit_guard()
        self.assertIn("Installed pre-commit guard", first)
        self.assertFalse(self.local.exists())

        second = main_mod._install_precommit_guard()
        self.assertEqual(second, "Installed pre-commit guard (blocks committing data/ and *.db)")
        self.assertFalse(self.local.exists())
        self.assertIn("Pre-commit guard — blocks captured content", self.target.read_text(encoding="utf-8"))

    def test_foreign_and_local_hooks_are_left_unchanged_with_warning(self):
        self.target.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        self.local.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
        os.chmod(str(self.target), 0o755)
        os.chmod(str(self.local), 0o755)
        before = {
            path: (path.read_bytes(), stat.S_IMODE(path.stat().st_mode))
            for path in (self.target, self.local)
        }

        result = main_mod._install_precommit_guard()

        self.assertIn("WARNING", result)
        self.assertIn("both exist", result)
        for path, (contents, mode) in before.items():
            self.assertEqual(path.read_bytes(), contents)
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), mode)


if __name__ == "__main__":
    unittest.main()
