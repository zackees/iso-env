"""Test concurrent installation to verify file locking."""

import multiprocessing
import tempfile
import time
from pathlib import Path

from iso_env.api import install
from iso_env.types import IsoEnvArgs, Requirements


def _install_worker(venv_path: Path, worker_id: int, results: list) -> None:
    """Worker function that attempts to install."""
    try:
        args = IsoEnvArgs(
            venv_path=venv_path,
            build_info=Requirements(content="requests", python_version=">=3.10.0"),
        )
        start_time = time.time()
        install(args, verbose=True)
        elapsed = time.time() - start_time
        results.append((worker_id, "success", elapsed))
        print(f"Worker {worker_id} completed in {elapsed:.2f}s")
    except Exception as e:
        results.append((worker_id, "failed", str(e)))
        print(f"Worker {worker_id} failed: {e}")


def test_concurrent_install():
    """Test that concurrent installs don't corrupt the environment."""
    with tempfile.TemporaryDirectory() as tmpdir:
        venv_path = Path(tmpdir) / "test_venv"

        # Use multiprocessing Manager to share results
        manager = multiprocessing.Manager()
        results = manager.list()

        # Start multiple processes trying to install simultaneously
        num_workers = 3
        processes = []

        print(f"\nStarting {num_workers} concurrent installation processes...")
        for i in range(num_workers):
            p = multiprocessing.Process(
                target=_install_worker, args=(venv_path, i, results)
            )
            p.start()
            processes.append(p)

        # Wait for all processes to complete
        for p in processes:
            p.join()

        # Check results
        print(f"\nResults: {list(results)}")

        # All workers should have succeeded
        assert (
            len(results) == num_workers
        ), f"Expected {num_workers} results, got {len(results)}"
        for worker_id, status, _ in results:
            assert status == "success", f"Worker {worker_id} failed"

        # Verify the installation is valid
        assert (venv_path / "installed").exists(), "Installation marker not found"
        assert (venv_path / "pyproject.toml").exists(), "pyproject.toml not found"

        print("✓ All workers completed successfully without corruption")


if __name__ == "__main__":
    test_concurrent_install()
