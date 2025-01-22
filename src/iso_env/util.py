import os
import sys

from iso_env.types import IsoEnvArgs


def get_verbose_from_env() -> bool:
    return os.environ.get("ISO_ENV_VERBOSE", "0") == "1"


def to_full_cmd_list(
    args: IsoEnvArgs,
    cmd_list: list[str],
    verbose: bool | None = None,
    **process_args,  # needed to capture unexpected arguments
) -> list[str]:
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
    return preamble + cmd_list


def clean_virtual_env_from_env(**process_args) -> dict[str, str]:
    if "env" in process_args:
        env = process_args["env"]
        process_args.pop("env")
    else:
        env = dict(os.environ)
    if "VIRTUAL_ENV" in env:
        del env["VIRTUAL_ENV"]
    return env
