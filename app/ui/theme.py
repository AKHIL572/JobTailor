"""
Theme / stylesheet for JobTailor.
Supports "dark" and "light" modes.
Uses a modern, premium design with generous breathing room and clear visual hierarchy.
"""

from __future__ import annotations

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont


DARK_STYLESHEET = """
/* ─────── Base & Global ─────── */
QWidget {
    background-color: #0f1117;
    color: #e8eaf0;
    font-family: 'Segoe UI', 'Inter', -apple-system, sans-serif;
    font-size: 13px;
}

QLabel {
    background-color: transparent;
    color: #e8eaf0;
}

QMainWindow {
    background-color: #0f1117;
}

/* ─────── Sidebar (Legacy / Subwidgets) ─────── */
QListWidget#sidebar {
    background-color: #141720;
    border: none;
    border-right: 1px solid #1e2235;
    padding: 8px 0px;
    font-size: 13px;
    outline: none;
}
QListWidget#sidebar::item {
    padding: 12px 20px;
    border-radius: 8px;
    margin: 2px 8px;
    color: #8b90a0;
}
QListWidget#sidebar::item:selected {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #5b6af0, stop:1 #7c3aed);
    color: #ffffff;
    font-weight: 600;
}
QListWidget#sidebar::item:hover:!selected {
    background-color: #1e2235;
    color: #c8cad8;
}

/* ─────── Base Buttons ─────── */
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #5b6af0, stop:1 #7c3aed);
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 8px 20px;
    font-weight: 600;
    font-size: 13px;
    min-height: 32px;
}
QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #6b7af8, stop:1 #8c4aff);
}
QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #4b5ae0, stop:1 #6c2add);
}
QPushButton:disabled {
    background-color: #2a2d3e;
    color: #555870;
}
QPushButton#secondary {
    background: #1c2236;
    color: #cbd5e1;
    border: 1px solid #2d3856;
}
QPushButton#secondary:hover {
    background: #252d47;
    border-color: #5b6af0;
    color: #ffffff;
}
QPushButton#danger {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #dc2626, stop:1 #b91c1c);
    color: #fff;
}
QPushButton#success {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #059669, stop:1 #047857);
    color: #fff;
}

/* ─────── Text areas & inputs ─────── */
QTextEdit, QPlainTextEdit {
    background-color: #141720;
    color: #e8eaf0;
    border: 1px solid #1e2235;
    border-radius: 8px;
    padding: 10px;
    font-size: 13px;
    selection-background-color: #5b6af0;
}
QTextEdit:focus, QPlainTextEdit:focus {
    border: 1px solid #5b6af0;
}
QLineEdit {
    background-color: #141720;
    color: #e8eaf0;
    border: 1px solid #1e2235;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 13px;
    selection-background-color: #5b6af0;
}
QLineEdit:focus {
    border: 1px solid #5b6af0;
}

/* ─────── Tab widget ─────── */
QTabWidget::pane {
    background-color: #141720;
    border: 1px solid #1e2235;
    border-radius: 0 0 8px 8px;
}
QTabBar::tab {
    background-color: #0f1117;
    color: #8b90a0;
    padding: 10px 18px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    margin-right: 2px;
    font-weight: 500;
}
QTabBar::tab:selected {
    background-color: #141720;
    color: #ffffff;
    font-weight: 600;
    border-top: 2px solid #5b6af0;
}
QTabBar::tab:hover:!selected {
    background-color: #191c28;
    color: #c8cad8;
}

/* ─────── Headings ─────── */
QLabel#header {
    font-size: 22px;
    font-weight: 700;
    color: #ffffff;
}
QLabel#subheader {
    font-size: 14px;
    color: #94a3b8;
}
QLabel#verdict_strongly_apply {
    color: #10b981;
    font-size: 20px;
    font-weight: 700;
}
QLabel#verdict_apply {
    color: #34d399;
    font-size: 20px;
    font-weight: 700;
}
QLabel#verdict_caution {
    color: #f59e0b;
    font-size: 20px;
    font-weight: 700;
}
QLabel#verdict_dont {
    color: #f87171;
    font-size: 20px;
    font-weight: 700;
}
QLabel#verdict_strongly_dont {
    color: #dc2626;
    font-size: 20px;
    font-weight: 700;
}

/* ─────── Progress bar ─────── */
QProgressBar {
    background-color: #1e2235;
    border-radius: 4px;
    height: 6px;
    text-align: center;
    color: transparent;
}
QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #5b6af0, stop:1 #7c3aed);
    border-radius: 4px;
}

/* ─────── Combo box ─────── */
QComboBox {
    background-color: #141720;
    color: #e8eaf0;
    border: 1px solid #1e2235;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 13px;
    min-height: 28px;
}
QComboBox::drop-down {
    border: none;
    width: 20px;
}
QComboBox QAbstractItemView {
    background-color: #141720;
    color: #e8eaf0;
    border: 1px solid #2a2d3e;
    selection-background-color: #5b6af0;
}

/* ─────── Scroll bars ─────── */
QScrollBar:vertical {
    background: #0f1117;
    width: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #2a2d3e;
    border-radius: 4px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background: #5b6af0;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal {
    background: #0f1117;
    height: 8px;
    border-radius: 4px;
}
QScrollBar::handle:horizontal {
    background: #2a2d3e;
    border-radius: 4px;
    min-width: 30px;
}
QScrollBar::handle:horizontal:hover { background: #5b6af0; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }

/* ─────── Group boxes ─────── */
QGroupBox {
    border: 1px solid #1e2235;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 8px;
    color: #8b90a0;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
}

/* ─────── Table / List ─────── */
QTableWidget, QListWidget {
    background-color: #141720;
    alternate-background-color: #191c2a;
    gridline-color: #1e2235;
    border: 1px solid #1e2235;
    border-radius: 8px;
}
QTableWidget::item, QListWidget::item {
    padding: 6px 10px;
}
QTableWidget::item:selected, QListWidget::item:selected {
    background-color: #5b6af0;
    color: #fff;
}
QHeaderView::section {
    background-color: #1a1d2e;
    color: #8b90a0;
    padding: 6px 10px;
    border: none;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
}

/* ─────── Check box ─────── */
QCheckBox {
    spacing: 8px;
    color: #e8eaf0;
}
QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 4px;
    border: 1px solid #2a2d3e;
    background: #141720;
}
QCheckBox::indicator:checked {
    background: #5b6af0;
    border-color: #5b6af0;
}

/* ─────── Splitter ─────── */
QSplitter::handle {
    background-color: #1e2235;
}
QSplitter::handle:horizontal { width: 1px; }
QSplitter::handle:vertical { height: 1px; }

/* ─────── Status bar ─────── */
QStatusBar {
    background-color: #0a0c12;
    color: #8b90a0;
    font-size: 11px;
    border-top: 1px solid #1e2235;
}

/* ─────── Tooltip ─────── */
QToolTip {
    background-color: #1e2235;
    color: #e8eaf0;
    border: 1px solid #2a2d3e;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
}

/* ─────── Spin box ─────── */
QSpinBox, QDoubleSpinBox {
    background-color: #141720;
    color: #e8eaf0;
    border: 1px solid #1e2235;
    border-radius: 6px;
    padding: 4px 8px;
}

/* ═══════════════════════════════════════════════════════════════════
   CUSTOM COMPONENT STYLES (Cleanly placed to override base widgets)
   ═══════════════════════════════════════════════════════════════════ */

/* ─────── Top Navigation Bar ─────── */
QWidget#top_bar {
    background-color: #141720;
    border-bottom: 1px solid #1e2235;
}
QLabel#app_logo_badge {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #5b6af0, stop:1 #8c4aff);
    color: #ffffff;
    font-weight: 800;
    font-size: 14px;
    border-radius: 8px;
}
QLabel#brand_title {
    color: #ffffff;
    font-size: 16px;
    font-weight: 700;
    background: transparent;
}
QLabel#brand_tagline {
    color: #8b90a0;
    font-size: 12px;
    background: transparent;
}
QFrame#top_bar_sep {
    color: #1e2235;
    background-color: #1e2235;
}
QPushButton#top_nav_btn {
    background: transparent;
    color: #8b90a0;
    border: 1px solid transparent;
    border-radius: 8px;
    padding: 7px 16px;
    font-weight: 600;
    font-size: 13px;
    min-height: 28px;
}
QPushButton#top_nav_btn:hover {
    background-color: #1e2235;
    color: #e8eaf0;
}
QPushButton#top_nav_btn:checked {
    background: #1e2235;
    color: #ffffff;
    border: 1px solid #5b6af0;
}
QPushButton#user_chip {
    background-color: #1e2235;
    color: #cbd5e1;
    border: 1px solid #2a2d3e;
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 12px;
    font-weight: 600;
}
QPushButton#user_chip:hover {
    background-color: #262a40;
    border-color: #5b6af0;
    color: #ffffff;
}
QPushButton#menu_btn {
    background: #1e2235;
    color: #cbd5e1;
    border: 1px solid #2a2d3e;
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 13px;
    font-weight: 700;
}
QPushButton#menu_btn:hover {
    background: #262a40;
    border-color: #5b6af0;
    color: #ffffff;
}

/* ─────── QMenu (Dropdowns) ─────── */
QMenu {
    background-color: #141720;
    border: 1px solid #2a2d3e;
    border-radius: 8px;
    padding: 6px;
    color: #e8eaf0;
    font-size: 13px;
}
QMenu::item {
    padding: 8px 16px;
    border-radius: 6px;
    margin: 2px 0px;
    background-color: transparent;
}
QMenu::item:selected {
    background-color: #5b6af0;
    color: #ffffff;
}
QMenu::separator {
    height: 1px;
    background: #1e2235;
    margin: 4px 8px;
}

/* ─────── Back Button ─────── */
QPushButton#back_btn {
    background-color: #141720;
    color: #8b90a0;
    border: 1px solid #1e2235;
    border-radius: 6px;
    padding: 6px 14px;
    font-weight: 600;
    font-size: 12px;
}
QPushButton#back_btn:hover {
    background-color: #1e2235;
    color: #ffffff;
    border-color: #5b6af0;
}

/* ─────── Dashboard Page Styles ─────── */
QScrollArea#dashboard_scroll {
    background-color: #0f1117;
    border: none;
}
QWidget#dashboard_content {
    background-color: #0f1117;
}

/* Profile Hero Card */
QFrame#profile_hero_card {
    background-color: #141724;
    border: 1px solid #23283c;
    border-radius: 14px;
}
QLabel#hero_avatar {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #5b6af0, stop:1 #8c4aff);
    color: #ffffff;
    font-size: 21px;
    font-weight: 800;
    border-radius: 29px;
}
QLabel#hero_name {
    color: #ffffff;
    font-size: 22px;
    font-weight: 700;
    background: transparent;
}
QLabel#badge_verified {
    background-color: #064e3b;
    color: #34d399;
    font-size: 11px;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 12px;
}
QLabel#hero_headline {
    color: #94a3b8;
    font-size: 13px;
    background: transparent;
}
QPushButton#hero_chip {
    background-color: #1a1e2e;
    color: #cbd5e1;
    border: 1px solid #283046;
    border-radius: 15px;
    padding: 6px 14px;
    font-size: 12px;
    font-weight: 500;
}
QPushButton#hero_chip:hover {
    background-color: #242c44;
    color: #ffffff;
    border-color: #5b6af0;
}

/* Stat Cards */
QFrame#stat_card {
    background-color: #141724;
    border: 1px solid #23283c;
    border-radius: 14px;
}
QFrame#stat_card:hover {
    border-color: #363e5e;
    background-color: #171c2c;
}
QLabel#stat_icon_badge {
    background-color: #1c2236;
    border-radius: 10px;
    font-size: 18px;
    color: #818cf8;
}
QLabel#stat_title {
    color: #818cf8;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.8px;
    background: transparent;
}
QLabel#stat_value {
    color: #ffffff;
    font-size: 24px;
    font-weight: 700;
    margin: 4px 0px;
    background: transparent;
}
QLabel#stat_sub {
    color: #94a3b8;
    font-size: 12px;
    background: transparent;
}

/* Feature Section Headings */
QLabel#section_header {
    color: #ffffff;
    font-size: 18px;
    font-weight: 700;
    background: transparent;
}
QLabel#section_sub {
    color: #94a3b8;
    font-size: 13px;
    line-height: 1.5;
    margin-top: 4px;
    margin-bottom: 8px;
    background: transparent;
}

/* Feature Cards */
QFrame#feature_card {
    background-color: #141724;
    border: 1px solid #23283c;
    border-radius: 14px;
}
QFrame#feature_card:hover {
    border-color: #3d4668;
    background-color: #171c2c;
}
QLabel#feature_icon_badge {
    background-color: #1c2236;
    border-radius: 10px;
    font-size: 20px;
    font-weight: bold;
    color: #818cf8;
}
QLabel#badge_primary {
    background-color: #312e81;
    color: #c7d2fe;
    font-size: 11px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 6px;
    letter-spacing: 0.5px;
}
QLabel#badge_purple {
    background-color: #4c1d95;
    color: #e9d5ff;
    font-size: 11px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 6px;
    letter-spacing: 0.5px;
}
QLabel#badge_green {
    background-color: #064e3b;
    color: #a7f3d0;
    font-size: 11px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 6px;
    letter-spacing: 0.5px;
}
QLabel#badge_blue {
    background-color: #1e3a8a;
    color: #bfdbfe;
    font-size: 11px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 6px;
    letter-spacing: 0.5px;
}
QLabel#badge_default {
    background-color: #1e2235;
    color: #8b90a0;
    font-size: 11px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 6px;
    letter-spacing: 0.5px;
}
QLabel#feature_title {
    color: #ffffff;
    font-size: 16px;
    font-weight: 700;
    margin-top: 2px;
    background: transparent;
}
QLabel#feature_desc {
    color: #94a3b8;
    font-size: 13px;
    background: transparent;
}
QPushButton#feature_btn_primary {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #5b6af0, stop:1 #7c3aed);
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 10px 22px;
    font-weight: 600;
    font-size: 13px;
    min-height: 38px;
}
QPushButton#feature_btn_primary:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6b7af8, stop:1 #8c4aff);
}
QPushButton#feature_btn_secondary {
    background-color: #1b2032;
    color: #e2e8f0;
    border: 1px solid #2d3652;
    border-radius: 8px;
    padding: 10px 22px;
    font-weight: 600;
    font-size: 13px;
    min-height: 38px;
}
QPushButton#feature_btn_secondary:hover {
    background-color: #242c46;
    border-color: #5b6af0;
    color: #ffffff;
}

/* Recent Job Rows */
QFrame#recent_job_row {
    background-color: #141724;
    border: 1px solid #23283c;
    border-radius: 10px;
}
QFrame#recent_job_row:hover {
    border-color: #363e5e;
    background-color: #171c2c;
}
QFrame#empty_state_frame {
    background-color: #141724;
    border: 1px dashed #2d3652;
    border-radius: 12px;
}
"""


