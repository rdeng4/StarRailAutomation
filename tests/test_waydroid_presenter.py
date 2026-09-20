from star_rail_automation.presentation.models.waydroid import WaydroidState, WaydroidStatus
from star_rail_automation.presentation.presenters.waydroid_presenter import WaydroidPresenter


class Signal:
    def __init__(self) -> None:
        self.callback = None

    def connect(self, callback) -> None:
        self.callback = callback


class FakeView:
    def __init__(self) -> None:
        self.refresh_requested = Signal()
        self.start_requested = Signal()
        self.config_requested = Signal()
        self.settings_requested = Signal()
        self.exit_requested = Signal()
        self.status = None

    def show_checking(self) -> None:
        pass

    def show_status(self, status) -> None:
        self.status = status

    def show_placeholder(self, page_name: str) -> None:
        pass

    def close(self) -> bool:
        return True


def test_presenter_renders_completed_status() -> None:
    view = FakeView()
    presenter = WaydroidPresenter(view, service=None)  # type: ignore[arg-type]
    status = WaydroidStatus(WaydroidState.READY, "Waydroid is ready.")

    presenter.on_check_completed(status)

    assert view.status is status
