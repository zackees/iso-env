import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Requirements:
    content: str
    python_version: str | None = None

    def __post_init__(self):
        self.content = self.content.strip()

    def __repr__(self):
        return self.content


@dataclass
class PyProjectToml:
    content: str

    def __post_init__(self):
        self.content = self.content.strip()

    def __repr__(self):
        return self.content


@dataclass
class IsoEnvArgs:
    venv_path: Path
    build_info: Requirements | PyProjectToml


class IsoEnv:
    def __init__(self, args: IsoEnvArgs) -> None:
        self.args = args

    def run(self, cmd_list: list[str], **process_args) -> subprocess.CompletedProcess:
        from iso_env.run import run

        return run(self.args, cmd_list, **process_args)

    def open_proc(self, cmd_list: list[str], **process_args) -> subprocess.Popen:
        from iso_env.api import open_proc

        return open_proc(self.args, cmd_list, **process_args)
