import os
import subprocess
import warnings
from pathlib import Path

from iso_env.api import install, installed, purge
from iso_env.types import IsoEnvArgs
from iso_env.util import get_verbose_from_env, to_full_cmd_list


def _to_str(src: bytes | str | list[str] | None) -> str:
    if src is None:
        return ""
    if isinstance(src, list):
        return subprocess.list2cmdline(src)
    if isinstance(src, str):
        return src
    return src.decode("utf-8")


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
        shell = process_args.pop("shell", False)
        cp = subprocess.run(
            full_cmd_list, env=env, check=check, shell=shell, **process_args
        )
        return cp
    except subprocess.CalledProcessError as exc:
        warn_errors = os.environ.get("ISO_ENV_WARN_ERRORS", "0") == "1"
        if warn_errors:
            stderr = _to_str(exc.stderr)
            stdout = _to_str(exc.stdout)
            cmd_str = _to_str(full_cmd_list)
            error_msg = f"\n\nFailed to run:\n  {cmd_str}\n{exc.returncode}\n\nstdout: {stdout}\nstderr: {stderr}\n\n"
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
