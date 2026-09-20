"""Models describing the Waydroid state rendered by the presentation layer."""

from dataclasses import dataclass
from enum import Enum


class WaydroidState(Enum):
    READY = "ready"
    NOT_INSTALLED = "not_installed"
    SESSION_STOPPED = "session_stopped"
    COMMAND_FAILED = "command_failed"
    TIMED_OUT = "timed_out"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class WaydroidStatus:
    state: WaydroidState
    message: str
    detail: str = ""

    @property
    def is_ready(self) -> bool:
        return self.state is WaydroidState.READY
