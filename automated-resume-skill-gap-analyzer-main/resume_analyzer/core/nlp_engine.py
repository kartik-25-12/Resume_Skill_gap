"""
core/nlp_engine.py
Semantic matching, skill taxonomy extraction, and compatibility scoring.
Powered by Sentence-Transformers (all-MiniLM-L6-v2) and Scikit-Learn Cosine Similarity.
"""

import re
from typing import Any, Dict, List, Optional, Set

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Optional Streamlit caching wrapper if running within Streamlit context
try:
    import streamlit as st
    cache_decorator = st.cache_resource
except Exception:
    def cache_decorator(func):
        return func


# ---------------------------------------------------------------------------
# Comprehensive Technical Skill Taxonomy & Alias Mapping
# ---------------------------------------------------------------------------
SKILL_TAXONOMY: Dict[str, Dict[str, Any]] = {
    # Machine Learning & AI
    "Machine Learning": {
        "aliases": [
            "machine learning", "ml", "supervised learning",
            "unsupervised learning", "scikit-learn", "sklearn"
        ],
        "category": "AI / Machine Learning",
        "priority": "High"
    },
    "Deep Learning": {
        "aliases": [
            "deep learning", "dl", "neural networks",
            "cnn", "rnn", "lstm", "pytorch", "torch"
        ],
        "category": "AI / Machine Learning",
        "priority": "High"
    },
    "PyTorch": {
        "aliases": ["pytorch", "torch"],
        "category": "AI / Machine Learning",
        "priority": "High"
    },
    "TensorFlow": {
        "aliases": ["tensorflow", "tf", "keras"],
        "category": "AI / Machine Learning",
        "priority": "High"
    },
    "Natural Language Processing": {
        "aliases": [
            "natural language processing", "nlp", "spacy", "nltk",
            "huggingface", "transformers", "bert", "tokenization"
        ],
        "category": "AI / Machine Learning",
        "priority": "High"
    },
    "Computer Vision": {
        "aliases": [
            "computer vision", "cv", "opencv", "yolo",
            "image processing", "object detection"
        ],
        "category": "AI / Machine Learning",
        "priority": "Medium"
    },
    "Large Language Models (LLMs)": {
        "aliases": [
            "llm", "llms", "large language models", "generative ai",
            "genai", "prompt engineering", "langchain", "llamaindex", "rag"
        ],
        "category": "AI / Machine Learning",
        "priority": "High"
    },
    "MLOps": {
        "aliases": [
            "mlops", "mlflow", "kubeflow", "model deployment",
            "model monitoring", "dvc", "wandb"
        ],
        "category": "AI / Machine Learning",
        "priority": "High"
    },

    # Programming Languages
    "Python": {
        "aliases": ["python", "python3", "py"],
        "category": "Programming Languages",
        "priority": "High"
    },
    "Java": {
        "aliases": ["java", "jvm", "spring", "spring boot"],
        "category": "Programming Languages",
        "priority": "Medium"
    },
    "C++": {
        "aliases": ["c++", "cpp"],
        "category": "Programming Languages",
        "priority": "Medium"
    },
    "JavaScript": {
        "aliases": ["javascript", "js", "es6", "node", "nodejs"],
        "category": "Programming Languages",
        "priority": "Medium"
    },
    "TypeScript": {
        "aliases": ["typescript", "ts"],
        "category": "Programming Languages",
        "priority": "Medium"
    },
    "Go / Golang": {
        "aliases": ["golang", "go language"],
        "category": "Programming Languages",
        "priority": "Medium"
    },
    "R": {
        "aliases": ["r programming", "r language", "r-project"],
        "category": "Programming Languages",
        "priority": "Medium"
    },

    # Data Science & Analytics
    "Pandas": {
        "aliases": ["pandas", "dataframe", "dataframes"],
        "category": "Data Science & Analytics",
        "priority": "Medium"
    },
    "NumPy": {
        "aliases": ["numpy", "numerical python"],
        "category": "Data Science & Analytics",
        "priority": "Medium"
    },
    "Data Visualization": {
        "aliases": [
            "matplotlib", "seaborn", "plotly", "tableau",
            "power bi", "data visualization"
        ],
        "category": "Data Science & Analytics",
        "priority": "Medium"
    },

    # Data Engineering & Big Data
    "Apache Spark": {
        "aliases": ["spark", "pyspark", "apache spark", "databricks"],
        "category": "Data Engineering",
        "priority": "High"
    },
    "Apache Kafka": {
        "aliases": ["kafka", "apache kafka", "event streaming"],
        "category": "Data Engineering",
        "priority": "High"
    },
    "Apache Airflow": {
        "aliases": ["airflow", "apache airflow", "data orchestration", "dag"],
        "category": "Data Engineering",
        "priority": "High"
    },

    # Databases & Storage
    "SQL": {
        "aliases": ["sql", "rdbms", "relational databases"],
        "category": "Databases & Storage",
        "priority": "High"
    },
    "PostgreSQL": {
        "aliases": ["postgresql", "postgres", "psql"],
        "category": "Databases & Storage",
        "priority": "Medium"
    },
    "MySQL": {
        "aliases": ["mysql"],
        "category": "Databases & Storage",
        "priority": "Medium"
    },
    "NoSQL / MongoDB": {
        "aliases": ["mongodb", "nosql", "documentdb", "cassandra", "dynamodb"],
        "category": "Databases & Storage",
        "priority": "Medium"
    },
    "Redis": {
        "aliases": ["redis", "in-memory cache"],
        "category": "Databases & Storage",
        "priority": "Low"
    },

    # Cloud & Infrastructure
    "AWS": {
        "aliases": ["aws", "amazon web services", "ec2", "s3", "lambda", "sagemaker"],
        "category": "Cloud & DevOps",
        "priority": "High"
    },
    "Google Cloud Platform (GCP)": {
        "aliases": ["gcp", "google cloud", "bigquery", "vertex ai"],
        "category": "Cloud & DevOps",
        "priority": "High"
    },
    "Microsoft Azure": {
        "aliases": ["azure", "microsoft azure", "azure ml"],
        "category": "Cloud & DevOps",
        "priority": "Medium"
    },
    "Docker": {
        "aliases": [
            "docker", "containerization", "containers",
            "dockerfile", "docker compose"
        ],
        "category": "Cloud & DevOps",
        "priority": "High"
    },
    "Kubernetes": {
        "aliases": ["kubernetes", "k8s", "container orchestration", "helm"],
        "category": "Cloud & DevOps",
        "priority": "High"
    },
    "CI/CD": {
        "aliases": [
            "ci/cd", "cicd", "continuous integration",
            "continuous deployment", "jenkins", "github actions", "gitlab ci"
        ],
        "category": "Cloud & DevOps",
        "priority": "High"
    },
    "Git": {
        "aliases": ["git", "github", "version control"],
        "category": "Cloud & DevOps",
        "priority": "Medium"
    },
    "Linux": {
        "aliases": ["linux", "unix", "bash", "shell scripting", "ubuntu"],
        "category": "Cloud & DevOps",
        "priority": "Medium"
    },

    # Web & API Frameworks
    "FastAPI": {
        "aliases": ["fastapi", "uvicorn"],
        "category": "Web & APIs",
        "priority": "Medium"
    },
    "Flask": {
        "aliases": ["flask", "werkzeug"],
        "category": "Web & APIs",
        "priority": "Medium"
    },
    "Django": {
        "aliases": ["django"],
        "category": "Web & APIs",
        "priority": "Medium"
    },
    "REST APIs": {
        "aliases": ["rest", "restful", "rest api", "rest apis", "microservices"],
        "category": "Web & APIs",
        "priority": "Medium"
    },
    "React": {
        "aliases": ["react", "react.js", "reactjs"],
        "category": "Web & APIs",
        "priority": "Low"
    },

    # Software Engineering Core
    "Data Structures & Algorithms": {
        "aliases": ["dsa", "data structures", "algorithms", "problem solving"],
        "category": "Core CS",
        "priority": "High"
    },
    "System Design": {
        "aliases": [
            "system design", "distributed systems",
            "software architecture", "scalability", "high availability"
        ],
        "category": "Core CS",
        "priority": "High"
    }
}


