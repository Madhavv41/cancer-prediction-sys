import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "cancer_app.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                created_at TEXT NOT NULL,
                age REAL NOT NULL,
                gender INTEGER NOT NULL,
                bmi REAL NOT NULL,
                smoking INTEGER NOT NULL,
                genetic_risk INTEGER NOT NULL,
                physical_activity REAL NOT NULL,
                alcohol_intake REAL NOT NULL,
                cancer_history INTEGER NOT NULL,
                prediction_label TEXT NOT NULL,
                diagnosis_code INTEGER NOT NULL,
                confidence REAL NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
            """
        )


def create_user(username, email, password_hash):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO users (username, email, password_hash, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (username, email, password_hash, datetime.utcnow().isoformat()),
        )


def get_user_by_username(username):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,),
        ).fetchone()
        return dict(row) if row else None


def get_user_by_email(email):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,),
        ).fetchone()
        return dict(row) if row else None


def get_user_by_id(user_id):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, username, email, created_at FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
        return dict(row) if row else None


def save_prediction(user_id, form_data, result):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO predictions (
                user_id, created_at, age, gender, bmi, smoking,
                genetic_risk, physical_activity, alcohol_intake,
                cancer_history, prediction_label, diagnosis_code, confidence
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                datetime.utcnow().isoformat(),
                float(form_data["age"]),
                int(form_data["gender"]),
                float(form_data["bmi"]),
                int(form_data["smoking"]),
                int(form_data["genetic_risk"]),
                float(form_data["physical_activity"]),
                float(form_data["alcohol_intake"]),
                int(form_data["cancer_history"]),
                result["prediction"],
                result["diagnosis"],
                result["confidence_raw"],
            ),
        )


def get_predictions_for_user(user_id, limit=50):
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM predictions
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (user_id, limit),
        ).fetchall()
        return [dict(row) for row in rows]


def get_prediction_count(user_id):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT COUNT(*) AS count FROM predictions WHERE user_id = ?",
            (user_id,),
        ).fetchone()
        return row["count"] if row else 0
