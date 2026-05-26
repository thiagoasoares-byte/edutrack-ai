"""
Helper to calculate overdue subject IDs for a given user.

Usage:
  python script/calculate_overdue_subjects.py --db sqlite:///data.db --user-id 123

This script is intentionally decoupled: it accepts a SQLAlchemy connection string and returns
a JSON array of subject IDs that have at least one overdue, not-completed task for the user.
"""
from __future__ import annotations
import os
import argparse
import json
from typing import List
from datetime import datetime

try:
    from sqlalchemy import create_engine, text
except Exception:
    create_engine = None


def get_overdue_subject_ids(db_url: str, user_id: int) -> List[int]:
    """Return distinct subject IDs with overdue tasks for user_id.

    Overdue = due_date < now AND completed = false
    """
    if create_engine is None:
        raise RuntimeError("sqlalchemy is required. Install with: pip install sqlalchemy")

    engine = create_engine(db_url)
    now_ts = datetime.utcnow()

    query = text(
        "SELECT DISTINCT subject_id FROM academic_tasks "
        "WHERE user_id = :user_id AND completed = 0 AND due_date < :now"
    )

    with engine.connect() as conn:
        rows = conn.execute(query, {"user_id": user_id, "now": now_ts}).fetchall()
    return [int(r[0]) for r in rows if r[0] is not None]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True, help="SQLAlchemy DB URL (eg sqlite:///data.db)")
    parser.add_argument("--user-id", required=True, type=int)
    args = parser.parse_args()

    ids = get_overdue_subject_ids(args.db, args.user_id)
    print(json.dumps(ids))


if __name__ == "__main__":
    main()
