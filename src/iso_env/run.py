import os
import subprocess
import warnings
from pathlib import Path

from iso_env.api import install, installed, purge
from iso_env.types import IsoEnvArgs
from iso_env.util import get_verbose_from_env, to_full_cmd_list


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
    env = dict(os.environ)
    if "env" in process_args:
        env = process_args.pop("env")
    if "VIRTUAL_ENV" in env:
        del env["VIRTUAL_ENV"]
    full_cmd_list = to_full_cmd_list(args, cmd_list, verbose=verbose, **process_args)
    check = process_args.pop("check", True)
    try:
        cp = subprocess.run(full_cmd_list, env=env, check=check, **process_args)
        return cp
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr
        stdout = exc.stdout
        error_msg = f"Failed to run: {exc.cmd} {exc.returncode}\nstdout: {stdout}\nstderr: {stderr}"
        warnings.warn(error_msg)
        raise


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
    shell = process_args.pop("shell", False)
    if verbose:
        full_path = Path(".").resolve()
        full_cmd_str = subprocess.list2cmdline(full_cmd_list)
        print(f"Running in {full_path}: {full_cmd_str}")

    env = dict(os.environ)
    if "env" in process_args:
        env = process_args.pop("env")
    if "VIRTUAL_ENV" in env:
        del env["VIRTUAL_ENV"]

    proc = subprocess.Popen(  # type: ignore
        full_cmd_list,
        shell=shell,
        env=env,
        **process_args,
    )
    return proc
