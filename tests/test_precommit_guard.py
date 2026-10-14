"""Pre-commit guard behavior in isolated repositories."""

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


GUARD_SOURCE = Path(__file__).resolve().parents[1] / "scripts" / "pre-commit-guard.sh"


@unittest.skipUnless(shutil.which("git"), "git is required")
class TestPrecommitGuard(unittest.TestCase):
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
        hook = self.repo / ".git" / "hooks" / "pre-commit"
        shutil.copyfile(str(GUARD_SOURCE), str(hook))
        os.chmod(str(hook), 0o755)

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


if __name__ == "__main__":
    unittest.main()
