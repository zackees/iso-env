import os
import subprocess
import sys

from iso_env.types import IsoEnvArgs


def get_verbose_from_env() -> bool:
    return os.environ.get("ISO_ENV_VERBOSE", "0") == "1"


def to_full_cmd_str(
    args: IsoEnvArgs,
    cmd_list: list[str] | str,
    verbose: bool | None = False,
    **process_args,  # needed to capture unexpected arguments
) -> str:
    verbose = verbose if verbose is not None else get_verbose_from_env()

    python_exe = sys.executable
    preamble = [
        python_exe,
        "-m",
        "uv",
        "run",
        "--project",
        str(args.venv_path),
    ]
    if isinstance(cmd_list, list):
        full_cmd = preamble + cmd_list
        full_cmd_str = subprocess.list2cmdline(full_cmd)
    else:
        full_cmd_str = subprocess.list2cmdline(preamble) + " " + cmd_list
    return full_cmd_str