@cache_decorator
def load_embedding_model(model_name: str = "all-MiniLM-L6-v2") -> SentenceTransformer:
    """
    Initializes and caches the Sentence-Transformer embedding model.
    'all-MiniLM-L6-v2' maps sentences & paragraphs to a 384-dimensional dense vector space.
    """
    return SentenceTransformer(model_name)


def extract_skills_from_text(text: str) -> Set[str]:
    """
    Extracts canonical technical skills from document text using regex word-boundary matching.
    Matches aliases to their canonical skill names.
    """
    if not text:
        return set()

    found_skills: Set[str] = set()
    cleaned_lower = text.lower()

    for canonical_name, data in SKILL_TAXONOMY.items():
        for alias in data["aliases"]:
            # Protect against partial substring match by anchoring to word boundaries
            # Handle special symbols like C++, CI/CD, .js safely
            escaped_alias = re.escape(alias.lower())
            pattern = r"(?<!\w)" + escaped_alias + r"(?!\w)"
            if re.search(pattern, cleaned_lower):
                found_skills.add(canonical_name)
                break  # Matched this skill, continue to next canonical skill

    return found_skills


def compute_semantic_similarity(
    text_a: str,
    text_b: str,
    model: Optional[SentenceTransformer] = None
) -> float:
    """
    Computes dense semantic cosine similarity between two text blocks using Sentence-Transformers.
    Returns a score normalized between 0.0 and 1.0.
    """
    if not text_a.strip() or not text_b.strip():
        return 0.0

    if model is None:
        model = load_embedding_model()

    embeddings = model.encode([text_a, text_b], convert_to_numpy=True)
    sim_matrix = cosine_similarity([embeddings[0]], [embeddings[1]])
    sim_score = float(sim_matrix[0][0])
    # Clip negative similarity values to 0.0
    return max(0.0, min(1.0, sim_score))


