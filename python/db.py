import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any

DB_PATH = Path("dqm.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS runs (
            run_id INTEGER PRIMARY KEY,
            mean REAL,
            stddev REAL,
            outlier_count INTEGER,
            status TEXT,
            processed_at TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def insert_run(
    run_id: int,
    mean: float,
    stddev: float,
    outlier_count: int,
    status: str,
    processed_at: str,
) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT OR REPLACE INTO runs (run_id, mean, stddev, outlier_count, status, processed_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (run_id, mean, stddev, outlier_count, status, processed_at),
    )
    conn.commit()
    conn.close()


def get_all_runs() -> List[Dict[str, Any]]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM runs ORDER BY run_id")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_latest_run() -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM runs ORDER BY run_id DESC LIMIT 1")
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def get_run(run_id: int) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM runs WHERE run_id = ?", (run_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None
