# JobTailor — AI Resume & Career Application Suite

<p align="center">
  <img src="assets/icon.png" alt="JobTailor Logo" width="100"/>
</p>

<p align="center">
  <b>An end-to-end AI-powered desktop application built with Python and PySide6 that analyzes job descriptions, flags scam risks, evaluates candidate fit, drafts targeted outreach emails, and compiles pixel-perfect, single-page, ATS-optimized LaTeX resumes.</b>
</p>

---

## Overview

**JobTailor** is a local-first career automation suite designed for candidates targeting competitive software engineering, data science, QA, and analyst roles. It eliminates the guesswork and tedious manual formatting of applying to jobs by combining deep LLM analysis with automated LaTeX typesetting and strict layout validation.

Whether you run open-source models completely offline via **Ollama** or high-throughput cloud models via **Groq**, **OpenRouter**, or **Together AI**, JobTailor keeps your data private, safe, and stored locally on your machine.

---

## Key Features

### 1. Modern Desktop Experience
- **Interactive Dashboard**: Quick view of candidate profile summary, application statistics (total processed, apply vs. skip verdicts), quick action launchpads, and recent application history.
- **Top Navigation Bar**: Streamlined navigation with candidate profile chip, quick view switchers, and settings drawer.
- **Adaptive Dark & Light Themes**: Fully styled with custom Qt stylesheets, modern typography, crisp cards, and color-coded status badges.

### 2. Autonomous 7-Phase Application Pipeline
When you paste a job description into **New Job**, JobTailor runs a sequential multi-stage pipeline:
1. **Job Analysis**: Extracts target role, company name, compensation, tech stack, and separates requirements into *Must-Have* vs *Preferred*.
2. **Genuineness Check**: Evaluates job credibility, scanning for red flags such as unrealistic compensation, WhatsApp/Telegram-only interviews, free public email domains (`@gmail.com`), or upfront payment requests.
3. **Evidence-Based Verdict**: Scores role alignment against your catalog of master projects. If the role is flagged `DON'T APPLY` or `STRONGLY DON'T APPLY`, the pipeline safely terminates early to save time and compute.
4. **Outreach & Cold Email**: Detects hiring contact emails and application portals, drafting a concise, persuasive cold outreach email tailored to the recruiter or hiring manager.
5. **Resume Tailoring**: Selects and highlights 2–3 relevant projects, customizes 4–5 categorized skill groups, frames 4 targeted experience bullets, and writes an impactful professional summary.
6. **LaTeX Compilation & Page Fit Validation**: Compiles the LaTeX template via **Tectonic** (or pdflatex) and rigorously checks for single-page constraint, strict single-line bullets, and 85–100% horizontal line fill.
7. **Automated LLM Fixer Loop**: If any bullet wraps onto a second line or exceeds visual space thresholds, the fixer loop calculates the exact overflow character delta and re-prompts the LLM to tighten wording while preserving metrics.

### 3. Comprehensive Application History
- Stored locally in a dedicated SQLite database (`history.db`).
- Search, filter by verdict (`APPLY`, `CAUTION`, `SKIP`), and inspect previous applications.
- One-click export for generated `.pdf`, `.tex`, and full analysis `.json` records.

### 4. Customizable Profile, Rules & Templates
- **Master Profile Tab**: Edit your candidate profile in markdown with real-time parse checks.
- **Rules Tab**: Fine-tune any of the 7 system prompts independently with per-rule "Reset to Default" backups.
- **Template Tab**: Live-edit the LaTeX resume template and inspect placeholder tags.

### 5. Enterprise-Grade Security
- API keys (Groq, Together AI, OpenRouter) are never stored in plaintext config files—they are encrypted using your operating system's native credential store via the `keyring` library.

---

## Project Architecture

