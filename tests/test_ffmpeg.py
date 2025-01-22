"""
Unit test file.
"""

import os
import unittest
from pathlib import Path

from iso_env import IsoEnv, IsoEnvArgs, Requirements

os.environ["ISO_ENV_VERBOSE"] = "1"

REQUIREMENTS_TXT = """
static-ffmpeg
"""


class MainTester(unittest.TestCase):
    """Main tester class."""

    def test_iso_env(self) -> None:
        """Test command line interface (CLI)."""
        args = IsoEnvArgs(
            venv_path=Path(".env_ffmpeg"),
            build_info=Requirements(REQUIREMENTS_TXT, python_version="==3.10.*"),
        )
        iso = IsoEnv(args)
        cp = iso.run(["static_ffmpeg", "-version"])
        print(cp)

        cp = iso.run(["pwd"])
        print(cp)
        print()


if __name__ == "__main__":
    unittest.main()
