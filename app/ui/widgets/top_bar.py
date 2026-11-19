"""
Top navigation bar widget for JobTailor.
Includes branding, primary view switchers, user profile chip, and the top-right options menu.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

from PySide6.QtCore import Qt, Signal, QPoint
from PySide6.QtGui import QFont, QAction, QCursor
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QMenu,
    QFrame,
)

from app.core.data_dirs import get_data_root


class TopBarWidget(QWidget):
    """
    Persistent sleek top bar across all pages.
    Replaces cluttered sidebars with intuitive top-level navigation and a 3-dots/lines menu.
    """
    navigate_requested = Signal(str)

    def __init__(self, user_name: str = "AKHIL T V", parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setObjectName("top_bar")
        self.setFixedHeight(64)
        self._user_name = user_name
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(16)

        # ── 1. App Brand / Logo ──────────────────────────────────────────────
        brand_widget = QWidget()
        brand_layout = QHBoxLayout(brand_widget)
        brand_layout.setContentsMargins(0, 0, 0, 0)
        brand_layout.setSpacing(10)

        # Gradient App Icon Badge
        self.app_badge = QLabel("JT")
        self.app_badge.setObjectName("app_logo_badge")
        self.app_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.app_badge.setFixedSize(36, 36)

        # Titles
        titles_layout = QHBoxLayout()
        titles_container = QWidget()
        titles_container_layout = QHBoxLayout(titles_container)
        titles_container_layout.setContentsMargins(0, 0, 0, 0)
        titles_container_layout.setSpacing(6)

        brand_title = QLabel("JobTailor")
        brand_title.setObjectName("brand_title")
        brand_title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))

        brand_tagline = QLabel("· AI Resume Tailor")
        brand_tagline.setObjectName("brand_tagline")

        titles_container_layout.addWidget(brand_title)
        titles_container_layout.addWidget(brand_tagline)

        brand_layout.addWidget(self.app_badge)
        brand_layout.addWidget(titles_container)

        layout.addWidget(brand_widget)

        # Subtle separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.VLine)
        sep.setObjectName("top_bar_sep")
        sep.setFixedHeight(24)
        layout.addWidget(sep)

        # ── 2. Primary Navigation Buttons ────────────────────────────────────
        self.dash_btn = QPushButton("📊  Dashboard")
        self.dash_btn.setObjectName("top_nav_btn")
        self.dash_btn.setCheckable(True)
        self.dash_btn.setChecked(True)
        self.dash_btn.clicked.connect(lambda: self.navigate_requested.emit("dashboard"))

        self.new_job_btn = QPushButton("✦  Tailor Resume")
        self.new_job_btn.setObjectName("top_nav_btn")
        self.new_job_btn.setCheckable(True)
        self.new_job_btn.clicked.connect(lambda: self.navigate_requested.emit("new_job"))

        layout.addWidget(self.dash_btn)
        layout.addWidget(self.new_job_btn)

        layout.addStretch()

        # ── 3. Right: User Chip & Options Menu (3 dots / lines) ───────────────
        self.user_chip = QPushButton()
        self.user_chip.setObjectName("user_chip")
        self.user_chip.setToolTip("View & Edit Master Profile Details")
        self.user_chip.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._render_user_chip()
        self.user_chip.clicked.connect(lambda: self.navigate_requested.emit("profile"))
        layout.addWidget(self.user_chip)

        # Three-dots / Hamburger menu button
        self.menu_btn = QPushButton("⋮  Menu")
        self.menu_btn.setObjectName("menu_btn")
        self.menu_btn.setToolTip("Options, History, Settings & Rules")
        self.menu_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._build_options_menu()
        self.menu_btn.clicked.connect(self._show_menu)
        layout.addWidget(self.menu_btn)

    def _render_user_chip(self) -> None:
        initials = "".join([part[0] for part in self._user_name.split() if part])[:2].upper()
        if not initials:
            initials = "ME"
        self.user_chip.setText(f"👤  {self._user_name}")

    def update_user_name(self, name: str) -> None:
        self._user_name = name or "AKHIL T V"
        self._render_user_chip()

    def _build_options_menu(self) -> None:
        self.options_menu = QMenu(self)
        self.options_menu.setObjectName("options_dropdown_menu")

        act_profile = QAction("👤  Master Profile Details", self)
        act_profile.setToolTip("Edit your genuine experience, projects, and contact info")
        act_profile.triggered.connect(lambda: self.navigate_requested.emit("profile"))
        self.options_menu.addAction(act_profile)

        act_history = QAction("⏱  Application History", self)
        act_history.setToolTip("Browse all past tailored jobs, PDFs, and verdicts")
        act_history.triggered.connect(lambda: self.navigate_requested.emit("history"))
        self.options_menu.addAction(act_history)

        self.options_menu.addSeparator()

        act_template = QAction("📄  LaTeX Resume Template", self)
        act_template.setToolTip("Customize the underlying 1-page LaTeX template")
        act_template.triggered.connect(lambda: self.navigate_requested.emit("template"))
        self.options_menu.addAction(act_template)

        act_rules = QAction("⚙  Tailoring Rules", self)
        act_rules.setToolTip("Configure prompt guidelines, ATS keywords, and rules")
        act_rules.triggered.connect(lambda: self.navigate_requested.emit("rules"))
        self.options_menu.addAction(act_rules)

        act_settings = QAction("🔧  System Settings", self)
        act_settings.setToolTip("Configure LLM model, API keys, and Tectonic compiler")
        act_settings.triggered.connect(lambda: self.navigate_requested.emit("settings"))
        self.options_menu.addAction(act_settings)

        self.options_menu.addSeparator()

        act_folder = QAction("📁  Open App Data Directory", self)
        act_folder.triggered.connect(self._open_data_folder)
        self.options_menu.addAction(act_folder)

    def _show_menu(self) -> None:
        pos = self.menu_btn.mapToGlobal(QPoint(0, self.menu_btn.height() + 4))
        self.options_menu.exec(pos)

    def _open_data_folder(self) -> None:
        folder = get_data_root()
        if sys.platform == "win32":
            os.startfile(str(folder))
        elif sys.platform == "darwin":
            subprocess.run(["open", str(folder)], check=False)
        else:
            subprocess.run(["xdg-open", str(folder)], check=False)

    def set_active_page(self, page_name: str) -> None:
        """Update active button state according to current page."""
        self.dash_btn.setChecked(page_name == "dashboard")
        self.new_job_btn.setChecked(page_name == "new_job")

