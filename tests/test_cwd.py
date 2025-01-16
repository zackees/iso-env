"""
Unit test file.
"""

import unittest
from pathlib import Path

from iso_env.api import IsoEnv, IsoEnvArgs, Requirements

REQUIREMENTS_TXT = """
"""


class MainTester(unittest.TestCase):
    """Main tester class."""

    def test_iso_env(self) -> None:
        """Test command line interface (CLI)."""
        args = IsoEnvArgs(
            venv_path=Path(".env_cwd"),
            build_info=Requirements(REQUIREMENTS_TXT),
        )
        iso = IsoEnv(args)
        cp = iso.run(["pwd"], capture_output=True, text=True, check=True)
        print(cp.stdout)
        print()


if __name__ == "__main__":
    unittest.main()
