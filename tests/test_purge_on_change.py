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


class PurgeOnChangeTester(unittest.TestCase):
    """Main tester class."""

    def test_iso_env_with_cwd(self) -> None:
        """Test command line interface (CLI)."""
        venv_path = Path(".env_purge").resolve()
        args = IsoEnvArgs(
            venv_path=venv_path,
            build_info=Requirements(REQUIREMENTS_TXT),
        )
        iso = IsoEnv(args)
        cp = iso.run(["pwd"], capture_output=True, text=True, check=True)
        self.assertEqual(cp.returncode, 0)
        # now add a new line to the requirements file
        args.build_info = Requirements(REQUIREMENTS_TXT + "pytest")
        iso = IsoEnv(args)
        cp = iso.run(["pwd"], capture_output=True, text=True, check=True)
        self.assertEqual(cp.returncode, 0)
        gen_pyproject = venv_path / "pyproject.toml"
        self.assertTrue(gen_pyproject.exists())
        text = gen_pyproject.read_text()
        self.assertIn("pytest", text)


if __name__ == "__main__":
    unittest.main()
