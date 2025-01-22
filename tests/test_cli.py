"""
Unit test file.
"""

import os
import unittest

os.environ["ISO_ENV_VERBOSE"] = "1"

COMMAND = "iso-env"


class MainTester(unittest.TestCase):
    """Main tester class."""

    def test_imports(self) -> None:
        """Test command line interface (CLI)."""
        rtn = os.system(COMMAND)
        self.assertEqual(0, rtn)


if __name__ == "__main__":
    unittest.main()
