"""
Automated unit & integration test suite for Resume & Skill Gap Analyzer.
Verifies parsing, NLP similarity, database transactions, and end-to-end flow.
"""

import os
import sys
import unittest

# Ensure resume_analyzer is on path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from core.database import clear_history, get_all_history, get_history_df, save_evaluation
from core.nlp_engine import analyze_resume_and_jd, extract_skills_from_text
from core.parser import clean_text, parse_pdf


class TestResumeAnalyzer(unittest.TestCase):

    def setUp(self):
        self.sample_pdf = os.path.join(BASE_DIR, "sample_data", "sample_ml_resume.pdf")
        self.sample_jd = os.path.join(BASE_DIR, "sample_data", "sample_ml_jd.txt")
        self.test_db = os.path.join(BASE_DIR, "test_evaluations.sqlite")

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_01_text_cleaning(self):
        dirty = "Hello\u2019s world! \u2022 bullet point \t with spaces.\n\n\nNext line."
        cleaned = clean_text(dirty)
        self.assertIn("Hello's world!", cleaned)
        self.assertNotIn("\u2019", cleaned)
        self.assertNotIn("\u2022", cleaned)

    def test_02_pdf_parser(self):
        self.assertTrue(os.path.exists(self.sample_pdf), "sample_ml_resume.pdf must exist")
        text = parse_pdf(self.sample_pdf)
        self.assertGreater(len(text), 500)
        self.assertIn("Alex Rivera", text)
        self.assertIn("PyTorch", text)

    def test_03_skill_extraction(self):
        sample = (
            "Proficient in Python, PyTorch, Docker, Kubernetes, and PostgreSQL. "
            "Familiar with scikit-learn and AWS."
        )
        skills = extract_skills_from_text(sample)
        self.assertIn("Python", skills)
        self.assertIn("PyTorch", skills)
        self.assertIn("Docker", skills)
        self.assertIn("Kubernetes", skills)
        self.assertIn("PostgreSQL", skills)
        self.assertIn("Machine Learning", skills)  # from scikit-learn
        self.assertIn("AWS", skills)

    def test_04_nlp_similarity_and_composite(self):
        resume_text = parse_pdf(self.sample_pdf)
        with open(self.sample_jd, "r", encoding="utf-8") as f:
            jd_text = f.read()

        results = analyze_resume_and_jd(resume_text, jd_text, candidate_name="Alex Rivera")
        self.assertIn("composite_score", results)
        self.assertIn("semantic_score", results)
        self.assertIn("skill_overlap_score", results)
        self.assertGreater(results["composite_score"], 0.4)
        self.assertLessEqual(results["composite_score"], 1.0)
        self.assertIn("Docker", results["matched_skills"])
        self.assertIn("Kubernetes", results["missing_skills"])

    def test_05_database_crud(self):
        clear_history(self.test_db)
        eval_id = save_evaluation(
            candidate_name="Test Candidate",
            filename="resume.pdf",
            semantic_score=0.75,
            skill_overlap_score=0.80,
            composite_score=0.77,
            matched_skills=["Python", "SQL"],
            missing_skills=["Kubernetes"],
            db_path=self.test_db
        )
        self.assertIsInstance(eval_id, int)
        history = get_all_history(self.test_db)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["candidate_name"], "Test Candidate")

        df = get_history_df(self.test_db)
        self.assertEqual(len(df), 1)
        self.assertIn("Composite %", df.columns)

        clear_history(self.test_db)
        history_after = get_all_history(self.test_db)
        self.assertEqual(len(history_after), 0)


if __name__ == "__main__":
    unittest.main()
