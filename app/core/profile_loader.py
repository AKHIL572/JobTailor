"""
Loads and parses the Master Profile markdown file.
Filters out Project 1 and tags the internship project.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from app.core.data_dirs import data_path

logger = logging.getLogger(__name__)


@dataclass
class ParsedProfile:
    """Structured representation of the master profile."""
    raw_text: str = ""
    education: str = ""
    skills: str = ""
    experience: str = ""           # Full experience section
    projects: list[str] = field(default_factory=list)    # projects 2..N (project 1 excluded)
    leadership: str = ""
    certifications: str = ""
    contact: dict = field(default_factory=dict)
    project1_excluded: bool = False
    internship_project_tagged: bool = False
    # The internship project text (if found), tagged for experience-only use
    internship_project_text: str = ""
    # Parse warnings
    warnings: list[str] = field(default_factory=list)


def load_profile() -> str:
    """Return raw master profile text."""
    path = data_path("profile", "master_profile.md")
    if path.exists() and path.stat().st_size > 0:
        return path.read_text(encoding="utf-8")
    
    # Fallback to workspace root master_profile.md
    root_profile = Path(__file__).parent.parent.parent / "master_profile.md"
    if root_profile.exists():
        text = root_profile.read_text(encoding="utf-8")
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        except Exception:
            pass
        return text
    return ""


def load_contact() -> dict:
    """Return contact JSON dict."""
    path = data_path("profile", "contact.json")
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if data and any(data.values()):
                return data
        except Exception:
            pass

    # Extract defaults from master_profile.md
    raw = load_profile()
    name = "AKHIL T V"
    email = ""
    phone = ""
    linkedin = ""
    github = ""
    website = ""
    for line in raw.splitlines()[:50]:
        clean = line.strip()
        if re.search(r"\*\*Name\*\*:\s*", clean, re.IGNORECASE):
            name = re.split(r":\s*", clean, maxsplit=1)[1].strip()
        elif re.search(r"\*\*Email\*\*:\s*", clean, re.IGNORECASE):
            email = re.split(r":\s*", clean, maxsplit=1)[1].strip()
        elif re.search(r"\*\*Phone\*\*:\s*", clean, re.IGNORECASE):
            phone = re.split(r":\s*", clean, maxsplit=1)[1].strip()
        elif re.search(r"\*\*LinkedIn\*\*:\s*", clean, re.IGNORECASE):
            linkedin = re.split(r":\s*", clean, maxsplit=1)[1].strip()
        elif re.search(r"\*\*GitHub\*\*:\s*", clean, re.IGNORECASE):
            github = re.split(r":\s*", clean, maxsplit=1)[1].strip()
        elif "Portfolio" in clean and ("http://" in clean or "https://" in clean):
            urls = re.findall(r"https?://[^\s)]+", clean)
            if urls and not website:
                website = urls[0]

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "linkedin": linkedin,
        "github": github,
        "website": website,
    }


def get_profile_summary() -> dict[str, str]:
    """Return structured profile summary for the dashboard."""
    contact = load_contact()
    raw = load_profile()

    name = contact.get("name") or "AKHIL T V"
    email = contact.get("email") or ""
    phone = contact.get("phone") or ""
    linkedin = contact.get("linkedin") or ""
    github = contact.get("github") or ""
    website = contact.get("website") or ""

    degree = ""
    m_deg = re.search(r"\*\*Degree\*\*:\s*([^\n\r]+)", raw)
    if m_deg:
        degree = m_deg.group(1).strip()

    institution = ""
    m_inst = re.search(r"\*\*Institution\*\*:\s*([^\n\r]+)", raw)
    if m_inst:
        institution = m_inst.group(1).strip()

    experience_role = ""
    m_role = re.search(r"\*\*Role\*\*:\s*([^\n\r]+)", raw)
    if m_role:
        experience_role = m_role.group(1).strip()

    company = ""
    m_comp = re.search(r"\*\*Company\*\*:\s*([^\n\r]+)", raw)
    if m_comp:
        company = m_comp.group(1).strip()

    headline_parts = []
    if experience_role:
        headline_parts.append(f"{experience_role} at {company}" if company else experience_role)
    if degree:
        headline_parts.append(degree)

    headline = " · ".join(headline_parts) if headline_parts else "Software & Data Engineer"

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "linkedin": linkedin,
        "github": github,
        "website": website,
        "degree": degree,
        "institution": institution,
        "role": experience_role,
        "company": company,
        "headline": headline,
    }


def save_contact(data: dict) -> None:
    """Persist contact info."""
    path = data_path("profile", "contact.json")
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def save_profile(text: str) -> None:
    """Persist master profile text."""
    path = data_path("profile", "master_profile.md")
    path.write_text(text, encoding="utf-8")


def parse_profile(
    raw: str,
    project1_identifier: str = "Project 1",
    internship_identifier: str = "Project 6",
) -> ParsedProfile:
    """
    Parse the master profile markdown into sections.
    - Excludes Project 1 from the projects list.
    - Tags the internship project for experience-only use.
    """
    parsed = ParsedProfile(raw_text=raw)

    # Extract contact
    parsed.contact = load_contact()

    # ── Section extraction ──────────────────────────────────────────────
    # We split on markdown H1/H2/H3 headings
    sections: dict[str, str] = {}
    current_key = ""
    current_lines: list[str] = []

    for line in raw.splitlines(keepends=True):
        # Match H1 or H2
        heading = re.match(r"^(#{1,2})\s+(.+)", line)
        if heading:
            level = len(heading.group(1))
            title = heading.group(2).strip()
            # If we're inside a major section like Leadership and encounter an H2, keep it as part of leadership
            if level == 2 and current_key and any(k in current_key.lower() for k in ["leadership", "activities"]):
                current_lines.append(line)
                continue
            if current_key:
                sections[current_key.lower()] = "".join(current_lines).strip()
            current_key = title
            current_lines = []
        else:
            current_lines.append(line)
    if current_key:
        sections[current_key.lower()] = "".join(current_lines).strip()

    # Map common heading variants
    def _find(keys: list[str]) -> str:
        for k in keys:
            for sk, sv in sections.items():
                if k.lower() in sk:
                    return sv
        return ""

    parsed.education = _find(["education", "academic"])
    parsed.skills = _find(["skill", "technical skill", "technologies"])
    parsed.experience = _find(["experience", "work experience", "internship"])
    parsed.leadership = _find(["leadership", "activities", "extracurricular"])
    parsed.certifications = _find(["certification", "certificate", "license"])

    # ── Project extraction ──────────────────────────────────────────────
    # Locate project blocks: each project starts with `# Project <N>` or `## Project <N>`
    project_matches = list(re.finditer(r"(?m)^#{1,2}\s+(Project\s+\d+.*?)\s*$", raw))
    
    all_projects: list[tuple[str, str]] = []
    if project_matches:
        for idx, m in enumerate(project_matches):
            p_name = m.group(1).strip()
            p_start = m.end()
            p_end = project_matches[idx + 1].start() if idx + 1 < len(project_matches) else len(raw)
            p_body = raw[p_start:p_end].strip()
            all_projects.append((p_name, p_body))
    else:
        # Fallback if no "Project <N>" headings are found
        for heading_key, body in sections.items():
            if "project" in heading_key:
                all_projects.append((heading_key, body))

    # Filter and tag
    filtered: list[str] = []
    for name, body in all_projects:
        label = name.strip()
        p1 = project1_identifier.lower()
        intern_id = internship_identifier.lower()

        # Use word boundaries so "Project 1" does not match "Project 10..15"
        p1_pattern = rf"\b{re.escape(p1)}\b"
        intern_pattern = rf"\b{re.escape(intern_id)}\b"

        if re.search(p1_pattern, label, re.IGNORECASE):
            parsed.project1_excluded = True
            logger.debug("Excluded Project 1: %s", label)
            continue

        if re.search(intern_pattern, label, re.IGNORECASE):
            parsed.internship_project_tagged = True
            parsed.internship_project_text = f"## {label}\n\n{body}"
            logger.debug("Tagged internship project: %s", label)
            continue

        filtered.append(f"## {label}\n\n{body}")

    parsed.projects = filtered

    if not parsed.experience and parsed.internship_project_text:
        # Internship project appended to experience
        parsed.experience = (parsed.experience + "\n\n" + parsed.internship_project_text).strip()

    return parsed


def _split_projects(section_heading: str, body: str) -> list[tuple[str, str]]:
    """
    Attempt to split a projects section body into individual projects.
    Returns list of (name, body) tuples.
    """
    # Try sub-headings (### or #### Project Name)
    sub_pattern = re.compile(r"^#{2,4}\s+(.+)", re.MULTILINE)
    parts = sub_pattern.split(body)

    if len(parts) > 1:
        results = []
        for i in range(1, len(parts), 2):
            name = parts[i].strip()
            content = parts[i + 1].strip() if i + 1 < len(parts) else ""
            results.append((name, content))
        return results

    # If no sub-headings, treat the whole section as one project named by the heading
    heading_words = section_heading.replace("projects", "").strip()
    return [(section_heading if heading_words else "Project", body)]


def filter_profile_for_llm(
    parsed: ParsedProfile,
    include_internship_in_experience: bool = True,
) -> str:
    """
    Build the profile text to send to the LLM.
    - Project 1 is never included.
    - Internship project is in experience section only, not in projects.
    """
    parts: list[str] = []

    if parsed.education:
        parts.append(f"## Education\n\n{parsed.education}")

    if parsed.skills:
        parts.append(f"## Skills\n\n{parsed.skills}")

    if parsed.experience:
        exp = parsed.experience
        parts.append(f"## Experience\n\n{exp}")

    if parsed.projects:
        projects_block = "\n\n".join(parsed.projects)
        parts.append(f"## Projects\n\n{projects_block}")

    if parsed.leadership:
        parts.append(f"## Leadership\n\n{parsed.leadership}")

    if parsed.certifications:
        parts.append(f"## Certifications\n\n{parsed.certifications}")

    return "\n\n---\n\n".join(parts)
