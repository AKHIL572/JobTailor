"""
Main application window with top navigation bar and dashboard.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QFont
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStackedWidget,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from app.core.data_dirs import data_path, get_data_root
from app.core.profile_loader import get_profile_summary
from app.ui.widgets.top_bar import TopBarWidget
from app.ui.pages.dashboard_page import DashboardPage
from app.ui.pages.new_job_page import NewJobPage
from app.ui.pages.history_page import HistoryPage
from app.ui.pages.profile_page import ProfilePage
from app.ui.pages.template_page import TemplatePage
from app.ui.pages.rules_page import RulesPage
from app.ui.pages.settings_page import SettingsPage


class MainWindow(QMainWindow):
    """
    The application's main window.
    Features a modern top navigation bar with quick view switchers, candidate profile chip,
    and a 3-dots/lines options menu in the top right.
    Opens to the Dashboard & Profile overview by default.
    """

    def __init__(self, config: dict[str, Any]):
        super().__init__()
        self.config = config
        self._setup_window()
        self._build_ui()
        self._connect_signals()

    # ------------------------------------------------------------------

    def _setup_window(self) -> None:
        self.setWindowTitle("JobTailor — AI Resume & Career Suite")
        self.setWindowFlags(
            Qt.WindowType.Window
            | Qt.WindowType.WindowSystemMenuHint
            | Qt.WindowType.WindowMinimizeButtonHint
            | Qt.WindowType.WindowMaximizeButtonHint
            | Qt.WindowType.WindowCloseButtonHint
        )

        screen = QApplication.primaryScreen()
        if screen:
            geo = screen.availableGeometry()
            min_width = min(1100, geo.width())
            min_height = min(680, geo.height())
            self.setMinimumSize(min_width, min_height)
            self.resize(min(1440, geo.width()), min(920, geo.height()))
            self.move(
                geo.x() + (geo.width() - self.width()) // 2,
                geo.y() + (geo.height() - self.height()) // 2,
            )
        else:
            self.setMinimumSize(1000, 680)
            self.resize(1400, 900)

    def _build_ui(self) -> None:
        central = QWidget()
        central.setObjectName("central_widget")
        self.setCentralWidget(central)
        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ── Sleek Top Navigation Bar ─────────────────────────────────────────
        profile_summary = get_profile_summary()
        user_name = profile_summary.get("name", "AKHIL T V")
        self.top_bar = TopBarWidget(user_name=user_name, parent=self)
        root_layout.addWidget(self.top_bar)

        # ── Stacked Pages Container ──────────────────────────────────────────
        self.page_stack = QStackedWidget()
        self.page_stack.setObjectName("page_stack")

        self.dashboard_page = DashboardPage(main_window=self)
        self.new_job_page = NewJobPage(self)
        self.history_page = HistoryPage(self)
        self.profile_page = ProfilePage(self)
        self.template_page = TemplatePage(self)
        self.rules_page = RulesPage(self)
        self.settings_page = SettingsPage(self)

        self.pages: dict[str, QWidget] = {
            "dashboard": self.dashboard_page,
            "new_job": self.new_job_page,
            "history": self.history_page,
            "profile": self.profile_page,
            "template": self.template_page,
            "rules": self.rules_page,
            "settings": self.settings_page,
        }

        for page in self.pages.values():
            self.page_stack.addWidget(page)

        root_layout.addWidget(self.page_stack)

        # ── Status Bar ───────────────────────────────────────────────────────
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready · Welcome to JobTailor")

        # Open Dashboard on launch
        self.navigate_to("dashboard")

    def _connect_signals(self) -> None:
        self.top_bar.navigate_requested.connect(self.navigate_to)
        self.dashboard_page.navigate_requested.connect(self.navigate_to)
        self.new_job_page.status_update.connect(self.status_bar.showMessage)

    def navigate_to(self, page_name: str) -> None:
        """Switch to the specified page and refresh its data if appropriate."""
        widget = self.pages.get(page_name)
        if widget:
            self.page_stack.setCurrentWidget(widget)
            self.top_bar.set_active_page(page_name)
            if page_name == "dashboard":
                self.dashboard_page.refresh()
            elif page_name == "history":
                self.history_page._load_history()
            elif page_name == "profile":
                self.profile_page._load()

    def reload_config(self) -> None:
        """Reload config after settings change."""
        from app.core.config import load_config
        self.config = load_config()
        self.dashboard_page.refresh()
