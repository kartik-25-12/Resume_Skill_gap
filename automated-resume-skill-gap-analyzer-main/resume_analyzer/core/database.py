"""
core/database.py
SQLite persistence layer for candidate evaluation history and gap analysis records.
"""

import json
import os
import sqlite3
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd

DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "evaluations.sqlite")


def get_connection(db_path: str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """
    Returns an active SQLite connection with row factory enabled for dict access.
    """
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = DEFAULT_DB_PATH) -> None:
    """
    Initializes the evaluations.sqlite database and creates the 'history' table if it doesn't exist.
    """
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                candidate_name TEXT NOT NULL,
                filename TEXT NOT NULL,
                semantic_score REAL NOT NULL,
                skill_overlap_score REAL NOT NULL,
                composite_score REAL NOT NULL,
                matched_skills_json TEXT NOT NULL,
                missing_skills_json TEXT NOT NULL
            );
        """)
        conn.commit()


def save_evaluation(
    candidate_name: str,
    filename: str,
    semantic_score: float,
    skill_overlap_score: float,
    composite_score: float,
    matched_skills: List[str],
    missing_skills: List[str],
    db_path: str = DEFAULT_DB_PATH
) -> int:
    """
    Inserts a newly evaluated resume record into the SQLite history table.

    Returns:
        The auto-generated row ID of the inserted evaluation.
    """
    init_db(db_path)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    matched_json = json.dumps(matched_skills)
    missing_json = json.dumps(missing_skills)

    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO history (
                timestamp, candidate_name, filename,
                semantic_score, skill_overlap_score, composite_score,
                matched_skills_json, missing_skills_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            timestamp,
            candidate_name.strip() or "Unnamed Candidate",
            filename,
            round(float(semantic_score), 4),
            round(float(skill_overlap_score), 4),
            round(float(composite_score), 4),
            matched_json,
            missing_json
        ))
        conn.commit()
        return cursor.lastrowid


def get_all_history(db_path: str = DEFAULT_DB_PATH) -> List[Dict[str, Any]]:
    """
    Retrieves all past evaluations ordered from newest to oldest.
    """
    init_db(db_path)
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, timestamp, candidate_name, filename,
                   semantic_score, skill_overlap_score, composite_score,
                   matched_skills_json, missing_skills_json
            FROM history
            ORDER BY id DESC;
        """)
        rows = cursor.fetchall()
        results = []
        for r in rows:
            results.append({
                "id": r["id"],
                "timestamp": r["timestamp"],
                "candidate_name": r["candidate_name"],
                "filename": r["filename"],
                "semantic_score": r["semantic_score"],
                "skill_overlap_score": r["skill_overlap_score"],
                "composite_score": r["composite_score"],
                "matched_skills": json.loads(r["matched_skills_json"]),
                "missing_skills": json.loads(r["missing_skills_json"])
            })
        return results


def get_history_df(db_path: str = DEFAULT_DB_PATH) -> pd.DataFrame:
    """
    Returns history as a Pandas DataFrame formatted for table display & CSV export.
    """
    records = get_all_history(db_path)
    if not records:
        return pd.DataFrame(columns=[
            "ID", "Timestamp", "Candidate", "File",
            "Semantic %", "Overlap %", "Composite %", "Matched Count", "Missing Count"
        ])

    data = []
    for rec in records:
        data.append({
            "ID": rec["id"],
            "Timestamp": rec["timestamp"],
            "Candidate": rec["candidate_name"],
            "File": rec["filename"],
            "Semantic %": round(rec["semantic_score"] * 100, 1),
            "Overlap %": round(rec["skill_overlap_score"] * 100, 1),
            "Composite %": round(rec["composite_score"] * 100, 1),
            "Matched Count": len(rec["matched_skills"]),
            "Missing Count": len(rec["missing_skills"]),
            "Matched Skills": ", ".join(rec["matched_skills"]),
            "Missing Skills": ", ".join(rec["missing_skills"])
        })
    return pd.DataFrame(data)


def clear_history(db_path: str = DEFAULT_DB_PATH) -> None:
    """
    Truncates all records from the history table.
    """
    init_db(db_path)
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM history;")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='history';")
        conn.commit()
