"""
Unit test file.
"""

import os
import shutil
import subprocess
from pathlib import Path

from iso_env.types import IsoEnvArgs, PyProjectToml, Requirements
from iso_env.util import get_verbose_from_env, to_full_cmd_list


def _to_requirements(build_info: Requirements) -> PyProjectToml:
    req_lines = build_info.content.split("\n")
    req_lines = [line.strip() for line in req_lines if line.strip()]
    headers = ["# This file is generated by iso_env.", "# Do not edit this file."]
    headers.append("[project]")
    headers.append('name = "project"')
    if build_info.python_version:
        headers.append(f'requires-python = "{build_info.python_version}"')
    headers.append('version = "0.1.0"')
    if req_lines:
        headers.append("dependencies = [")
        for line in build_info.content.split("\n"):
            headers.append(f'  "{line}",')
        headers.append("]")
    return PyProjectToml("\n".join(headers))


def _to_pyproject_toml(build_info: Requirements | PyProjectToml) -> PyProjectToml:
    if isinstance(build_info, Requirements):
        return _to_requirements(build_info)
    return build_info


# def install(path: Path, requirements_text: str) -> None:
def install(args: IsoEnvArgs, verbose: bool) -> None:
    """Uses isolated_environment to install."""
    # env: dict = dict(os.environ)
    try:
        path = args.venv_path.resolve()
        if installed(args, verbose=verbose):
            if verbose:
                print(f"{path} is already installed.")
            return
        py_project_toml = _to_pyproject_toml(args.build_info)
        # Print installing message
        # Install using isolated_environment
        path.mkdir(exist_ok=True, parents=True)
        cmd_list = ["uv", "venv"]
        cmd_str = subprocess.list2cmdline(cmd_list)
        if verbose:
            print(f"Installing in {path} using command: {cmd_str}")
        try:
            subprocess.run(
                cmd_str,
                cwd=str(path),
                check=True,
                capture_output=True,
                text=True,
                shell=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"Error creating venv: {e}\n: {e.stdout}, \n{e.stderr}")
            raise
        py_project_toml_path = path / "pyproject.toml"
        py_project_toml_path.write_text(str(py_project_toml), encoding="utf-8")
        if verbose:
            cmd_str = subprocess.list2cmdline(cmd_list)
            print(f"Installing in {path} using command: {cmd_str}")
        try:
            _ = subprocess.run(
                cmd_str,
                cwd=str(path),
                check=True,
                capture_output=True,
                text=True,
                shell=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"Error creating venv: {e}\n: {e.stdout}, \n{e.stderr}")
            raise

        (path / "installed").touch()
    except KeyboardInterrupt:
        pass


def purge(venv_path: Path) -> int:
    print("Purging...")
    if not venv_path.exists():
        print("venv_path does not exist.")
        return 0
    try:
        shutil.rmtree(venv_path)
        print("purged successfully.")
        return 0
    except Exception as e:
        print(f"Error purging: {e}")
        return 1


def _santize(context: str) -> str:
    new_lines: list[str] = []
    for line in context.split("\n"):
        line = line.strip()
        if line:
            new_lines.append(line)
    return "\n".join(new_lines)


# def installed(venv_path: Path, requirements_text: str) -> bool:
def installed(args: IsoEnvArgs, verbose: bool) -> bool:
    if verbose:
        print(f"Checking if {args.venv_path} is installed.")
    venv_path = args.venv_path
    if not venv_path.exists():
        if verbose:
            print(f"{venv_path} does not exist.")
        return False
    pyproject_toml_path = venv_path / "pyproject.toml"
    if not pyproject_toml_path.exists():
        if verbose:
            print(f"{pyproject_toml_path} does not exist.")
        return False
    pyproject_toml = _to_pyproject_toml(args.build_info)
    if verbose:
        print(f"Checking {pyproject_toml_path} and {pyproject_toml}")
    if _santize(pyproject_toml_path.read_text()) != _santize(str(pyproject_toml)):
        if verbose:
            print(f"{pyproject_toml_path} is different.")
        return False
    out = (venv_path / "installed").exists()
    if verbose:
        print(f"Installed: {out}")
    return out


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
    env = _get_env(**process_args)
    if verbose:
        full_path = Path(".").resolve()
        full_cmd_str = subprocess.list2cmdline(full_cmd_list)
        print(f"Running in {full_path}: {full_cmd_str}")

    env = _get_env(**process_args)
    proc = subprocess.Popen(
        full_cmd_list,
        shell=shell,
        env=env,
        **process_args,
    )
    return proc


def _get_env(**process_args) -> dict[str, str]:
    if "env" in process_args:
        env = process_args["env"]
        process_args.pop("env")
    else:
        env = dict(os.environ)
    if "VIRTUAL_ENV" in env:
        del env["VIRTUAL_ENV"]
    return env
