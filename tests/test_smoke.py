"""Smoke checks for the pinned toolchain.

These tests confirm the project layout and that the HTTP library import
still matches the call sites already in the CLI. They do not run scanners
or open network connections.
"""

import importlib
import importlib.metadata
import pathlib
import py_compile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class ToolchainSmokeTest(unittest.TestCase):
    def test_expected_project_files_exist(self):
        expected = (
            "main.py",
            "programs.py",
            "requirements.txt",
            "src/ports.txt",
            "src/dirb.txt",
            "src/subdomain.txt",
        )
        for relative in expected:
            path = ROOT / relative
            self.assertTrue(path.is_file(), relative)
            self.assertGreater(path.stat().st_size, 0, relative)

    def test_application_modules_compile(self):
        for name in ("main.py", "programs.py"):
            py_compile.compile(str(ROOT / name), doraise=True)

    def test_runtime_modules_import(self):
        programs = importlib.import_module("programs")
        main = importlib.import_module("main")
        for name in ("port_scanner", "submarine", "boat", "social", "request"):
            self.assertTrue(callable(getattr(programs, name)), name)
        self.assertTrue(callable(main.Lead))

    def test_requests_pin_matches_lock(self):
        requests = importlib.import_module("requests")
        version = importlib.metadata.version("requests")
        self.assertEqual(version, "2.34.2")
        self.assertTrue(callable(requests.get))
        self.assertTrue(issubclass(requests.exceptions.ConnectionError, OSError))
