"""
Unit test file.
"""

import os
import unittest
from pathlib import Path

from iso_env import IsoEnv, IsoEnvArgs, Requirements

os.environ["ISO_ENV_VERBOSE"] = "1"

REQUIREMENTS_TXT = """
"""


class CwdTester(unittest.TestCase):
    """Main tester class."""

    def test_iso_env_with_cwd(self) -> None:
        """Test command line interface (CLI)."""
        args = IsoEnvArgs(
            venv_path=Path(".env_cwd"),
            build_info=Requirements(REQUIREMENTS_TXT),
        )
        iso = IsoEnv(args)
        proc = iso.open_proc(["pwd"], text=True)
        proc.wait()
        print(proc.stdout)
        print()


if __name__ == "__main__":
    unittest.main()
