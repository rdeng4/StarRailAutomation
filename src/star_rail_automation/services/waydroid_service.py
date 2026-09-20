"""Waydroid command-line integration."""

from __future__ import annotations

import shutil
import subprocess
from collections.abc import Callable

from star_rail_automation.presentation.models.waydroid import WaydroidState, WaydroidStatus


class WaydroidService:
    """Checks whether a locally installed Waydroid session is running."""

    def __init__(
        self,
        find_executable: Callable[[str], str | None] = shutil.which,
        run_command: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
        timeout_seconds: float = 5.0,
    ) -> None:
        self._find_executable = find_executable
        self._run_command = run_command
        self._timeout_seconds = timeout_seconds

    def check_status(self) -> WaydroidStatus:
        executable = self._find_executable("waydroid")
        if executable is None:
            return WaydroidStatus(
                WaydroidState.NOT_INSTALLED,
                "Waydroid is not installed.",
            )

        try:
            result = self._run_command(
                [executable, "status"],
                capture_output=True,
                text=True,
                timeout=self._timeout_seconds,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return WaydroidStatus(WaydroidState.TIMED_OUT, "Waydroid status check timed out.")
        except OSError as error:
            return WaydroidStatus(WaydroidState.COMMAND_FAILED, "Could not run Waydroid.", str(error))

        output = "\n".join(part for part in (result.stdout, result.stderr) if part)
        if result.returncode != 0:
            return WaydroidStatus(
                WaydroidState.COMMAND_FAILED,
                "Waydroid status check failed.",
                output.strip(),
            )
        if "Session:\tRUNNING" in output or "Session: RUNNING" in output:
            return WaydroidStatus(WaydroidState.READY, "Waydroid is ready.")
        if "Session:\tSTOPPED" in output or "Session: STOPPED" in output:
            return WaydroidStatus(WaydroidState.SESSION_STOPPED, "Waydroid session is stopped.")
        return WaydroidStatus(
            WaydroidState.UNKNOWN,
            "Waydroid returned an unrecognized status.",
            output.strip(),
        )
