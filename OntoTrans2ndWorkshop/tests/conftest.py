"""Pytest fixtures and setup functions."""
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def repo_dir() -> Path:
    """Absolute path to the repository directory."""
    return Path(__file__).parent.parent.parent.parent.resolve()


@pytest.fixture(scope="session")
def use_case_dir() -> Path:
    """Absolute path to the meso_multi_sim_demo use case."""
    return Path(__file__).parent.parent.parent.resolve()


@pytest.fixture(scope="session")
def shell_job_case_dir() -> Path:
    """Absolute path to the shell_job version of the use case."""
    return Path(__file__).parent.parent.resolve()