LIGHT_STYLESHEET = """
/* ─────── Base & Global (Light) ─────── */
QWidget {
    background-color: #f8f9fc;
    color: #1a1d2e;
    font-family: 'Segoe UI', 'Inter', -apple-system, sans-serif;
    font-size: 13px;
}

QLabel {
    background-color: transparent;
    color: #1a1d2e;
}

QMainWindow { background-color: #f0f2f8; }

/* ─────── Base Buttons (Light) ─────── */
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #5b6af0, stop:1 #7c3aed);
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 8px 20px;
    font-weight: 600;
    font-size: 13px;
    min-height: 32px;
}
QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #6b7af8, stop:1 #8c4aff);
}
QPushButton#secondary {
    background: #f0f2fa;
    color: #1a1d2e;
    border: 1px solid #d8dcee;
}
QPushButton#secondary:hover {
    background: #e4e7f5;
    color: #1a1d2e;
}

/* ─────── Text areas & inputs (Light) ─────── */
QTextEdit, QPlainTextEdit {
    background-color: #ffffff;
    color: #1a1d2e;
    border: 1px solid #d8dcee;
    border-radius: 8px;
    padding: 10px;
    font-size: 13px;
    selection-background-color: #5b6af0;
}
QLineEdit {
    background-color: #ffffff;
    color: #1a1d2e;
    border: 1px solid #d8dcee;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 13px;
}

/* ─────── Tab widget (Light) ─────── */
QTabWidget::pane {
    background-color: #ffffff;
    border: 1px solid #e2e5f0;
    border-radius: 0 0 8px 8px;
}
QTabBar::tab {
    background-color: #f0f2f8;
    color: #6b7080;
    padding: 10px 18px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background-color: #ffffff;
    color: #1a1d2e;
    font-weight: 600;
    border-top: 2px solid #5b6af0;
}

/* ─────── Group Box (Light) ─────── */
QGroupBox {
    border: 1px solid #e2e5f0;
    border-radius: 8px;
    margin-top: 12px;
    color: #6b7080;
    font-size: 11px;
    font-weight: 600;
}

/* ─────── Scroll Bar & Progress Bar (Light) ─────── */
QScrollBar:vertical { background: #f0f2f8; width: 8px; border-radius: 4px; }
QScrollBar::handle:vertical { background: #c8cce0; border-radius: 4px; min-height: 30px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QProgressBar { background-color: #e2e5f0; border-radius: 4px; height: 6px; color: transparent; }
QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #5b6af0, stop:1 #7c3aed);
    border-radius: 4px;
}
QStatusBar { background-color: #eef0fa; color: #6b7080; font-size: 11px; }

/* ─────── Headings (Light) ─────── */
QLabel#header { font-size: 22px; font-weight: 700; color: #1a1d2e; }
QLabel#subheader { font-size: 14px; color: #6b7080; }

/* ═══════════════════════════════════════════════════════════════════
   CUSTOM COMPONENT STYLES (Light Mode)
   ═══════════════════════════════════════════════════════════════════ */

/* ─────── Top Navigation Bar (Light) ─────── */
QWidget#top_bar {
    background-color: #ffffff;
    border-bottom: 1px solid #e2e5f0;
}
QLabel#app_logo_badge {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #5b6af0, stop:1 #8c4aff);
    color: #ffffff;
    font-weight: 800;
    font-size: 14px;
    border-radius: 8px;
}
QLabel#brand_title {
    color: #1a1d2e;
    font-size: 16px;
    font-weight: 700;
    background: transparent;
}
QLabel#brand_tagline {
    color: #6b7080;
    font-size: 12px;
    background: transparent;
}
QFrame#top_bar_sep {
    color: #e2e5f0;
    background-color: #e2e5f0;
}
QPushButton#top_nav_btn {
    background: transparent;
    color: #6b7080;
    border: 1px solid transparent;
    border-radius: 8px;
    padding: 7px 16px;
    font-weight: 600;
    font-size: 13px;
    min-height: 28px;
}
QPushButton#top_nav_btn:hover {
    background-color: #f0f2fa;
    color: #1a1d2e;
}
QPushButton#top_nav_btn:checked {
    background: #f0f2fa;
    color: #5b6af0;
    border: 1px solid #5b6af0;
}
QPushButton#user_chip {
    background-color: #f0f2fa;
    color: #1a1d2e;
    border: 1px solid #e2e5f0;
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 12px;
    font-weight: 600;
}
QPushButton#user_chip:hover {
    background-color: #e4e7f5;
    border-color: #5b6af0;
}
QPushButton#menu_btn {
    background: #f0f2fa;
    color: #1a1d2e;
    border: 1px solid #e2e5f0;
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 13px;
    font-weight: 700;
}
QPushButton#menu_btn:hover {
    background: #e4e7f5;
    border-color: #5b6af0;
}

/* ─────── QMenu (Light) ─────── */
QMenu {
    background-color: #ffffff;
    border: 1px solid #e2e5f0;
    border-radius: 8px;
    padding: 6px;
    color: #1a1d2e;
    font-size: 13px;
}
QMenu::item {
    padding: 8px 16px;
    border-radius: 6px;
    margin: 2px 0px;
    background-color: transparent;
}
QMenu::item:selected {
    background-color: #5b6af0;
    color: #ffffff;
}
QMenu::separator {
    height: 1px;
    background: #e2e5f0;
    margin: 4px 8px;
}

/* ─────── Back Button (Light) ─────── */
QPushButton#back_btn {
    background-color: #ffffff;
    color: #6b7080;
    border: 1px solid #e2e5f0;
    border-radius: 6px;
    padding: 6px 14px;
    font-weight: 600;
    font-size: 12px;
}
QPushButton#back_btn:hover {
    background-color: #f0f2fa;
    color: #1a1d2e;
    border-color: #5b6af0;
}

/* ─────── Dashboard Styles (Light) ─────── */
QScrollArea#dashboard_scroll { background-color: #f0f2f8; border: none; }
QWidget#dashboard_content { background-color: #f0f2f8; }
QFrame#profile_hero_card {
    background-color: #ffffff;
    border: 1px solid #e2e5f0;
    border-radius: 14px;
}
QLabel#hero_avatar {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #5b6af0, stop:1 #8c4aff);
    color: #ffffff;
    font-size: 21px;
    font-weight: 800;
    border-radius: 29px;
}
QLabel#hero_name { color: #1a1d2e; font-size: 22px; font-weight: 700; background: transparent; }
QLabel#badge_verified {
    background-color: #d1fae5;
    color: #065f46;
    font-size: 11px;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 12px;
}
QLabel#hero_headline { color: #6b7080; font-size: 13px; background: transparent; }
QPushButton#hero_chip {
    background-color: #f0f2fa;
    color: #4b5563;
    border: 1px solid #e2e5f0;
    border-radius: 15px;
    padding: 6px 14px;
    font-size: 12px;
    font-weight: 500;
}
QPushButton#hero_chip:hover { background-color: #e4e7f5; color: #1a1d2e; border-color: #5b6af0; }

/* Stat Cards (Light) */
QFrame#stat_card { background-color: #ffffff; border: 1px solid #e2e5f0; border-radius: 14px; }
QFrame#stat_card:hover { border-color: #c8cce0; }
QLabel#stat_icon_badge {
    background-color: #f0f2fa;
    border-radius: 10px;
    font-size: 18px;
    color: #5b6af0;
}
QLabel#stat_title { color: #5b6af0; font-size: 11px; font-weight: 700; letter-spacing: 0.8px; }
QLabel#stat_value { color: #1a1d2e; font-size: 24px; font-weight: 700; margin: 4px 0px; }
QLabel#stat_sub { color: #8b90a0; font-size: 12px; }

/* Feature Cards (Light) */
QLabel#section_header { color: #1a1d2e; font-size: 18px; font-weight: 700; }
QLabel#section_sub { color: #6b7080; font-size: 13px; line-height: 1.5; margin-top: 4px; margin-bottom: 8px; }
QFrame#feature_card { background-color: #ffffff; border: 1px solid #e2e5f0; border-radius: 14px; }
QFrame#feature_card:hover { border-color: #c8cce0; }
QLabel#feature_icon_badge {
    background-color: #f0f2fa;
    border-radius: 10px;
    font-size: 20px;
    font-weight: bold;
    color: #5b6af0;
}
QLabel#badge_primary {
    background-color: #e0e7ff;
    color: #3730a3;
    font-size: 11px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 6px;
    letter-spacing: 0.5px;
}
QLabel#badge_purple {
    background-color: #f3e8ff;
    color: #6b21a8;
    font-size: 11px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 6px;
    letter-spacing: 0.5px;
}
QLabel#badge_green {
    background-color: #d1fae5;
    color: #065f46;
    font-size: 11px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 6px;
    letter-spacing: 0.5px;
}
QLabel#badge_blue {
    background-color: #dbeafe;
    color: #1e40af;
    font-size: 11px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 6px;
    letter-spacing: 0.5px;
}
QLabel#badge_default {
    background-color: #f0f2fa;
    color: #5b6af0;
    font-size: 11px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 6px;
    letter-spacing: 0.5px;
}
QLabel#feature_title { color: #1a1d2e; font-size: 16px; font-weight: 700; margin-top: 2px; }
QLabel#feature_desc { color: #6b7080; font-size: 13px; }
QPushButton#feature_btn_primary {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #5b6af0, stop:1 #7c3aed);
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 10px 22px;
    font-weight: 600;
    font-size: 13px;
    min-height: 38px;
}
QPushButton#feature_btn_primary:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6b7af8, stop:1 #8c4aff);
}
QPushButton#feature_btn_secondary {
    background-color: #f0f2fa;
    color: #1a1d2e;
    border: 1px solid #d8dcee;
    border-radius: 8px;
    padding: 10px 22px;
    font-weight: 600;
    font-size: 13px;
    min-height: 38px;
}
QPushButton#feature_btn_secondary:hover {
    background-color: #e4e7f5;
    border-color: #5b6af0;
}

QFrame#recent_job_row { background-color: #ffffff; border: 1px solid #e2e5f0; border-radius: 10px; }
QFrame#recent_job_row:hover { border-color: #c8cce0; }
QFrame#empty_state_frame { background-color: #ffffff; border: 1px dashed #c8cce0; border-radius: 12px; }
"""


def apply_theme(app: QApplication, theme: str) -> None:
    """Apply the chosen theme stylesheet to the application."""
    if theme == "light":
        app.setStyleSheet(LIGHT_STYLESHEET)
    else:
        app.setStyleSheet(DARK_STYLESHEET)

    # Set default font
    font = QFont("Segoe UI", 10)
    font.setHintingPreference(QFont.HintingPreference.PreferFullHinting)
    app.setFont(font)
