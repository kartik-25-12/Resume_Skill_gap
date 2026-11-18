"""
app.py
Streamlit Web Frontend for Automated Resume & Skill Gap Analyzer.
MCA 3rd-Semester Minor Project.
"""

import io
import os
import sys
import time

import streamlit as st

# Ensure local core module is importable regardless of launch directory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from core.database import clear_history, get_all_history, get_history_df, save_evaluation
from core.nlp_engine import analyze_resume_and_jd, load_embedding_model
from core.parser import extract_text

# ---------------------------------------------------------------------------
# Streamlit Page Configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Resume & Skill Gap Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------------------------
# Custom CSS for Modern, Academic & Professional UI
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .main-header {
        background: linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #4338CA 100%);
        padding: 24px 32px;
        border-radius: 16px;
        color: #FFFFFF;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(49, 46, 129, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .main-header h1 {
        margin: 0;
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #FFFFFF !important;
    }
    .main-header p {
        margin: 6px 0 0 0;
        font-size: 14px;
        color: #C7D2FE;
        font-weight: 400;
    }

    /* Metric Cards */
    .metric-card {
        background: #1E222D;
        border-radius: 12px;
        padding: 18px 20px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        text-align: center;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(99, 102, 241, 0.5);
    }
    .metric-title {
        font-size: 13px;
        font-weight: 600;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 6px;
    }
    .metric-value-primary {
        font-size: 34px;
        font-weight: 800;
        background: linear-gradient(135deg, #60A5FA, #A78BFA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 4px 0;
    }
    .metric-value-green {
        font-size: 34px;
        font-weight: 800;
        color: #34D399;
        margin: 4px 0;
    }
    .metric-value-blue {
        font-size: 34px;
        font-weight: 800;
        color: #38BDF8;
        margin: 4px 0;
    }
    .metric-subtitle {
        font-size: 12px;
        color: #64748B;
        font-weight: 500;
    }

    /* Skill Badges */
    .skill-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin: 10px 0 16px 0;
    }
    .badge-matched {
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 5px 12px;
        border-radius: 9999px;
        font-size: 12.5px;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }
    .badge-missing {
        background: rgba(244, 63, 94, 0.15);
        color: #FB7185;
        border: 1px solid rgba(244, 63, 94, 0.4);
        padding: 5px 12px;
        border-radius: 9999px;
        font-size: 12.5px;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }
    .badge-extra {
        background: rgba(148, 163, 184, 0.12);
        color: #CBD5E1;
        border: 1px solid rgba(148, 163, 184, 0.3);
        padding: 5px 12px;
        border-radius: 9999px;
        font-size: 12.5px;
        font-weight: 500;
        display: inline-flex;
        align-items: center;
    }

    /* Recommendation Card */
    .rec-card {
        background: rgba(30, 41, 59, 0.7);
        border-left: 4px solid #F43F5E;
        padding: 12px 16px;
        border-radius: 6px 10px 10px 6px;
        margin-bottom: 10px;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    .rec-card.high-priority {
        border-left-color: #F43F5E;
    }
    .rec-card.medium-priority {
        border-left-color: #F59E0B;
    }
    .rec-skill-name {
        font-weight: 700;
        font-size: 14px;
        color: #F8FAFC;
    }
    .rec-tag {
        font-size: 11px;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: 600;
        margin-left: 8px;
    }
    .rec-tag-high {
        background: rgba(244, 63, 94, 0.2);
        color: #FDA4AF;
    }
    .rec-tag-medium {
        background: rgba(245, 158, 11, 0.2);
        color: #FDE68A;
    }
    .rec-advice {
        font-size: 12.5px;
        color: #94A3B8;
        margin-top: 4px;
        line-height: 1.4;
    }

    /* Demo Quick Box */
    .demo-info-box {
        background: rgba(99, 102, 241, 0.12);
        border: 1px dashed rgba(99, 102, 241, 0.4);
        padding: 12px 16px;
        border-radius: 10px;
        font-size: 12.5px;
        color: #C7D2FE;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------------------------
if "candidate_name" not in st.session_state:
    st.session_state.candidate_name = ""
if "jd_text" not in st.session_state:
    st.session_state.jd_text = ""
if "sample_loaded" not in st.session_state:
    st.session_state.sample_loaded = False
if "eval_results" not in st.session_state:
    st.session_state.eval_results = None
if "uploaded_resume_bytes" not in st.session_state:
    st.session_state.uploaded_resume_bytes = None
if "uploaded_resume_name" not in st.session_state:
    st.session_state.uploaded_resume_name = ""

# Paths for sample data
SAMPLE_RESUME_PATH = os.path.join(CURRENT_DIR, "sample_data", "sample_ml_resume.pdf")
SAMPLE_JD_PATH = os.path.join(CURRENT_DIR, "sample_data", "sample_ml_jd.txt")


def load_demo_data():
    """Callback to load sample candidate resume and target JD into state."""
    st.session_state.candidate_name = "Alex Rivera (ML Engineer)"
    if os.path.exists(SAMPLE_JD_PATH):
        with open(SAMPLE_JD_PATH, "r", encoding="utf-8") as f:
            st.session_state.jd_text = f.read()

    if os.path.exists(SAMPLE_RESUME_PATH):
        with open(SAMPLE_RESUME_PATH, "rb") as f:
            st.session_state.uploaded_resume_bytes = f.read()
        st.session_state.uploaded_resume_name = "sample_ml_resume.pdf"

    st.session_state.sample_loaded = True
    st.session_state.eval_results = None


# ---------------------------------------------------------------------------
# Sidebar UI: Demo Controls, History Drawer & Academic Metadata
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🎓 MCA Minor Project")
    st.caption("**Automated Resume & Skill Gap Analyzer**")
    st.caption("3rd-Semester Academic Submission")

    st.divider()

    st.markdown("#### ⚡ Viva Live Demo")
    if st.button("🚀 Load Sample ML Resume & JD", on_click=load_demo_data, use_container_width=True, type="primary"):
        st.toast("✅ Sample Candidate Data Loaded for Live Demo!", icon="🎯")

    if st.session_state.sample_loaded:
        st.caption("🟢 **Demo Mode Active**: Alex Rivera vs. Senior ML Role")

    st.divider()

    # Pre-cache model status
    st.markdown("#### 🧠 Model Engine Status")
    with st.spinner("Checking Sentence-Transformer..."):
        try:
            _ = load_embedding_model("all-MiniLM-L6-v2")
            st.success("✅ `all-MiniLM-L6-v2` (384-d) Online", icon="🟢")
        except Exception as e:
            st.warning(f"Embedding model loading: {e}")

    st.caption("Formula: **Composite = 60% Semantic + 40% Overlap**")

    st.divider()

    # Past Evaluations History Section
    st.markdown("#### 📜 Evaluation History")
    history_records = get_all_history()
    st.caption(f"Total Evaluations Logged: **{len(history_records)}**")

    if history_records:
        df_history = get_history_df()

        # CSV Export
        csv_data = df_history.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download History (CSV)",
            data=csv_data,
            file_name="resume_evaluations_history.csv",
            mime="text/csv",
            use_container_width=True
        )

        with st.expander("👁️ View History Log"):
            st.dataframe(
                df_history[["ID", "Candidate", "Composite %", "Semantic %", "Overlap %"]],
                use_container_width=True,
                height=180
            )

        if st.button("🗑️ Clear Evaluation History", use_container_width=True):
            clear_history()
            st.toast("Evaluation history cleared.", icon="🗑️")
            st.rerun()
    else:
        st.caption("No evaluations logged yet. Run your first analysis to see records here.")

    st.divider()
    st.markdown(
        "<small style='color: #64748B;'>Antigravity AI Architecture • Streamlit + PyTorch</small>",
        unsafe_allow_html=True
    )


# ---------------------------------------------------------------------------
# Main Application Header
# ---------------------------------------------------------------------------
st.markdown("""
<div class="main-header">
    <h1>🎯 Automated Resume & Skill Gap Analyzer</h1>
    <p>Hybrid Semantic Embedding (Sentence-Transformers) + Rule-Based Skill Taxonomy Matching Engine</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# 2-Column Split Layout
# ---------------------------------------------------------------------------
col_input, col_results = st.columns([1, 1.25], gap="large")

# ===========================================================================
# Left Column: Inputs & Orchestration
# ===========================================================================
with col_input:
    st.markdown("### 📄 Candidate & Document Input")

    candidate_name = st.text_input(
        "Candidate Name",
        value=st.session_state.candidate_name,
        placeholder="e.g. Alex Rivera",
        help="Full name or identifier for the candidate being evaluated."
    )

    # File uploader
    uploaded_file = st.file_uploader(
        "Upload Resume (.PDF or .DOCX)",
        type=["pdf", "docx", "txt"],
        help="Supports multi-page PDF and DOCX files. Scanned images require OCR."
    )

    # Notice if demo resume is currently active
    if uploaded_file is None and st.session_state.sample_loaded and st.session_state.uploaded_resume_bytes:
        st.markdown("""
        <div class="demo-info-box">
            📎 <b>Using Pre-loaded Sample Resume:</b> <code>sample_ml_resume.pdf</code> (Alex Rivera)<br/>
            <i>To upload a custom resume, drop a file into the uploader above.</i>
        </div>
        """, unsafe_allow_html=True)

    # Job Description Input
    jd_text = st.text_area(
        "Target Job Description (JD)",
        value=st.session_state.jd_text,
        height=280,
        placeholder="Paste the target job description or requirements specification here...",
        help="Include role responsibilities, required technical skills, qualifications, and tool stack."
    )

    # Trigger Analysis Button
    analyze_clicked = st.button(
        "⚡ Run Gap Analysis & Compatibility Scoring",
        type="primary",
        use_container_width=True
    )


# ===========================================================================
# Execution Trigger & Processing Logic
# ===========================================================================
if analyze_clicked:
    # 1. Resolve Resume Source
    resume_text = ""
    resolved_filename = ""

    if uploaded_file is not None:
        resolved_filename = uploaded_file.name
        try:
            with st.spinner("Extracting and normalizing document text..."):
                file_bytes = uploaded_file.read()
                resume_text = extract_text(io.BytesIO(file_bytes), resolved_filename)
        except Exception as err:
            st.error(f"Error parsing uploaded document: {err}")
            resume_text = ""
    elif st.session_state.sample_loaded and st.session_state.uploaded_resume_bytes:
        resolved_filename = st.session_state.uploaded_resume_name or "sample_ml_resume.pdf"
        try:
            with st.spinner("Extracting sample PDF text..."):
                resume_text = extract_text(io.BytesIO(st.session_state.uploaded_resume_bytes), resolved_filename)
        except Exception as err:
            st.error(f"Error parsing sample PDF: {err}")
            resume_text = ""
    else:
        st.warning("⚠️ Please upload a resume (.pdf or .docx) or click 'Load Sample ML Resume & JD' in the sidebar.")

    # 2. Validate JD
    if not jd_text.strip():
        st.warning("⚠️ Please provide a Target Job Description to compare against.")

    # 3. Perform Analysis if Both Texts Available
    if resume_text.strip() and jd_text.strip():
        with st.spinner("Generating 384-dimensional dense semantic embeddings and executing taxonomy matching..."):
            start_time = time.time()
            results = analyze_resume_and_jd(
                resume_text=resume_text,
                jd_text=jd_text,
                candidate_name=candidate_name.strip() or "Unnamed Candidate"
            )
            elapsed = time.time() - start_time

            # 4. Save Evaluation to SQLite
            try:
                eval_id = save_evaluation(
                    candidate_name=results["candidate_name"],
                    filename=resolved_filename,
                    semantic_score=results["semantic_score"],
                    skill_overlap_score=results["skill_overlap_score"],
                    composite_score=results["composite_score"],
                    matched_skills=results["matched_skills"],
                    missing_skills=results["missing_skills"]
                )
                results["eval_id"] = eval_id
                results["elapsed"] = round(elapsed, 2)
                results["filename"] = resolved_filename
                results["resume_char_count"] = len(resume_text)
                results["jd_char_count"] = len(jd_text)
            except Exception as db_err:
                st.warning(f"Could not persist record to database: {db_err}")

            st.session_state.eval_results = results
            st.toast("🎉 Analysis Completed Successfully!", icon="✨")


# ===========================================================================
# Right Column: High-Visibility Evaluation Dashboard
# ===========================================================================
with col_results:
    st.markdown("### 📊 Compatibility & Gap Report")

    res = st.session_state.eval_results

    if res is None:
        st.info(
            "👈 **Awaiting Input**: Upload a candidate's resume and job description on the left, "
            "or click **'Load Sample ML Resume & JD'** in the sidebar to run a live demonstration."
        )
    else:
        # 1. Key Metric Score Cards
        m_col1, m_col2, m_col3 = st.columns(3)

        with m_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Composite Match</div>
                <div class="metric-value-primary">{res['composite_score_pct']}%</div>
                <div class="metric-subtitle">60% Semantic + 40% Overlap</div>
            </div>
            """, unsafe_allow_html=True)

        with m_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Semantic Cosine</div>
                <div class="metric-value-blue">{res['semantic_score_pct']}%</div>
                <div class="metric-subtitle">MiniLM-L6-v2 Dense Vectors</div>
            </div>
            """, unsafe_allow_html=True)

        with m_col3:
            total_req = res['total_jd_skills_count']
            matched_cnt = res['matched_skills_count']
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Skill Overlap</div>
                <div class="metric-value-green">{res['skill_overlap_pct']}%</div>
                <div class="metric-subtitle">{matched_cnt} of {total_req} Required Skills</div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")

        # Progress Visual Indicator
        st.progress(res['composite_score'], text=f"Overall Candidate Compatibility: {res['composite_score_pct']}%")

        st.divider()

        # 2. Matched Skills (Green)
        st.markdown(f"#### ✅ Matched Skills ({len(res['matched_skills'])})")
        if res['matched_skills']:
            matched_html = "".join([f'<span class="badge-matched">✓ {skill}</span>' for skill in res['matched_skills']])
            st.markdown(f'<div class="skill-container">{matched_html}</div>', unsafe_allow_html=True)
        else:
            st.caption("No direct taxonomy skill overlaps detected.")

        # 3. Missing Skills (Amber/Red)
        st.markdown(f"#### ⚠️ Missing Skills to Learn ({len(res['missing_skills'])})")
        if res['missing_skills']:
            missing_html = "".join([f'<span class="badge-missing">✕ {skill}</span>' for skill in res['missing_skills']])
            st.markdown(f'<div class="skill-container">{missing_html}</div>', unsafe_allow_html=True)
        else:
            st.success("🎯 Candidate satisfies all identified technical skill requirements!")

        # 4. Actionable Bridge-the-Gap Recommendations
        st.markdown("#### 🎯 Priority Recommendations to Bridge the Gap")
        recommendations = res.get("recommendations", [])
        if recommendations:
            for rec in recommendations[:5]:  # Display top 5 actionable suggestions
                prio_class = "high-priority" if rec.get("priority") == "High" else "medium-priority"
                tag_class = "rec-tag-high" if rec.get("priority") == "High" else "rec-tag-medium"
                st.markdown(f"""
                <div class="rec-card {prio_class}">
                    <div style="display: flex; align-items: center;">
                        <span class="rec-skill-name">Learn {rec['skill']}</span>
                        <span class="rec-tag {tag_class}">{rec.get('priority', 'Medium')} Priority</span>
                        <span style="font-size: 11px; color: #64748B; margin-left: auto;">
                            {rec.get('category', 'Technical')}
                        </span>
                    </div>
                    <div class="rec-advice">{rec['advice']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("No skill gaps identified.")

        # 5. Expandable Full Technical Details
        with st.expander("🔍 Deep Inspection & Skill Matrix"):
            tab1, tab2, tab3 = st.tabs(["Resume Skills", "JD Required Skills", "Evaluation Audit"])

            with tab1:
                st.markdown("**All Skills Detected in Resume:**")
                extra_html = "".join([f'<span class="badge-extra">• {s}</span>' for s in res['resume_skills']])
                st.markdown(f'<div class="skill-container">{extra_html}</div>', unsafe_allow_html=True)

            with tab2:
                st.markdown("**All Skills Required in Job Description:**")
                jd_html = "".join([f'<span class="badge-extra">• {s}</span>' for s in res['jd_skills']])
                st.markdown(f'<div class="skill-container">{jd_html}</div>', unsafe_allow_html=True)

            with tab3:
                st.markdown(f"""
                - **Candidate Name:** `{res['candidate_name']}`
                - **Evaluated File:** `{res.get('filename', 'N/A')}`
                - **Resume Characters:** `{res.get('resume_char_count', 'N/A')}`
                - **Job Description Characters:** `{res.get('jd_char_count', 'N/A')}`
                - **Evaluation Runtime:** `{res.get('elapsed', 0)} seconds`
                - **Database Record ID:** `#{res.get('eval_id', 'N/A')}`
                """)
