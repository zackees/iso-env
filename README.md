# iso-env - Run apps in an isolated environment using uv

[![Lint](https://github.com/zackees/iso-env/actions/workflows/lint.yml/badge.svg)](https://github.com/zackees/iso-env/actions/workflows/lint.yml)

[![MacOS_Tests](https://github.com/zackees/iso-env/actions/workflows/test_macos.yml/badge.svg)](https://github.com/zackees/iso-env/actions/workflows/test_macos.yml)
[![Ubuntu_Tests](https://github.com/zackees/iso-env/actions/workflows/test_ubuntu.yml/badge.svg)](https://github.com/zackees/iso-env/actions/workflows/test_ubuntu.yml)
[![Win_Tests](https://github.com/zackees/iso-env/actions/workflows/test_win.yml/badge.svg)](https://github.com/zackees/iso-env/actions/workflows/test_win.yml)

![image](https://github.com/user-attachments/assets/b7adcbac-0400-4f72-a0cd-3a4f2bea3b4c)

# About

Got an AI app? Are you in dependency hell because of `pytorch`? Well, so was I...

Once upon a time I wanted to release an AI tool called `transcribe-anything` to tie a bunch of AI tools together to do translations across Windows/Mac/Linux without any complicated setup. To do this, I made `isolated-environment`, a package built ontop of `venv`. It was extremely messy but got the job done, and `transcribe-anything` surged in popularity. Fast forward a year later and `uv` comes out. `uv-iso-env` is a remake of `isolated-environment` but built on top of `uv`, the way god intended it.

# Simple Example


```python

import unittest
from pathlib import Path

from iso_env import IsoEnv, IsoEnvArgs, Requirements

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

```python
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



To develop software, run `. ./activate`

# Windows

This environment requires you to use `git-bash`.

# Linting

Run `./lint` to find linting errors.

# Footguns

Please don't use `shell=True` when you run python unless you absolutely need to. Why? Because on Linux, if you are running a script and you have any errors, instead of bombing out immediately, python will drop you into a command terminal. This only happens on Linux (and maybe mac). It's a very nasty bug when you try and run your scripts on linux, causing your scripts to hang. The workaround is to use `shutil.which(progname_str)` and pass the resulting full path into `iso.run([progname_str, ...], shell=False)`


