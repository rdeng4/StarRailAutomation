"""Application entry point."""

import sys

from PySide6.QtWidgets import QApplication

from star_rail_automation.presentation.presenters.waydroid_presenter import WaydroidPresenter
from star_rail_automation.presentation.views.landing_view import LandingView
from star_rail_automation.services.waydroid_service import WaydroidService


def main() -> int:
    app = QApplication(sys.argv)
    view = LandingView()
    presenter = WaydroidPresenter(view, WaydroidService())
    view.show()
    presenter.start()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
