"""
Unit test file.
"""

import unittest
from pathlib import Path

from iso_env.api import IsoEnv, IsoEnvArgs, Requirements

REQUIREMENTS_TXT = Requirements(
    """
static-ffmpeg
"""
)


class MainTester(unittest.TestCase):
    """Main tester class."""

    def test_iso_env(self) -> None:
        """Test command line interface (CLI)."""
        args = IsoEnvArgs(
            venv_path=Path(".iso_env"),
            build_info=REQUIREMENTS_TXT,
        )
        iso = IsoEnv(args)
        cp = iso.run(["static_ffmpeg", "-version"])
        print(cp)


if __name__ == "__main__":
    unittest.main()
