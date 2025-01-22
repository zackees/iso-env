import subprocess

from iso_env.api import _get_env, install, installed, purge, to_full_cmd_list
from iso_env.types import IsoEnvArgs
from iso_env.util import get_verbose_from_env


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
    env = _get_env(**process_args)
    full_cmd_list = to_full_cmd_list(args, cmd_list, verbose=verbose, **process_args)
    cp = subprocess.run(full_cmd_list, env=env, **process_args)
    return cp
