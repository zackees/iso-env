import subprocess
from pathlib import Path

from iso_env.api import install, installed, purge
from iso_env.types import IsoEnvArgs
from iso_env.util import (
    clean_virtual_env_from_env,
    get_verbose_from_env,
    to_full_cmd_list,
)


def run(
    args: IsoEnvArgs,
    cmd_list: list[str],
    verbose: bool | None = None,
    **process_args,
) -> subprocess.CompletedProcess:
    """Runs the command using the isolated environment."""
    verbose = verbose if verbose is not None else get_verbose_from_env()
    if not installed(args, verbose=verbose):
        purge(args.venv_path)
        install(args, verbose=verbose)
    env = clean_virtual_env_from_env(**process_args)
    full_cmd_list = to_full_cmd_list(args, cmd_list, verbose=verbose, **process_args)
    cp = subprocess.run(full_cmd_list, env=env, **process_args)
    return cp


def open_proc(
    args: IsoEnvArgs,
    cmd_list: list[str],
    verbose: bool | None = None,
    **process_args,
) -> subprocess.Popen:
    """Runs the command using the isolated environment."""
    verbose = verbose if verbose is not None else get_verbose_from_env()
    if not installed(args, verbose=verbose):
        purge(args.venv_path)
        install(args, verbose=verbose)
    full_cmd_list = to_full_cmd_list(args, cmd_list, verbose=verbose, **process_args)
    shell = process_args.pop("shell", True)
    if verbose:
        full_path = Path(".").resolve()
        full_cmd_str = subprocess.list2cmdline(full_cmd_list)
        print(f"Running in {full_path}: {full_cmd_str}")

    env = clean_virtual_env_from_env(**process_args)
    proc = subprocess.Popen(
        full_cmd_list,
        shell=shell,
        env=env,
        **process_args,
    )
    return proc
