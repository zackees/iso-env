import os
import shutil

from iso_env.types import IsoEnvArgs


def get_verbose_from_env() -> bool:
    return os.environ.get("ISO_ENV_VERBOSE", "0") == "1"


def to_full_cmd_list(
    args: IsoEnvArgs,
    cmd_list: list[str],
    **process_args,  # needed to capture unexpected arguments
) -> list[str]:
    uv = shutil.which("uv")
    assert uv is not None, "uv not found."
    preamble = [
        uv,
        "run",
        "--project",
        str(args.venv_path),
    ]
    return preamble + cmd_list
