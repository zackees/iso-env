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
