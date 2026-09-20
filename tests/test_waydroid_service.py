import subprocess

import pytest

from star_rail_automation.presentation.models.waydroid import WaydroidState
from star_rail_automation.services.waydroid_service import WaydroidService


def completed(output: str, returncode: int = 0) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(["waydroid", "status"], returncode, stdout=output, stderr="")


def test_reports_missing_executable() -> None:
    status = WaydroidService(find_executable=lambda _: None).check_status()

    assert status.state is WaydroidState.NOT_INSTALLED


def test_reports_running_session() -> None:
    status = WaydroidService(
        find_executable=lambda _: "/usr/bin/waydroid",
        run_command=lambda *args, **kwargs: completed("Session:\tRUNNING"),
    ).check_status()

    assert status.is_ready


def test_reports_stopped_session() -> None:
    status = WaydroidService(
        find_executable=lambda _: "/usr/bin/waydroid",
        run_command=lambda *args, **kwargs: completed("Session:\tSTOPPED"),
    ).check_status()

    assert status.state is WaydroidState.SESSION_STOPPED


def test_reports_command_failure() -> None:
    status = WaydroidService(
        find_executable=lambda _: "/usr/bin/waydroid",
        run_command=lambda *args, **kwargs: completed("broken", returncode=1),
    ).check_status()

    assert status.state is WaydroidState.COMMAND_FAILED


def test_reports_timeout() -> None:
    def timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired("waydroid", 5)

    status = WaydroidService(find_executable=lambda _: "/usr/bin/waydroid", run_command=timeout).check_status()

    assert status.state is WaydroidState.TIMED_OUT


def test_reports_unrecognized_output() -> None:
    status = WaydroidService(
        find_executable=lambda _: "/usr/bin/waydroid",
        run_command=lambda *args, **kwargs: completed("Vendor type:\tMAINLINE"),
    ).check_status()

    assert status.state is WaydroidState.UNKNOWN
