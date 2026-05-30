"""Regression tests for iso-env#1.

When ``uv venv`` fails inside ``api.install``, the actual uv stderr is the
only actionable diagnostic. v1.0.43 lost it: it ``print``ed to stdout and
re-raised a bare ``CalledProcessError`` whose ``str(e)`` only said
``"... returned non-zero exit status N"``. Downstream callers (notably
transcribe-anything) therefore showed users an unactionable error.

This module pins the new contract: a ``RuntimeError`` is raised whose
message contains the captured stderr.
"""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from iso_env import IsoEnvArgs, PyProjectToml
from iso_env.api import install


def _make_args(venv_path: Path) -> IsoEnvArgs:
    return IsoEnvArgs(
        venv_path=venv_path,
        build_info=PyProjectToml(
            "[project]\n"
            'name = "p"\n'
            'version = "0.0.1"\n'
            'requires-python = ">=3.10"\n'
        ),
    )


class InstallErrorPropagationTester(unittest.TestCase):
    def test_uv_venv_failure_raises_runtime_error_with_stderr(self) -> None:
        stderr_text = "error: failed to discover python interpreter: <synthetic>"
        cpe = subprocess.CalledProcessError(
            returncode=2,
            cmd=["/usr/bin/uv", "venv"],
            output="",
            stderr=stderr_text,
        )
        with tempfile.TemporaryDirectory() as tmp:
            venv_path = Path(tmp) / "venv"
            args = _make_args(venv_path)
            with mock.patch("iso_env.api.shutil.which", return_value="/usr/bin/uv"):
                with mock.patch(
                    "iso_env.api.subprocess.run",
                    side_effect=cpe,
                ):
                    with self.assertRaises(RuntimeError) as ctx:
                        install(args, verbose=False)
        msg = str(ctx.exception)
        self.assertIn("2", msg)  # exit code
        self.assertIn(stderr_text, msg)
        self.assertIn("uv venv", msg)

    def test_runtime_error_chains_original_calledprocesserror(self) -> None:
        """RuntimeError must be raised ``from`` the CalledProcessError so the
        original cause is preserved for debugging.
        """
        cpe = subprocess.CalledProcessError(
            returncode=42,
            cmd=["/usr/bin/uv", "venv"],
            output="",
            stderr="something specific",
        )
        with tempfile.TemporaryDirectory() as tmp:
            venv_path = Path(tmp) / "venv"
            args = _make_args(venv_path)
            with mock.patch("iso_env.api.shutil.which", return_value="/usr/bin/uv"):
                with mock.patch(
                    "iso_env.api.subprocess.run",
                    side_effect=cpe,
                ):
                    with self.assertRaises(RuntimeError) as ctx:
                        install(args, verbose=False)
        self.assertIsInstance(ctx.exception.__cause__, subprocess.CalledProcessError)


if __name__ == "__main__":
    unittest.main()
