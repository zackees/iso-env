"""
Unit test file.
"""

import os
import unittest
from pathlib import Path

from iso_env import IsoEnvArgs, Requirements

os.environ["ISO_ENV_VERBOSE"] = "1"

REQUIREMENTS_TXT = """
"""


class PythonBadVersionTester(unittest.TestCase):
    """Main tester class."""

    def test_invalid_python_str(self) -> None:
        """Test command line interface (CLI)."""
        venv_path = Path(".env_311").resolve()
        # assert ValueError is raised
        with self.assertRaises(ValueError):
            _ = IsoEnvArgs(
                venv_path=venv_path,
                build_info=Requirements(REQUIREMENTS_TXT, python_version="==3.11"),
            )
        _ = IsoEnvArgs(
            venv_path=venv_path,
            build_info=Requirements(REQUIREMENTS_TXT, python_version="==3.10.*"),
        )


if __name__ == "__main__":
    unittest.main()
