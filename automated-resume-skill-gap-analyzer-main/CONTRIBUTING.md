# Contributing to Automated Resume & Skill Gap Analyzer

Thank you for your interest in contributing! We welcome contributions to enhance features, improve performance, extend the skill taxonomy, and polish the documentation.

---

## Code of Conduct

Please review and adhere to our [Code of Conduct](CODE_OF_CONDUCT.md) in all community and repository interactions.

---

## How Can You Contribute?

1. **Reporting Bugs:** Submit an issue using our [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.md).
2. **Suggesting Enhancements:** Propose improvements or new features using our [Feature Request Template](.github/ISSUE_TEMPLATE/feature_request.md).
3. **Extending Skill Taxonomy:** Add new domain skills, modern tech stacks, or synonyms in `resume_analyzer/core/nlp_engine.py`.
4. **Writing Tests:** Increase test coverage across edge-case documents (complex PDF layouts, scanned text, OCR).
5. **UI & Visualization:** Enhance Streamlit widgets, charts, and downloadable reports.

---

## Development Workflow

### 1. Fork & Clone
```bash
git clone https://github.com/<your-username>/automated-resume-skill-gap-analyzer.git
cd automated-resume-skill-gap-analyzer
```

### 2. Set Up Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt -r requirements-dev.txt
```

### 4. Create a Feature Branch
```bash
git checkout -b feature/amazing-feature
# or: git checkout -b fix/issue-description
```

### 5. Run Quality Checks & Tests
Before committing, ensure your code conforms to linting standards and passes all tests:
```bash
# Run tests
pytest resume_analyzer/tests -v

# Run linter
ruff check .

# Auto-format
ruff format .
```

### 6. Commit & Push
Write clear, conventional commit messages:
```bash
git add .
git commit -m "feat(nlp): add cloud engineering skill taxonomy aliases"
git push origin feature/amazing-feature
```

### 7. Open a Pull Request
- Target the `main` branch.
- Complete the provided [Pull Request Template](.github/pull_request_template.md).
- Reference any related issues (e.g. `Closes #12`).

---

## Coding Standards

- **Python Version:** Compatible with Python 3.10, 3.11, and 3.12.
- **Type Annotations:** Use Python type hints where applicable.
- **Docstrings:** Document functions and modules explaining inputs, outputs, and edge cases.
- **Deterministic Logic:** For testing, ensure random seeds are handled and model downloads are cached.
