# iso-env - Run apps in an isolated environment using uv

[![Lint](https://github.com/zackees/iso-env/actions/workflows/lint.yml/badge.svg)](https://github.com/zackees/iso-env/actions/workflows/lint.yml)

[![MacOS_Tests](https://github.com/zackees/iso-env/actions/workflows/test_macos.yml/badge.svg)](https://github.com/zackees/iso-env/actions/workflows/test_macos.yml)
[![Ubuntu_Tests](https://github.com/zackees/iso-env/actions/workflows/test_ubuntu.yml/badge.svg)](https://github.com/zackees/iso-env/actions/workflows/test_ubuntu.yml)
[![Win_Tests](https://github.com/zackees/iso-env/actions/workflows/test_win.yml/badge.svg)](https://github.com/zackees/iso-env/actions/workflows/test_win.yml)


# Simple Example


```python

import unittest
from pathlib import Path

from iso_env.api import IsoEnv, IsoEnvArgs, Requirements

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
```

# Complex Example

```
"""
Unit test file.
"""

import unittest
from pathlib import Path

from iso_env.api import IsoEnv, IsoEnvArgs, PyProjectToml

PY_PROJECT_TOML = PyProjectToml(
    """
[project]
name = "project"
version = "0.1.0"
requires-python = ">=3.10.0"
dependencies = [
    "torch==2.1.2",
]

[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[tool.uv.sources]
torch = [
  { index = "pytorch-cu121", marker = "platform_system == 'Windows'" },
]

[[tool.uv.index]]
name = "pytorch-cu121"
url = "https://download.pytorch.org/whl/cu121"
explicit = true
"""
)


class ComplexInstallTester(unittest.TestCase):
    """Main tester class."""

    @unittest.skip("Skip this test - it takes a long time")
    def test_iso_env(self) -> None:
        """Test command line interface (CLI)."""
        args = IsoEnvArgs(
            venv_path=Path(".env_torch"),
            build_info=PY_PROJECT_TOML,
        )
        iso = IsoEnv(args)
        cp = iso.run(['python', '-c', "import torch; print(torch.__version__)"], check=True)
        print(cp)


if __name__ == "__main__":
    unittest.main()
```



To develop software, run `. ./activate.sh`

# Windows

This environment requires you to use `git-bash`.

# Linting

Run `./lint.sh` to find linting errors using `pylint`, `flake8` and `mypy`.


