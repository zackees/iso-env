"""
Unit test file.
"""

import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


def run(
    path: Path, requirements: str, cmd_list: list[str], **process_args
) -> subprocess.CompletedProcess:
    """Runs the command using the isolated environment."""
    if not installed(path):
        install(path, requirements)
    full_cmd = ["uvx"] + cmd_list
    full_cmd_str = subprocess.list2cmdline(full_cmd)
    env = dict(os.environ)
    env["VIRTUAL_ENV"] = str(path / ".venv")
    cp = subprocess.run(full_cmd_str, cwd=path, env=env, shell=True, **process_args)
    return cp


def install(path: Path, requirements_text: str) -> None:
    """Uses isolated_environment to install aider."""
    if installed(path):
        return
    # Print installing message
    print("Installing aider...")
    # Install aider using isolated_environment
    path.mkdir(exist_ok=True)
    subprocess.run(["uv", "venv"], cwd=str(path), check=True)
    requirements = path / "requirements.txt"
    requirements.write_text(requirements_text, encoding="utf-8")
    env: dict = dict(os.environ)
    env["VIRTUAL_ENV"] = str(path / ".venv")
    subprocess.run(
        "uv pip install -r requirements.txt",
        cwd=str(path),
        env=env,
        shell=True,
        check=True,
    )
    (path / "installed").touch()


def purge(path: Path) -> int:
    print("Purging...")
    if not installed(path):
        print("program is not installed.")
        return 0
    try:
        shutil.rmtree(path)
        print("purged successfully.")
        return 0
    except Exception as e:
        print(f"Error purging aider: {e}")
        return 1


def installed(venv_path: Path) -> bool:
    here = Path(__file__).parent
    dst = venv_path / "trampoline.py"
    if not dst.exists():
        venv_path.mkdir(parents=True, exist_ok=True)
        shutil.copy(here / "trampoline.py", venv_path / "trampoline.py")
    return (venv_path / "installed").exists()


@dataclass
class IsoEnvArgs:
    venv_path: Path
    requirements: str


class IsoEnv:
    def __init__(self, args: IsoEnvArgs) -> None:
        self.venv_path = args.venv_path
        self.requirements = args.requirements

    def run(self, cmd_list: list[str], **process_args) -> subprocess.CompletedProcess:
        return run(self.venv_path, self.requirements, cmd_list, **process_args)
