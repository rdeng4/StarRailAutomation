import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication

from star_rail_automation.presentation.models.waydroid import WaydroidState, WaydroidStatus
from star_rail_automation.presentation.views.landing_view import LandingView


def test_landing_view_has_required_controls() -> None:
    app = QApplication.instance() or QApplication([])
    view = LandingView()
    view.show()
    app.processEvents()

    assert view.findChild(type(view.start_button), "startButton") is view.start_button
    assert view.findChild(type(view.config_button), "configButton") is view.config_button
    assert view.findChild(type(view.settings_button), "settingsButton") is view.settings_button
    assert view.findChild(type(view.exit_button), "exitButton") is view.exit_button
    assert abs(view.start_button.geometry().center().x() - view.rect().center().x()) <= 1
    assert view.settings_button.geometry().x() < view.exit_button.geometry().x()


def test_landing_view_renders_status() -> None:
    view = LandingView()

    view.show_status(WaydroidStatus(WaydroidState.READY, "Waydroid is ready."))

    assert view.status_label.text() == "Waydroid is ready."
