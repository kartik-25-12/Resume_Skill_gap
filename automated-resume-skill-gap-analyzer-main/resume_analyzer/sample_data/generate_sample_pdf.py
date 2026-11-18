"""
Script to generate a professional PDF resume for sample testing and viva demo.
Uses reportlab to generate resume_analyzer/sample_data/sample_ml_resume.pdf
"""

import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer


def generate_pdf(output_path: str):
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1E293B')
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#2563EB')
    )

    contact_style = ParagraphStyle(
        'DocContact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#64748B')
    )

    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=10,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#334155')
    )

    bullet_style = ParagraphStyle(
        'BulletDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155'),
        leftIndent=12
    )

    elements = []

    # Header
    elements.append(Paragraph("Alex Rivera", title_style))
    elements.append(Paragraph("Machine Learning & NLP Engineer | Data Scientist", subtitle_style))
    elements.append(Paragraph(
        "San Francisco, CA &nbsp;|&nbsp; alex.rivera@example.com &nbsp;|&nbsp; "
        "+1 (555) 234-5678 &nbsp;|&nbsp; github.com/alexrivera-ml",
        contact_style
    ))
    elements.append(Spacer(1, 8))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#3B82F6'), spaceAfter=10))

    # Summary
    elements.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
    elements.append(Paragraph(
        "Results-oriented Machine Learning Engineer with 3+ years of experience developing, training, and evaluating "
        "predictive models, Deep Learning architectures, and Natural Language Processing (NLP) solutions. "
        "Proficient in Python, PyTorch, Scikit-Learn, and Docker. Proven track record of architecting microservices "
        "with FastAPI and PostgreSQL to serve high-accuracy inference engines in production.",
        body_style
    ))
    elements.append(Spacer(1, 6))

    # Technical Skills
    elements.append(Paragraph("TECHNICAL SKILLS", heading_style))
    skills_text = (
        "<b>Programming & Languages:</b> Python, C++, SQL, Bash/Shell scripting<br/>"
        "<b>Machine Learning & AI:</b> Scikit-Learn (sklearn), PyTorch, Deep Learning, NLP, "
        "Computer Vision, Transformers, NumPy, Pandas<br/>"
        "<b>Tools & Infrastructure:</b> Docker, Git, GitHub Actions, Linux, FastAPI, Flask<br/>"
        "<b>Databases:</b> PostgreSQL, MySQL, SQLite<br/>"
        "<b>Core Competencies:</b> Data Structures & Algorithms, REST APIs, Microservices, Statistical Analysis"
    )
    elements.append(Paragraph(skills_text, body_style))
    elements.append(Spacer(1, 6))

    # Experience
    elements.append(Paragraph("WORK EXPERIENCE", heading_style))
    elements.append(Paragraph(
        "<b>Machine Learning Engineer</b> &mdash; <i>Cortex Analytics Lab</i> (2022 &ndash; Present)",
        body_style
    ))
    elements.append(Paragraph(
        "&bull; Designed and trained deep learning NLP classification models using PyTorch, "
        "achieving 94.2% F1-score across 500k customer sentiment queries.",
        bullet_style
    ))
    elements.append(Paragraph(
        "&bull; Engineered feature extraction pipelines using Scikit-Learn and Pandas, "
        "reducing model training preprocessing time by 38%.",
        bullet_style
    ))
    elements.append(Paragraph(
        "&bull; Containerized ML inference services using Docker and served endpoints "
        "through high-performance FastAPI backends.",
        bullet_style
    ))
    elements.append(Paragraph(
        "&bull; Integrated PostgreSQL database queries for automated storage of evaluation metrics, "
        "embeddings, and drift logs.",
        bullet_style
    ))
    elements.append(Spacer(1, 6))

    elements.append(Paragraph(
        "<b>Junior Data Scientist</b> &mdash; <i>Apex Data Solutions</i> (2020 &ndash; 2022)",
        body_style
    ))
    elements.append(Paragraph(
        "&bull; Developed supervised learning algorithms with Python and Scikit-Learn to "
        "forecast inventory churn for e-commerce clients.",
        bullet_style
    ))
    elements.append(Paragraph(
        "&bull; Built automated exploratory data analysis scripts with Matplotlib, Seaborn, and Pandas.",
        bullet_style
    ))
    elements.append(Paragraph(
        "&bull; Maintained Git version control workflows and collaborated within an Agile Scrum team.",
        bullet_style
    ))
    elements.append(Spacer(1, 6))

    # Education
    elements.append(Paragraph("EDUCATION", heading_style))
    elements.append(Paragraph(
        "<b>Master of Computer Applications (MCA)</b> &mdash; Computer Science & AI (2020)",
        body_style
    ))
    elements.append(Paragraph(
        "<b>B.Sc. in Computer Science</b> &mdash; First Class with Distinction (2018)",
        body_style
    ))
    elements.append(Spacer(1, 6))

    # Key Projects
    elements.append(Paragraph("NOTABLE PROJECTS", heading_style))
    elements.append(Paragraph(
        "<b>Neural Text Summarizer:</b> Trained transformer models with PyTorch on 100k "
        "article records with automated evaluation benchmarks.",
        bullet_style
    ))
    elements.append(Paragraph(
        "<b>Object Detection Vision API:</b> Developed OpenCV and PyTorch pipeline containerized "
        "with Docker for real-time asset tagging.",
        bullet_style
    ))

    doc.build(elements)
    print(f"Sample PDF successfully created at: {output_path}")


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_ml_resume.pdf")
    generate_pdf(out)
