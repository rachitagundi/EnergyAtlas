"""The setup check should run before installing application dependencies."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from scripts.check_setup import check_fullstack_files, read_command


class SetupDiagnosticChecks(unittest.TestCase):
    def test_runs_in_isolated_python_from_another_directory(self):
        script = Path(__file__).resolve().parents[1] / "scripts" / "check_setup.py"
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, "-I", str(script)],
                cwd=directory,
                capture_output=True,
                text=True,
                timeout=30,
                check=True,
            )
        report = json.loads(result.stdout)
        self.assertEqual(report["schema_version"], 1)
        self.assertEqual(report["python"]["version"], sys.version.split()[0])
        self.assertGreaterEqual(report["project_disk_free_gib"], 0)
        self.assertIsInstance(report["git"]["available"], bool)
        self.assertIsInstance(report["node"]["available"], bool)
        self.assertTrue(report["project"]["fullstack"]["complete"])

    def test_incomplete_extraction_reports_the_missing_files(self):
        with tempfile.TemporaryDirectory() as directory:
            report = check_fullstack_files(Path(directory))
        self.assertFalse(report["complete"])
        self.assertIn("frontend/package-lock.json", report["missing_files"])
        self.assertIn("backend/constraints-py312.txt", report["missing_files"])

    def test_missing_optional_program_does_not_crash(self):
        with patch("scripts.check_setup.subprocess.run", side_effect=FileNotFoundError):
            self.assertIsNone(read_command(["optional-program"]))

    def test_slow_optional_program_does_not_hang(self):
        timeout = subprocess.TimeoutExpired(cmd=["optional-program"], timeout=15)
        with patch("scripts.check_setup.subprocess.run", side_effect=timeout):
            self.assertIsNone(read_command(["optional-program"]))
