"""
Dashboard & Profile Page for JobTailor.
Serves as the opening view:
- Displays user profile summary (Akhil T V, contact, headline, education)
- Displays live statistics (Total Jobs Tailored, Top Role, ATS pass rate)
- Showcases what the system can do (distinct feature cards with direct actions)
- Shows recent tailored applications with quick PDF & detail actions
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Optional

from PySide6.QtCore import Qt, Signal, QUrl
from PySide6.QtGui import QFont, QDesktopServices, QCursor
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QFrame,
    QSizePolicy,
)

from app.core.history import get_history, get_history_stats
from app.core.profile_loader import get_profile_summary


class DashboardPage(QWidget):
    """
    Main landing dashboard showing:
    1. Candidate Profile Overview (Akhil T V)
    2. Real-time Tailoring Analytics (Total jobs, Top role, ATS pass rate)
    3. Core Capabilities / Feature Showcase
    4. Recent Applications Activity
    """
    navigate_requested = Signal(str)

    def __init__(self, main_window: Any = None, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.main_window = main_window
        self._setup_ui()
        self.refresh()

    def _setup_ui(self) -> None:
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        # Scroll area so dashboard renders beautifully on all screen resolutions
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setObjectName("dashboard_scroll")

        content = QWidget()
        content.setObjectName("dashboard_content")
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(36, 32, 36, 42)
        self.content_layout.setSpacing(32)

        # ── 1. Candidate Profile Hero Card ───────────────────────────────────
        self.profile_hero = self._build_profile_hero()
        self.content_layout.addWidget(self.profile_hero)

        # ── 2. Analytics & Metrics Cards Row ─────────────────────────────────
        self.stats_widget = self._build_stats_section()
        self.content_layout.addWidget(self.stats_widget)

        # ── 3. What JobTailor Can Do — Feature Showcase ──────────────────────
        features_section = self._build_features_section()
        self.content_layout.addWidget(features_section)

        # ── 4. Recent Applications ───────────────────────────────────────────
        self.recent_section = self._build_recent_section()
        self.content_layout.addWidget(self.recent_section)

        self.content_layout.addStretch()

        scroll.setWidget(content)
        outer_layout.addWidget(scroll)

    # ─────────────────────────────────────────────────────────────────────────
    # 1. Profile Hero Section
    # ─────────────────────────────────────────────────────────────────────────
    def _build_profile_hero(self) -> QWidget:
        card = QFrame()
        card.setObjectName("profile_hero_card")
        layout = QHBoxLayout(card)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(24)

        # Avatar initials circle
        self.avatar_label = QLabel("AT")
        self.avatar_label.setObjectName("hero_avatar")
        self.avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.avatar_label.setFixedSize(58, 58)
        layout.addWidget(self.avatar_label)

        # User details column
        info_col = QVBoxLayout()
        info_col.setSpacing(8)

        name_row = QHBoxLayout()
        name_row.setSpacing(12)
        self.name_label = QLabel("AKHIL T V")
        self.name_label.setObjectName("hero_name")
        self.name_label.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))

        verified_badge = QLabel("✓  Master Profile Active")
        verified_badge.setObjectName("badge_verified")
        name_row.addWidget(self.name_label)
        name_row.addWidget(verified_badge)
        name_row.addStretch()
        info_col.addLayout(name_row)

        self.headline_label = QLabel("Data Science Intern · Bachelor of Technology in Computer Science")
        self.headline_label.setObjectName("hero_headline")
        info_col.addWidget(self.headline_label)

        # Contact pills row
        self.contact_row = QHBoxLayout()
        self.contact_row.setSpacing(10)

        self.email_chip = self._create_chip("✉", "Email")
        self.phone_chip = self._create_chip("📱", "Phone")
        self.linkedin_chip = self._create_chip("💼", "LinkedIn", is_link=True)
        self.github_chip = self._create_chip("🐙", "GitHub", is_link=True)
        self.portfolio_chip = self._create_chip("🌐", "Portfolio", is_link=True)

        self.contact_row.addWidget(self.email_chip)
        self.contact_row.addWidget(self.phone_chip)
        self.contact_row.addWidget(self.linkedin_chip)
        self.contact_row.addWidget(self.github_chip)
        self.contact_row.addWidget(self.portfolio_chip)
        self.contact_row.addStretch()

        info_col.addLayout(self.contact_row)
        layout.addLayout(info_col, stretch=1)

        # Quick Hero CTA Buttons
        hero_actions = QVBoxLayout()
        hero_actions.setSpacing(10)
        hero_actions.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        edit_profile_btn = QPushButton("✏  Edit Master Profile")
        edit_profile_btn.setObjectName("secondary")
        edit_profile_btn.setMinimumHeight(40)
        edit_profile_btn.setToolTip("View and edit the master profile Markdown & details")
        edit_profile_btn.clicked.connect(lambda: self.navigate_requested.emit("profile"))

        start_job_btn = QPushButton("✦  Tailor New Job")
        start_job_btn.setObjectName("feature_btn_primary")
        start_job_btn.setMinimumHeight(40)
        start_job_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        start_job_btn.clicked.connect(lambda: self.navigate_requested.emit("new_job"))

        hero_actions.addWidget(start_job_btn)
        hero_actions.addWidget(edit_profile_btn)
        layout.addLayout(hero_actions)

        return card

    def _create_chip(self, icon: str, text: str, is_link: bool = False) -> QPushButton:
        btn = QPushButton(f"{icon}  {text}")
        btn.setObjectName("hero_chip")
        btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor if is_link else Qt.CursorShape.ArrowCursor))
        btn._target_url = ""
        if is_link:
            btn.clicked.connect(lambda: self._open_chip_url(btn))
        return btn

    def _open_chip_url(self, btn: QPushButton) -> None:
        url = getattr(btn, "_target_url", "")
        if url:
            QDesktopServices.openUrl(QUrl(url))

    # ─────────────────────────────────────────────────────────────────────────
    # 2. Stats Section
    # ─────────────────────────────────────────────────────────────────────────
    def _build_stats_section(self) -> QWidget:
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(18)

        # Stat Card 1: Total Jobs Tailored
        self.stat_total_val = QLabel("0")
        card_total = self._build_stat_card(
            "🎯", "TOTAL JOBS TAILORED", self.stat_total_val, "Resumes generated"
        )

        # Stat Card 2: Top / Most Tailored Role
        self.stat_top_role_val = QLabel("Ready for 1st Role")
        card_role = self._build_stat_card(
            "💼", "TOP JOB ROLE", self.stat_top_role_val, "Most tailored target role"
        )

        # Stat Card 3: ATS Match & Pass Rate
        self.stat_pass_rate_val = QLabel("100%")
        card_pass = self._build_stat_card(
            "🛡️", "ATS PASS RATE", self.stat_pass_rate_val, "Passed verification"
        )

        # Stat Card 4: Single Source Truth
        self.stat_source_val = QLabel("220 KB")
        card_source = self._build_stat_card(
            "📄", "MASTER PROFILE ASSETS", self.stat_source_val, "Single source of truth"
        )

        layout.addWidget(card_total)
        layout.addWidget(card_role)
        layout.addWidget(card_pass)
        layout.addWidget(card_source)

        return container

    def _build_stat_card(self, icon: str, title: str, value_label: QLabel, subtext: str) -> QFrame:
        card = QFrame()
        card.setObjectName("stat_card")
        card.setMinimumHeight(136)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(10)

        top_row = QHBoxLayout()
        top_row.setSpacing(10)

        icon_badge = QLabel(icon)
        icon_badge.setObjectName("stat_icon_badge")
        icon_badge.setFixedSize(36, 36)
        icon_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_lbl = QLabel(title)
        title_lbl.setObjectName("stat_title")

        top_row.addWidget(icon_badge)
        top_row.addWidget(title_lbl)
        top_row.addStretch()
        layout.addLayout(top_row)

        value_label.setObjectName("stat_value")
        value_label.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        layout.addWidget(value_label)

        sub_lbl = QLabel(subtext)
        sub_lbl.setObjectName("stat_sub")
        layout.addWidget(sub_lbl)

        return card

    # ─────────────────────────────────────────────────────────────────────────
    # 3. Features Showcase Section ("What JobTailor Can Do")
    # ─────────────────────────────────────────────────────────────────────────
    def _build_features_section(self) -> QWidget:
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        sec_header = QLabel("⚡ What JobTailor Can Do")
        sec_header.setObjectName("section_header")
        sec_header.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))

        sec_sub = QLabel(
            "Explore the integrated features designed to analyze job specs, verify authentic qualifications, "
            "compile 1-page executive resumes, and generate targeted recruiter outreach."
        )
        sec_sub.setObjectName("section_sub")
        sec_sub.setWordWrap(True)

        layout.addWidget(sec_header)
        layout.addWidget(sec_sub)

        grid = QGridLayout()
        grid.setSpacing(22)

        # Feature 1: Tailor Resume to Job Description
        f1 = self._build_feature_card(
            badge="CORE FEATURE",
            icon="✦",
            title="Tailor Resume to Job Description",
            desc=(
                "Paste any Job Description (JD) from LinkedIn, Indeed, or career portals. "
                "JobTailor extracts core requirements and ATS keywords, intelligently selects "
                "your best matching genuine projects, and compiles an executive 1-page LaTeX PDF."
            ),
            btn_text="✦  Start Tailoring Resume",
            target_page="new_job",
            is_primary=True,
            badge_variant="primary",
        )

        # Feature 2: Cold Outreach Email Generator
        f2 = self._build_feature_card(
            badge="RECRUITER OUTREACH",
            icon="✉",
            title="Hiring Manager Cold Email Pitch",
            desc=(
                "Automatically drafts a concise, personalized cold outreach email or cover letter "
                "tailored directly to the hiring manager or recruiter. Emphasizes your matching "
                "experience, key metrics, and embeds your live portfolio links."
            ),
            btn_text="✉  Draft Outreach with Job",
            target_page="new_job",
            badge_variant="purple",
        )

        # Feature 3: Genuineness & ATS Match Score
        f3 = self._build_feature_card(
            badge="ZERO-HALLUCINATION",
            icon="🛡️",
            title="Truthful ATS Match & Fit Verdict",
            desc=(
                "Rigorous pre-evaluation checks your genuine qualifications against the role. "
                "Classifies the role into Strong Fit, Moderate Fit, or Stretch, highlights "
                "gaps, and guarantees zero fabricated experience or fake certifications."
            ),
            btn_text="🛡  View Tailoring Rules",
            target_page="rules",
            badge_variant="green",
        )

        # Feature 4: Application History & Document Archive
        f4 = self._build_feature_card(
            badge="ARCHIVE & OUTPUTS",
            icon="⏱",
            title="Application History & LaTeX Archive",
            desc=(
                "Keep track of every application you tailor. Search past jobs, inspect the "
                "exact LaTeX source code, review email drafts, and open or download generated "
                "PDFs at any time from your local SQLite database."
            ),
            btn_text="⏱  Browse Past Applications",
            target_page="history",
            badge_variant="blue",
        )

        grid.addWidget(f1, 0, 0)
        grid.addWidget(f2, 0, 1)
        grid.addWidget(f3, 1, 0)
        grid.addWidget(f4, 1, 1)

        layout.addLayout(grid)
        return container

    def _build_feature_card(
        self,
        badge: str,
        icon: str,
        title: str,
        desc: str,
        btn_text: str,
        target_page: str,
        is_primary: bool = False,
        badge_variant: str = "primary",
    ) -> QFrame:
        card = QFrame()
        card.setObjectName("feature_card")
        card.setMinimumHeight(240)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(28, 26, 28, 26)
        layout.setSpacing(16)

        # Header with badge and icon
        top_row = QHBoxLayout()
        top_row.setSpacing(12)

        icon_badge = QLabel(icon)
        icon_badge.setObjectName("feature_icon_badge")
        icon_badge.setFixedSize(40, 40)
        icon_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)

        badge_lbl = QLabel(badge)
        badge_lbl.setObjectName(f"badge_{badge_variant}")
        badge_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        top_row.addWidget(icon_badge)
        top_row.addWidget(badge_lbl)
        top_row.addStretch()
        layout.addLayout(top_row)

        title_lbl = QLabel(title)
        title_lbl.setObjectName("feature_title")
        title_lbl.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        layout.addWidget(title_lbl)

        desc_lbl = QLabel()
        desc_lbl.setObjectName("feature_desc")
        desc_lbl.setTextFormat(Qt.TextFormat.RichText)
        desc_lbl.setWordWrap(True)
        desc_lbl.setText(
            f"<div style='line-height: 160%; color: #94a3b8; font-size: 13px;'>{desc}</div>"
        )
        layout.addWidget(desc_lbl)

        layout.addSpacing(6)
        layout.addStretch()

        btn = QPushButton(btn_text)
        btn.setFixedHeight(42)
        if is_primary:
            btn.setObjectName("feature_btn_primary")
        else:
            btn.setObjectName("feature_btn_secondary")
        btn.clicked.connect(lambda: self.navigate_requested.emit(target_page))
        layout.addWidget(btn)

        return card

    # ─────────────────────────────────────────────────────────────────────────
    # 4. Recent Applications Section
    # ─────────────────────────────────────────────────────────────────────────
    def _build_recent_section(self) -> QWidget:
        container = QWidget()
        self.recent_layout = QVBoxLayout(container)
        self.recent_layout.setContentsMargins(0, 0, 0, 0)
        self.recent_layout.setSpacing(12)

        header_row = QHBoxLayout()
        sec_header = QLabel("⏱ Recent Tailored Applications")
        sec_header.setObjectName("section_header")
        sec_header.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        header_row.addWidget(sec_header)
        header_row.addStretch()

        view_all_btn = QPushButton("View All History →")
        view_all_btn.setObjectName("secondary")
        view_all_btn.clicked.connect(lambda: self.navigate_requested.emit("history"))
        header_row.addWidget(view_all_btn)
        self.recent_layout.addLayout(header_row)

        self.recent_items_container = QVBoxLayout()
        self.recent_items_container.setSpacing(8)
        self.recent_layout.addLayout(self.recent_items_container)

        return container

    # ─────────────────────────────────────────────────────────────────────────
    # Refresh Logic
    # ─────────────────────────────────────────────────────────────────────────
    def refresh(self) -> None:
        """Reload profile data, stats, and recent jobs."""
        self._refresh_profile()
        self._refresh_stats_and_recent()

    def _refresh_profile(self) -> None:
        summary = get_profile_summary()
        name = summary.get("name") or "AKHIL T V"
        self.name_label.setText(name)

        initials = "".join([part[0] for part in name.split() if part])[:2].upper()
        self.avatar_label.setText(initials or "AT")

        headline = summary.get("headline") or "Software & Data Engineer"
        self.headline_label.setText(headline)

        # Update contact buttons
        email = summary.get("email", "")
        self.email_chip.setText(f"✉  {email}" if email else "✉  No Email")

        phone = summary.get("phone", "")
        self.phone_chip.setText(f"📱  {phone}" if phone else "📱  No Phone")

        linkedin = summary.get("linkedin", "")
        self.linkedin_chip._target_url = linkedin
        self.linkedin_chip.setVisible(bool(linkedin))

        github = summary.get("github", "")
        self.github_chip._target_url = github
        self.github_chip.setVisible(bool(github))

        website = summary.get("website", "")
        self.portfolio_chip._target_url = website
        self.portfolio_chip.setVisible(bool(website))

        # Also notify main window top bar to update user name
        if self.main_window and hasattr(self.main_window, "top_bar"):
            self.main_window.top_bar.update_user_name(name)

    def _refresh_stats_and_recent(self) -> None:
        stats = get_history_stats()
        total_jobs = stats.get("total_jobs", 0)
        self.stat_total_val.setText(str(total_jobs))

        top_role = stats.get("top_role", "No jobs yet")
        top_role_count = stats.get("top_role_count", 0)
        if total_jobs > 0:
            self.stat_top_role_val.setText(f"{top_role[:24]} ({top_role_count})")
        else:
            self.stat_top_role_val.setText("Ready for 1st Role")

        passed_count = stats.get("passed_count", 0)
        if total_jobs > 0:
            pct = int((passed_count / total_jobs) * 100)
            self.stat_pass_rate_val.setText(f"{pct}% ({passed_count}/{total_jobs})")
        else:
            self.stat_pass_rate_val.setText("100% (Ready)")

        # Clear existing recent items
        while self.recent_items_container.count():
            item = self.recent_items_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        entries = get_history(limit=5)
        if not entries:
            empty_frame = QFrame()
            empty_frame.setObjectName("empty_state_frame")
            empty_layout = QVBoxLayout(empty_frame)
            empty_layout.setContentsMargins(24, 28, 24, 28)
            empty_layout.setSpacing(10)
            empty_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            empty_icon = QLabel("📄")
            empty_icon.setStyleSheet("font-size: 32px;")
            empty_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

            empty_title = QLabel("No Tailored Resumes Yet")
            empty_title.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
            empty_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

            empty_desc = QLabel(
                "Paste your first job description to tailor an ATS-compliant resume, "
                "generate a cold recruiter email, and check your role fit."
            )
            empty_desc.setStyleSheet("color: #8b90a0; font-size: 12px;")
            empty_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)

            start_btn = QPushButton("✦  Tailor Your First Resume")
            start_btn.setFixedWidth(240)
            start_btn.clicked.connect(lambda: self.navigate_requested.emit("new_job"))

            empty_layout.addWidget(empty_icon)
            empty_layout.addWidget(empty_title)
            empty_layout.addWidget(empty_desc)
            empty_layout.addWidget(start_btn, alignment=Qt.AlignmentFlag.AlignCenter)

            self.recent_items_container.addWidget(empty_frame)
            return

        for entry in entries:
            row_frame = self._build_recent_row(entry)
            self.recent_items_container.addWidget(row_frame)

    def _build_recent_row(self, entry: dict[str, Any]) -> QFrame:
        row = QFrame()
        row.setObjectName("recent_job_row")
        layout = QHBoxLayout(row)
        layout.setContentsMargins(18, 12, 18, 12)
        layout.setSpacing(16)

        # Role and company
        title_col = QVBoxLayout()
        title_col.setSpacing(2)

        role_name = entry.get("job_title") or "Software / Tech Role"
        role_lbl = QLabel(role_name)
        role_lbl.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        role_lbl.setStyleSheet("color: #ffffff;")

        comp_name = entry.get("company") or "Target Company"
        comp_lbl = QLabel(comp_name)
        comp_lbl.setStyleSheet("color: #8b90a0; font-size: 12px;")

        title_col.addWidget(role_lbl)
        title_col.addWidget(comp_lbl)
        layout.addLayout(title_col, stretch=2)

        # Verdict Badge
        verdict = entry.get("verdict") or "VERDICT"
        verdict_badge = QLabel(verdict)
        verdict_badge.setObjectName("badge_verdict")
        if "STRONGLY_APPLY" in verdict or "APPLY" in verdict:
            verdict_badge.setStyleSheet(
                "background-color: #064e3b; color: #34d399; padding: 4px 10px; border-radius: 6px; font-weight: 600; font-size: 11px;"
            )
        elif "CAUTION" in verdict:
            verdict_badge.setStyleSheet(
                "background-color: #78350f; color: #fbbf24; padding: 4px 10px; border-radius: 6px; font-weight: 600; font-size: 11px;"
            )
        else:
            verdict_badge.setStyleSheet(
                "background-color: #1e2235; color: #94a3b8; padding: 4px 10px; border-radius: 6px; font-weight: 600; font-size: 11px;"
            )
        layout.addWidget(verdict_badge)

        # ATS Status
        passed = entry.get("validation_passed", 0)
        ats_lbl = QLabel("✓ ATS Passed" if passed else "⚠ Warning")
        ats_lbl.setStyleSheet("color: #10b981; font-size: 11px;" if passed else "color: #f59e0b; font-size: 11px;")
        layout.addWidget(ats_lbl)

        # Date snippet
        ts = entry.get("timestamp", "")
        clean_ts = ts.split("T")[0] if "T" in ts else ts[:10]
        date_lbl = QLabel(clean_ts)
        date_lbl.setStyleSheet("color: #64748b; font-size: 11px;")
        layout.addWidget(date_lbl)

        # Action: Open Output Folder / PDF
        output_dir = entry.get("output_dir", "")
        if output_dir and Path(output_dir).exists():
            open_btn = QPushButton("📁  Open Folder")
            open_btn.setObjectName("secondary")
            open_btn.setFixedHeight(30)
            open_btn.clicked.connect(lambda checked=False, d=output_dir: self._open_path(d))
            layout.addWidget(open_btn)

        view_btn = QPushButton("View Details →")
        view_btn.setObjectName("secondary")
        view_btn.setFixedHeight(30)
        view_btn.clicked.connect(lambda: self.navigate_requested.emit("history"))
        layout.addWidget(view_btn)

        return row

    def _open_path(self, path_str: str) -> None:
        p = Path(path_str)
        if not p.exists():
            return
        if sys.platform == "win32":
            os.startfile(str(p))
        elif sys.platform == "darwin":
            subprocess.run(["open", str(p)], check=False)
        else:
            subprocess.run(["xdg-open", str(p)], check=False)
