"""Presenter coordinating the landing view and Waydroid service."""

from __future__ import annotations

from typing import Protocol

from PySide6.QtCore import QObject, QThread, Signal, Slot

from star_rail_automation.presentation.models.waydroid import WaydroidStatus
from star_rail_automation.services.waydroid_service import WaydroidService


class LandingViewPort(Protocol):
    refresh_requested: Signal
    start_requested: Signal
    config_requested: Signal
    settings_requested: Signal
    exit_requested: Signal

    def show_checking(self) -> None: ...
    def show_status(self, status: WaydroidStatus) -> None: ...
    def show_placeholder(self, page_name: str) -> None: ...
    def close(self) -> bool: ...


class StatusCheckWorker(QObject):
    completed = Signal(object)

    def __init__(self, service: WaydroidService) -> None:
        super().__init__()
        self._service = service

    @Slot()
    def check(self) -> None:
        self.completed.emit(self._service.check_status())


class WaydroidPresenter(QObject):
    """Coordinates landing-page interactions without putting logic in the view."""

    def __init__(self, view: LandingViewPort, service: WaydroidService) -> None:
        super().__init__()
        self._view = view
        self._service = service
        self._thread: QThread | None = None
        self._worker: StatusCheckWorker | None = None
        view.refresh_requested.connect(self.refresh)
        view.start_requested.connect(lambda: self._view.show_placeholder("Start"))
        view.config_requested.connect(lambda: self._view.show_placeholder("Config"))
        view.settings_requested.connect(lambda: self._view.show_placeholder("Settings"))
        view.exit_requested.connect(self._view.close)

    def start(self) -> None:
        self.refresh()

    @Slot()
    def refresh(self) -> None:
        if self._thread is not None:
            return
        self._view.show_checking()
        self._thread = QThread(self)
        self._worker = StatusCheckWorker(self._service)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.check)
        self._worker.completed.connect(self.on_check_completed)
        self._worker.completed.connect(self._thread.quit)
        self._worker.completed.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)
        self._thread.finished.connect(self._clear_worker)
        self._thread.start()

    @Slot(object)
    def on_check_completed(self, status: WaydroidStatus) -> None:
        self._view.show_status(status)

    @Slot()
    def _clear_worker(self) -> None:
        self._thread = None
        self._worker = None
