# Automated Resume & Skill Gap Analyzer

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-all--MiniLM--L6--v2-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
[![Code style: ruff](https://img.shields.io/badge/Code%20Style-Ruff-000000.svg?style=for-the-badge&logo=ruff)](https://github.com/astral-sh/ruff)

**A high-performance, context-aware NLP screening engine combining Sentence-BERT dense semantic representations with a domain-specific technical skill taxonomy for intelligent candidate matching and gap remediation.**

[Quick Start](#-quick-start) •
[Architecture](#-system-architecture) •
[Mathematical Formulation](#-mathematical-formulation) •
[Tech Stack](#-technology-stack) •
[Viva & Interview Defense](#-viva-defense--interview-cheat-sheet) •
[Contributing](#-contributing)

</div>

---

## 📌 Executive Summary

Traditional **Applicant Tracking Systems (ATS)** rely on rigid, exact-string frequency heuristics. This creates two critical failure modes in modern talent acquisition:
1. **Vocabulary Mismatch (High False Negatives):** Highly qualified applicants describing achievements with synonyms (e.g., *"Deep Residual Networks"* vs. *"PyTorch DL Models"*) are discarded.
2. **Keyword Stuffing (High False Positives):** Unscrupulous candidates game systems by hiding keyword lists in white text without real project context.

The **Automated Resume & Skill Gap Analyzer** solves this through a dual-engine **Hybrid Composite Compatibility Architecture**:
- **Dense Contextual Embeddings (60% weight):** Utilizes `all-MiniLM-L6-v2` Sentence-Transformers to compute semantic cosine alignment across high-dimensional latent space.
- **Rule-Based Skill Taxonomy (40% weight):** Employs regex word-boundary guards and synonym canonicalization to detect essential technology prerequisites without substring collisions.
- **Actionable Gap Remediation:** Identifies missing competencies and recommends targeted learning roadmaps to bridge the technical divide.

---

## 🏗️ System Architecture

```
+------------------------+      +-------------------------------+
|  Candidate Resume      |      | Target Job Description (JD)   |
|  (.pdf, .docx, .txt)   |      | (Plaintext / Pasted text)     |
+-----------+------------+      +---------------+---------------+
            |                                   |
            v                                   v
+------------------------+                      |
| Multi-Format Parser    |                      |
| (pypdf, python-docx)   |                      |
| - Non-ASCII cleaning   |                      |
| - Whitespace normalize |                      |
+-----------+------------+                      |
            |                                   |
            +-----------------+-----------------+
                              |
                              v
             +---------------------------------+
             |           NLP Engine            |
             +----------------+----------------+
                              |
       +----------------------+----------------------+
       |                                             |
       v                                             v
+-----------------------------+       +-----------------------------+
| Dense Semantic Embeddings   |       | Rule-Based Skill Taxonomy   |
| - 'all-MiniLM-L6-v2' (384d) |       | - Regex Word-Boundary Match |
| - Cosine Similarity Calc    |       | - Alias Normalization       |
| - Score S in [0.0, 1.0]     |       | - Overlap Ratio O = |M|/|J| |
+--------------+--------------+       +--------------+--------------+
               |                                     |
               +------------------+------------------+
                                  |
                                  v
             +-----------------------------------------+
             |    Weighted Composite Scorer            |
             |  Score = (0.60 * S) + (0.40 * O)        |
             +--------------------+--------------------+
                                  |
            +---------------------+---------------------+
            |                                           |
            v                                           v
+-----------------------------+             +-----------------------+
|  Local SQLite Persistence   |             | Streamlit UI Dash     |
|  (evaluations.sqlite)       |             | - Metric KPI Cards    |
|  - Timestamped history      |             | - Matched/Missing Tags|
|  - JSON skill serialization |             | - Bridge-the-gap Tips |
|  - CSV export engine        |             | - 1-Click Viva Demo   |
+-----------------------------+             +-----------------------+
```

```mermaid
flowchart TD
    subgraph Ingestion ["1. Document Ingestion"]
        A[Candidate Resume\n.pdf, .docx, .txt] --> C[Document Parser\npypdf & python-docx]
        B[Job Description\nText Input] --> D[Sanitization Pipeline\nASCII Normalization & Regex]
        C --> D
    end

    subgraph DualNLP ["2. Dual NLP Scoring Engine"]
        D --> E[Contextual Dense Embeddings\nall-MiniLM-L6-v2 384d]
        D --> F[Skill Taxonomy Matcher\nWord-Boundary Regex + Canonical Aliases]
        E --> G[Cosine Similarity S\n0.0 - 1.0]
        F --> H[Skill Overlap Ratio O\n|Matched| / |Required|]
    end

    subgraph Evaluation ["3. Scoring & Remediation"]
        G --> I[Composite Scorer\nScore = 0.60*S + 0.40*O]
        H --> I
        F --> J[Skill Gap Engine\nMissing & Extra Skills]
    end

    subgraph Presentation ["4. Storage & UI"]
        I --> K[Streamlit Analytics Dashboard]
        J --> K
        I --> L[(SQLite Persistence\nevaluations.sqlite)]
        K --> M[CSV Export & Historical Audit]
    end
```

---

## ✨ Key Features

- 📄 **Universal Document Parser:** Seamlessly parses multi-page `.pdf`, `.docx`, and `.txt` files with automated Unicode sanitization, stripping unprintable control characters and typographical anomalies.
- 🧠 **Context-Aware Embeddings:** Generates 384-dimensional dense vectors using Hugging Face's `all-MiniLM-L6-v2` transformer model for contextual semantic understanding beyond surface keywords.
- 🎯 **Boundary-Guarded Skill Taxonomy:** Evaluates 50+ core technologies across 7 domains (ML/AI, Cloud, Frontend, Backend, Databases, DevOps, Languages) using strict word-boundary guards `(?<!\w)alias(?!\w)` to eliminate false positives on short acronyms (`R`, `C`, `k8s`).
- 📊 **Metric KPI Dashboard:** Real-time visual cards for Composite Match %, Semantic Similarity %, Technical Skill Overlap %, and qualitative readiness classifications (High, Moderate, Low).
- 💡 **Actionable Gap Remediation:** Categorizes technical skills into **Matched**, **Missing**, and **Differentiating/Extra**, generating contextual recommendations to bridge skill gaps.
- 💾 **Zero-Config SQLite Persistence:** Automatically persists candidate evaluations locally with full JSON skill serialization, searchable historical audits, and 1-click CSV exports.
- 🧪 **1-Click Viva Defense Demo:** Includes pre-packaged sample resumes and job descriptions for immediate, reproducible testing and examiner demonstrations.

---

## 📐 Mathematical Formulation

### 1. Dense Semantic Cosine Similarity
Let $\mathbf{u} \in \mathbb{R}^{384}$ represent the sentence embedding vector of the Candidate Resume, and $\mathbf{v} \in \mathbb{R}^{384}$ represent the sentence embedding of the Target Job Description:

$$\text{Semantic Similarity } (S) = \cos(\theta) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\|_2 \|\mathbf{v}\|_2} = \frac{\sum_{i=1}^{384} u_i v_i}{\sqrt{\sum_{i=1}^{384} u_i^2} \sqrt{\sum_{i=1}^{384} v_i^2}}$$

Since embeddings produced by Sentence-Transformers are $L_2$-normalized ($\|\mathbf{u}\|_2 = 1$), this reduces directly to the inner product:
$$S = \mathbf{u} \cdot \mathbf{v}, \quad S \in [-1.0, 1.0] \xrightarrow{\text{clipped}} [0.0, 1.0]$$

### 2. Set-Theoretic Skill Overlap Ratio
Let $R$ denote the set of canonical skills extracted from the resume and $J$ denote the required skills extracted from the Job Description:
- **Matched Skills ($M$):** $M = R \cap J$
- **Missing Skills ($G$):** $G = J \setminus R$
- **Extra Skills ($E$):** $E = R \setminus J$

The **Skill Overlap Ratio ($O$)** is formulated as:
$$O = \begin{cases} \frac{|R \cap J|}{|J|}, & \text{if } |J| > 0 \\ 1.0, & \text{if } |J| = 0 \text{ and } |R| > 0 \\ 0.0, & \text{otherwise} \end{cases}$$

### 3. Weighted Composite Compatibility Metric
$$\text{Composite Score} = (0.60 \times S) + (0.40 \times O)$$

The $60/40$ weighting balances holistic domain context against non-negotiable hard tool proficiencies, preventing both keyword gaming and vocabulary-mismatch rejections.

---

## 💻 Technology Stack

| Layer | Technology | Specification / Version | Architectural Justification |
| :--- | :--- | :--- | :--- |
| **Frontend UI** | Streamlit | `>=1.30.0` | Reactive Python dashboard framework with native session state and cached model inference. |
| **NLP Transformer** | Sentence-Transformers | `>=2.2.2` | Siamese BERT networks fine-tuned specifically for semantic textual similarity (STS). |
| **Pretrained Weights** | `all-MiniLM-L6-v2` | PyTorch | 22.7M parameters; sub-50ms inference on CPU; 5x faster than BERT-base with 95% semantic parity. |
| **Vector Math** | Scikit-Learn | `>=1.3.0` | High-performance vectorized cosine distance computations. |
| **Document Parsing** | PyPDF & python-docx | `>=3.17.0` | In-memory binary document parsing without external system dependencies (no Poppler required). |
| **Persistence** | SQLite3 | Native Standard Library | ACID-compliant, zero-configuration local database for self-contained audit histories. |
| **Tabular Data** | Pandas | `>=2.0.0` | Dataframe transformation and streaming CSV data export. |

---

## 📂 Repository Structure

```
automated-resume-skill-gap-analyzer/
├── .github/
│   ├── workflows/
│   │   └── ci.yml                     # Multi-OS GitHub Actions CI pipeline
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md              # Structured bug report template
│   │   └── feature_request.md         # Enhancement proposal template
│   └── pull_request_template.md       # Standardized PR checklist
├── resume_analyzer/
│   ├── app.py                         # Streamlit application entry point & UI
│   ├── core/
│   │   ├── __init__.py                # Package initialization
│   │   ├── parser.py                  # Multi-format document parser & sanitizer
│   │   ├── nlp_engine.py              # Sentence-BERT embeddings & skill taxonomy
│   │   └── database.py                # SQLite persistence & audit query engine
│   ├── sample_data/
│   │   ├── sample_ml_resume.pdf       # Valid sample candidate resume
│   │   ├── sample_ml_jd.txt           # Realistic target job description
│   │   └── generate_sample_pdf.py     # Programmatic sample generator (ReportLab)
│   └── tests/
│       └── test_integration.py        # Automated test suite (5 passing suites)
├── .gitignore                         # Comprehensive git exclusions
├── CITATION.cff                       # Academic citation metadata
├── CODE_OF_CONDUCT.md                 # Contributor Covenant Code of Conduct
├── CONTRIBUTING.md                    # Contribution workflow & guidelines
├── LICENSE                            # MIT Open Source License
├── Makefile                           # Development automation commands
├── pyproject.toml                     # Modern Python project configuration
├── requirements.txt                   # Production package dependencies
├── requirements-dev.txt               # Development & test dependencies
└── README.md                          # Repository documentation
```

---

## 🚀 Quick Start

### Prerequisites
- Python `3.10` or higher
- Git

### 1. Clone Repository
```bash
git clone https://github.com/your-username/automated-resume-skill-gap-analyzer.git
cd automated-resume-skill-gap-analyzer
```

### 2. Create and Activate Virtual Environment
```bash
# macOS / Linux:
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell):
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch Application
```bash
streamlit run resume_analyzer/app.py
```
Open your browser at `http://localhost:8501`.

---

## 🧪 Testing & Code Quality

The repository includes a test suite covering document parsing, text sanitization, skill taxonomy matching, embedding generation, and database CRUD transactions.

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Execute test suite
pytest resume_analyzer/tests -v

# Run code linter
ruff check .

# Auto-format code
ruff format .
```

---

## 🎓 Viva Defense & Interview Cheat Sheet

<details>
<summary><b>Q1: Why choose <code>all-MiniLM-L6-v2</code> over BERT-base or TF-IDF?</b></summary>
<br>

- **vs. TF-IDF:** TF-IDF relies purely on lexical overlap. It completely fails when a candidate writes *"deep neural networks"* and the JD requests *"PyTorch architectures"*. Sentence-Transformers map text into a dense 384-dimensional latent semantic space where related concepts are clustered closely.
- **vs. BERT-base:** Standard BERT-base has 110M parameters and requires quadratic $O(N^2)$ cross-encoder computation. `all-MiniLM-L6-v2` contains only 22.7M parameters, yields fixed-size pooled embeddings in $<50$ms on commodity CPUs, and achieves 95% of BERT's accuracy on Semantic Textual Similarity benchmarks.
</details>

<details>
<summary><b>Q2: Why does Hybrid Scoring outperform keyword-only ATS systems?</b></summary>
<br>

Pure keyword systems suffer from **keyword stuffing** and **vocabulary variation**. 
Our hybrid approach allocates **60% to Semantic Similarity** (validating that the candidate's actual narrative and achievements match the problem domain) and **40% to Skill Overlap** (verifying that non-negotiable tools like Docker, Kubernetes, or Python are present).
</details>

<details>
<summary><b>Q3: How does the Skill Taxonomy avoid false-positive substring collisions?</b></summary>
<br>

Naive substring checks fail on short acronyms (e.g., searching for `R` or `C` matches inside "training" or "cloud"; searching `ML` matches "HTML").
In `core/nlp_engine.py`, regular expressions enforce strict word boundary lookarounds `(?<!\w)alias(?!\w)` alongside canonical synonym dictionaries, ensuring that `k8s` normalizes to `Kubernetes` and `sklearn` normalizes to `Machine Learning` without erroneous triggers.
</details>

<details>
<summary><b>Q4: Why is SQLite used instead of a client-server database like PostgreSQL?</b></summary>
<br>

SQLite is serverless, zero-configuration, and fully ACID-compliant, packaging the database directly within `evaluations.sqlite`. This ensures the application is completely portable, requiring zero container setups or external network daemons for examiner evaluation.
</details>

---

## 🗺️ Roadmap

- [ ] Add OCR support for scanned image-based PDF resumes (Tesseract / EasyOCR).
- [ ] Implement section-level parsing (Work Experience, Education, Projects, Certifications).
- [ ] Add automated PDF summary report export with visual radar charts.
- [ ] Integrate local quantized LLM inference (e.g., Llama 3 via Ollama) for personalized cover letter generation.

---

## 🤝 Contributing

Contributions are welcomed! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on branching, testing standards, and submitting pull requests.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 📚 Citation

If you utilize this project in your academic coursework or research, please cite it using:

```bibtex
@software{AutomatedResumeAnalyzer2026,
  author = {Vivek},
  title = {Automated Resume & Skill Gap Analyzer: Context-Aware Semantic Candidate Matching and Skill Taxonomy System},
  year = {2026},
  url = {https://github.com/vivek/automated-resume-skill-gap-analyzer}
}
```
