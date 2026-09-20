"""Landing-page widgets and rendering."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from star_rail_automation.presentation.models.waydroid import WaydroidStatus


class LandingView(QWidget):
    """The passive landing-page view exposed to its presenter."""

    refresh_requested = Signal()
    start_requested = Signal()
    config_requested = Signal()
    settings_requested = Signal()
    exit_requested = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Star Rail Automation")
        self.resize(640, 440)

        root = QVBoxLayout(self)
        root.setContentsMargins(32, 28, 32, 24)

        self.status_card = QFrame(objectName="waydroidStatusCard")
        status_layout = QHBoxLayout(self.status_card)
        self.status_label = QLabel("Checking Waydroid…", objectName="waydroidStatusLabel")
        self.refresh_button = QPushButton("Refresh", objectName="refreshButton")
        self.refresh_button.clicked.connect(self.refresh_requested)
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        status_layout.addWidget(self.refresh_button)
        root.addWidget(self.status_card)

        root.addStretch()
        main_actions = QVBoxLayout()
        self.start_button = QPushButton("Start", objectName="startButton")
        self.config_button = QPushButton("Config", objectName="configButton")
        self.start_button.clicked.connect(self.start_requested)
        self.config_button.clicked.connect(self.config_requested)
        main_actions.addWidget(self.start_button, alignment=Qt.AlignmentFlag.AlignHCenter)
        main_actions.addWidget(self.config_button, alignment=Qt.AlignmentFlag.AlignHCenter)
        root.addLayout(main_actions)
        root.addStretch()

        footer = QHBoxLayout()
        footer.addStretch()
        self.settings_button = QPushButton("Settings", objectName="settingsButton")
        self.exit_button = QPushButton("Exit", objectName="exitButton")
        self.settings_button.clicked.connect(self.settings_requested)
        self.exit_button.clicked.connect(self.exit_requested)
        footer.addWidget(self.settings_button)
        footer.addWidget(self.exit_button)
        root.addLayout(footer)

    def show_checking(self) -> None:
        self.status_label.setText("Checking Waydroid…")
        self.refresh_button.setEnabled(False)

    def show_status(self, status: WaydroidStatus) -> None:
        self.status_label.setText(status.message)
        self.status_label.setToolTip(status.detail)
        self.refresh_button.setEnabled(True)

    def show_placeholder(self, page_name: str) -> None:
        QMessageBox.information(self, page_name, f"{page_name} is not implemented yet.")
