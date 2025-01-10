"""
Unit test file.
"""

import unittest
from pathlib import Path

from iso_env.api import IsoEnv


class MainTester(unittest.TestCase):
    """Main tester class."""

    def test_iso_env(self) -> None:
        """Test command line interface (CLI)."""
        reqs = "static-ffmpeg"
        path = Path("iso_env")
        iso = IsoEnv(path, reqs)
        cp = iso.run(["static_ffmpeg", "-version"])
        print(cp)


if __name__ == "__main__":
    unittest.main()
