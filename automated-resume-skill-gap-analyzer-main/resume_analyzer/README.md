# Automated Resume & Skill Gap Analyzer
### MCA 3rd-Semester Minor Project | Department of Computer Applications

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Sentence-Transformers](https://img.shields.io/badge/NLP-all--MiniLM--L6--v2-orange.svg)](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
[![Database](https://img.shields.io/badge/Database-SQLite3-003B57.svg)](https://www.sqlite.org/)

---

## 1. Project Abstract

In contemporary recruitment processes, traditional **Applicant Tracking Systems (ATS)** rely excessively on exact keyword frequency matching, making them prone to false negatives (rejecting qualified candidates due to vocabulary variation) and susceptible to keyword stuffing.

The **Automated Resume & Skill Gap Analyzer** is an end-to-end, production-grade NLP platform designed to bridge this divide. Combining dense contextual semantic representations from Hugging Face's `all-MiniLM-L6-v2` Sentence-Transformer with a domain-specific technical skill taxonomy matching engine, the system computes a balanced **Composite Compatibility Score**. Furthermore, it executes set-theoretic skill gap identification to pinpoint missing technical proficiencies and generates personalized, actionable learning recommendations for candidates.

---

## 2. System Architecture & Dataflow

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
|  - Timestamped history      |             | - Matched/Missing Badges
|  - JSON skill serialization |             | - Bridge-the-gap Tips |
|  - CSV export engine        |             | - 1-Click Viva Demo   |
+-----------------------------+             +-----------------------+
```

---

## 3. Project Directory Structure

```
resume_analyzer/
├── app.py                      # Main Streamlit UI, session state, and orchestration
├── requirements.txt            # Pinned Python package dependencies
├── README.md                   # Academic documentation, architecture, and viva cheat sheet
├── core/
│   ├── __init__.py             # Module initialization
│   ├── parser.py               # Multi-format document parser (.pdf, .docx, .txt)
│   ├── nlp_engine.py           # Sentence-Transformer embeddings, cosine similarity, skill taxonomy
│   └── database.py             # SQLite connection, history logging, and CRUD utility
└── sample_data/
    ├── sample_ml_resume.pdf    # Programmatically generated valid PDF resume
    ├── sample_ml_jd.txt        # Sample Target Job Description text
    └── generate_sample_pdf.py  # ReportLab generation script for sample PDF
```

---

## 4. Technology Stack

| Layer | Technology | Version | Justification |
| :--- | :--- | :--- | :--- |
| **Frontend & UI** | Streamlit | `>=1.30.0` | Rapid, reactive Python web dashboard with native caching and state management. |
| **NLP Embeddings** | Sentence-Transformers | `>=2.2.2` | Implements Siamese BERT architectures for generating fixed 384-dimensional dense vectors. |
| **Pretrained Model**| `all-MiniLM-L6-v2` | PyTorch | Lightweight (22.7M parameters), ultra-fast inference (<50ms), 5x faster than BERT-base with 95% semantic parity. |
| **Vector Math** | Scikit-Learn | `>=1.3.0` | Vectorized cosine similarity computation across high-dimensional vector spaces. |
| **Document Parsing**| PyPDF & Python-Docx | `>=3.17.0` | Robust handling of multi-page PDFs and Word documents without external OS dependencies. |
| **Persistence** | SQLite3 | Native | Zero-configuration, serverless, ACID-compliant local database storing structured evaluation histories. |
| **Data Handling** | Pandas | `>=2.0.0` | Tabular data representation, filtering, and seamless CSV exporting. |

---

## 5. Mathematical & Algorithmic Formulation

### 5.1 Dense Semantic Cosine Similarity
Let $\mathbf{u} \in \mathbb{R}^{384}$ be the normalized sentence embedding of the Candidate Resume, and $\mathbf{v} \in \mathbb{R}^{384}$ be the sentence embedding of the Target Job Description:

$$\text{Semantic Similarity } (S) = \cos(\theta) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\|_2 \|\mathbf{v}\|_2} = \frac{\sum_{i=1}^{384} u_i v_i}{\sqrt{\sum_{i=1}^{384} u_i^2} \sqrt{\sum_{i=1}^{384} v_i^2}}$$

Because embeddings generated by Sentence-Transformers are unit-normalized ($L_2 = 1$), this reduces to the direct dot product:
$$S = \mathbf{u} \cdot \mathbf{v}$$

### 5.2 Set-Theoretic Skill Overlap Ratio
Let $R$ represent the set of technical skills extracted from the resume and $J$ represent the set of skills required by the Job Description:
- **Matched Skills ($M$):** $M = R \cap J$
- **Missing Skills ($G$):** $G = J \setminus R$
- **Extra Skills ($E$):** $E = R \setminus J$

The **Skill Overlap Ratio ($O$)** is given by:
$$O = \begin{cases} \frac{|R \cap J|}{|J|}, & \text{if } |J| > 0 \\ 1.0, & \text{if } |J| = 0 \text{ and } |R| > 0 \\ 0.0, & \text{otherwise} \end{cases}$$

### 5.3 Composite Compatibility Metric
$$\text{Composite Score} = (0.60 \times S) + (0.40 \times O)$$
The composite score weights contextual domain semantic alignment at 60% and exact technical requirements overlap at 40%, balancing holistic experience against hard tool prerequisites.

---

## 6. Installation & Execution Guide

### Step 1: Clone or Navigate to Directory
```bash
cd "resume_analyzer"
```

### Step 2: Create and Activate Virtual Environment
```bash
# macOS/Linux:
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell):
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Launch the Streamlit Web Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 7. Viva Defense & Examination Q&A Cheat Sheet

### Q1: Why use `all-MiniLM-L6-v2` instead of standard BERT-base or TF-IDF?
> **Answer:**
> - **vs. TF-IDF:** TF-IDF only tracks exact lexical term frequencies. It fails when a candidate writes *"deep neural networks"* and the job requires *"PyTorch DL architectures"*. Sentence-Transformers capture semantic meaning in high-dimensional embedding space.
> - **vs. BERT-base:** BERT-base has 110 million parameters and outputs token-level embeddings requiring expensive cross-encoder passes ($O(N^2)$). `all-MiniLM-L6-v2` has only 22.7 million parameters, produces a compact 384-dimensional vector, runs 5x faster on standard CPU hardware, and achieves 95% of BERT's performance on semantic textual similarity benchmarks.

### Q2: Why does Hybrid Scoring (Semantic + Keyword) outperform pure keyword ATS?
> **Answer:**
> Pure keyword ATS suffers from two fatal flaws:
> 1. **Keyword Stuffing Vulnerability:** Unscrupulous applicants paste white-colored text keywords to trick the system.
> 2. **Vocabulary Mismatch:** True experts who summarize their achievements without repeating buzzwords are falsely rejected.
> 
> Our hybrid model uses **Semantic Similarity (60%)** to verify that the overall project experience and accomplishments genuinely align with the role's domain, while **Skill Overlap (40%)** guarantees that non-negotiable stack competencies (e.g. Docker, Kubernetes, AWS) are present.

### Q3: How does the Skill Taxonomy avoid false positive substring matches?
> **Answer:**
> Simple substring searches fail on short acronyms (e.g., searching for `R` or `C` matches inside "training" or "cloud", `ML` matches "HTML"). 
> In `core/nlp_engine.py`, we implement regular expressions with strict word boundary guards `(?<!\w)alias(?!\w)` alongside canonical synonym dictionaries, ensuring that "sklearn" maps to "Machine Learning" and "k8s" maps to "Kubernetes" safely without false matches.

### Q4: Why is SQLite ideal for this architecture?
> **Answer:**
> SQLite is zero-configuration, serverless, and stores evaluations in a single self-contained file (`evaluations.sqlite`). It provides full ACID transaction guarantees without requiring a separate database daemon (like MySQL or PostgreSQL), making the application completely portable and immediately runnable on any examiner's machine.

### Q5: How are multi-page documents and formatting variations sanitized?
> **Answer:**
> `core/parser.py` parses each page sequentially, replaces non-standard Unicode typographical characters (curly quotes, long dashes, bullet points) with standard ASCII equivalents, strips unprintable control characters, and collapses redundant whitespace and carriage returns into clean normalized paragraphs.

---

## 8. Academic Project Metadata
- **Course:** Master of Computer Applications (MCA)
- **Semester:** 3rd Semester
- **Subject:** Minor Project / Software Engineering & Applied AI Lab
- **Implementation:** Python 3, PyTorch, Sentence-Transformers, Streamlit, SQLite3