def generate_recommendations(missing_skills: List[str]) -> List[Dict[str, str]]:
    """
    Generates tailored, actionable bridge-the-gap recommendations for missing skills.
    """
    if not missing_skills:
        return [{
            "skill": "All Requirements Met",
            "category": "Complete Match",
            "advice": "Candidate possesses all required technical competencies for this position."
        }]

    recommendations = []
    for skill in missing_skills:
        info = SKILL_TAXONOMY.get(skill, {"category": "Technical", "priority": "Medium"})
        category = info.get("category", "Technical")
        priority = info.get("priority", "Medium")

        if "Machine Learning" in category or "AI" in category:
            advice = (
                f"Implement a portfolio project featuring {skill} "
                f"(e.g. model training, evaluation, fine-tuning) with GitHub documentation."
            )
        elif "Cloud" in category or "DevOps" in category:
            advice = f"Deploy containerized microservices using {skill} and publish an automated CI/CD pipeline."
        elif "Data Engineering" in category:
            advice = f"Build an end-to-end streaming or batch ETL pipeline highlighting {skill}."
        elif "Databases" in category:
            advice = f"Demonstrate schema modeling, query optimization, and indexing with {skill}."
        else:
            advice = f"Complete practical coursework or develop a focused GitHub repository showcasing {skill}."

        recommendations.append({
            "skill": skill,
            "category": category,
            "priority": priority,
            "advice": advice
        })

    # Sort so High priority missing skills appear first
    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    recommendations.sort(key=lambda x: priority_order.get(x["priority"], 99))
    return recommendations


def analyze_resume_and_jd(
    resume_text: str,
    jd_text: str,
    candidate_name: str = "Candidate",
    model: Optional[SentenceTransformer] = None
) -> Dict[str, Any]:
    """
    Comprehensive pipeline:
    1. Extracts technical skill sets from Resume and Job Description.
    2. Computes Matched Skills (intersection) and Missing Skills (difference).
    3. Calculates Skill Overlap Ratio = |Matched| / |JD Skills|.
    4. Computes Dense Semantic Cosine Similarity via Sentence-Transformers.
    5. Calculates Weighted Composite Compatibility Score:
       Composite = (0.6 * Semantic Similarity) + (0.4 * Skill Overlap Ratio).
    6. Formulates actionable skill gap recommendations.

    Returns:
        Structured dictionary containing all evaluation metrics, sets, and recommendations.
    """
    # 1. Skill Extraction
    resume_skills: Set[str] = extract_skills_from_text(resume_text)
    jd_skills: Set[str] = extract_skills_from_text(jd_text)

    # 2. Set Operations
    matched_skills: Set[str] = resume_skills.intersection(jd_skills)
    missing_skills: Set[str] = jd_skills - resume_skills
    extra_skills: Set[str] = resume_skills - jd_skills

    # 3. Skill Overlap Ratio
    if len(jd_skills) > 0:
        skill_overlap_ratio = len(matched_skills) / len(jd_skills)
    else:
        # If JD specified no explicit taxonomy skills, base purely on semantic context
        skill_overlap_ratio = 1.0 if len(resume_skills) > 0 else 0.0

    # 4. Semantic Similarity (Sentence-Transformers)
    semantic_similarity = compute_semantic_similarity(resume_text, jd_text, model=model)

    # 5. Composite Score = 60% Semantic + 40% Keyword Skill Overlap
    composite_score = (0.6 * semantic_similarity) + (0.4 * skill_overlap_ratio)

    # Convert to sorted lists for JSON serialization and frontend display
    matched_list = sorted(list(matched_skills))
    missing_list = sorted(list(missing_skills))
    extra_list = sorted(list(extra_skills))
    resume_skills_list = sorted(list(resume_skills))
    jd_skills_list = sorted(list(jd_skills))

    # 6. Actionable Recommendations
    recommendations = generate_recommendations(missing_list)

    return {
        "candidate_name": candidate_name,
        "semantic_score": round(float(semantic_similarity), 4),
        "semantic_score_pct": round(float(semantic_similarity) * 100, 1),
        "skill_overlap_score": round(float(skill_overlap_ratio), 4),
        "skill_overlap_pct": round(float(skill_overlap_ratio) * 100, 1),
        "composite_score": round(float(composite_score), 4),
        "composite_score_pct": round(float(composite_score) * 100, 1),
        "total_resume_skills_count": len(resume_skills),
        "total_jd_skills_count": len(jd_skills),
        "matched_skills_count": len(matched_skills),
        "missing_skills_count": len(missing_skills),
        "matched_skills": matched_list,
        "missing_skills": missing_list,
        "extra_skills": extra_list,
        "resume_skills": resume_skills_list,
        "jd_skills": jd_skills_list,
        "recommendations": recommendations
    }