```
Resume Tailor/
├── app/
│   ├── main.py                  # Application entry point & Qt initialization
│   ├── core/
│   │   ├── apply_finder.py      # Contact & application link extraction
│   │   ├── config.py            # Settings persistence & model defaults
│   │   ├── data_dirs.py         # LocalAppData directory management & seeding
│   │   ├── email_writer.py      # Tailored recruiter outreach generator
│   │   ├── fixer.py             # Line-overflow fixer loop
│   │   ├── genuineness.py       # Job scam & authenticity checker
│   │   ├── history.py           # SQLite history storage & analytics
│   │   ├── job_analyzer.py      # JD parsing and requirement segmentation
│   │   ├── latex_utils.py       # LaTeX escaping, template filling, Tectonic compilation
│   │   ├── llm_client.py        # Unified OpenAI-compatible LLM client (Ollama/Groq/etc.)
│   │   ├── logging_setup.py     # File & console logging setup
│   │   ├── pipeline.py          # Orchestrates the 7-step pipeline & Qt signals
│   │   ├── profile_loader.py    # Markdown profile parser & validator
│   │   ├── resume_builder.py    # Resume section generation
│   │   ├── rules_loader.py      # System prompts loader
│   │   ├── validator.py         # PDF page count, bullet wrap, and line fill validator
│   │   └── verdict.py           # Match evaluation & apply/skip decision logic
│   ├── models/
│   │   └── schemas.py           # Pydantic models for structured outputs
│   └── ui/
│       ├── main_window.py       # Main application window & top navigation
│       ├── theme.py             # Custom Dark & Light Qt style definitions
│       ├── pages/               # Individual view controllers (Dashboard, New Job, History, Profile, etc.)
│       └── widgets/             # Reusable UI components (TopBar, PDFViewer)
├── assets/                      # Application icons & visual assets
├── bin/                         # Bundled Tectonic binary for Windows
├── build/                       # PyInstaller packaging configuration
├── prompts/                     # Default modular prompt instructions (01 through 07)
├── templates/                   # Default LaTeX resume template
├── tests/                       # Comprehensive pytest suite
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

---

## Quick Start

### 1. Prerequisites
- **Python 3.11+** installed on your system.
- **LaTeX Compiler**:
  - The bundled lightweight `bin/tectonic.exe` is used automatically on Windows.
  - Alternatively, install system-wide [Tectonic](https://tectonic-typesetting.github.io/) (`winget install tectonic`) or [MiKTeX](https://miktex.org/).
- **LLM Provider**:
  - **Local Ollama** (recommended for full privacy): [Download Ollama](https://ollama.com/) and run:
    ```bash
    ollama run llama3:latest
    # or for larger parameter models:
    ollama run llama3.3:70b
    ```
  - **Cloud APIs**: Groq, OpenRouter, or Together AI (configure in Settings).

---

### 2. Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/AKHIL572/Resume_Tailor.git
   cd Resume_Tailor
   ```

2. **Create and activate a virtual environment**:
   ```powershell
   # Windows PowerShell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
   *(If script execution is disabled in PowerShell, run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

3. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

---

### 3. Launching the App

Start the application with:
```powershell
python -m app.main
```

On initial launch, JobTailor automatically seeds your local profile, templates, and rules into:
`%LOCALAPPDATA%\JobTailor\JobTailor\`

---

## Running the Test Suite

Run the full automated test suite with:
```powershell
python -m pytest
```

Tests cover:
- LLM response parsing and schema validation
- LaTeX special character escaping and placeholder substitution
- Candidate profile parsing and project count constraints
- Line-fill calculations, bullet point length, and single-page constraints
- Settings migration and client retry logic

---

## Building a Standalone Windows Executable

To compile JobTailor into a standalone Windows `.exe` with the bundled icon:

```powershell
pip install pyinstaller
pyinstaller build/pyinstaller.spec
```

The compiled binary will be placed in `dist/JobTailor.exe`.

---

## Configuration & Layout Tuning

Layout behavior is managed via `%LOCALAPPDATA%\JobTailor\JobTailor\config\layout_config.json`:

```json
{
  "page_count": 1,
  "summary_lines": [3, 4],
  "experience_bullets": 4,
  "skills_categories_default": 4,
  "skills_categories_when_two_projects_or_qa_role": 5,
  "projects_default": 3,
  "bullets_per_project": {
    "2_projects": 4,
    "3_projects": 3
  },
  "leadership_max_positions": 2,
  "leadership_bullets_per_position": 1,
  "certifications": [1, 2],
  "line_fill_min": 0.85,
  "line_fill_max": 1.00,
  "max_fix_rounds": 5,
  "unused_space_threshold_mm": 15.0
}
```

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
