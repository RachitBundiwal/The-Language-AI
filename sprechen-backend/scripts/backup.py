"""Sprechen database backup.

Copies sprechen.db to ./backups/sprechen_{YYYYMMDD}.db and prunes backups
older than the 7 most recent.

Usage:    python scripts/backup.py
Crontab:  0 2 * * * cd /path/to/sprechen-backend && .venv/bin/python scripts/backup.py
"""
from __future__ import annotations

import os
import shutil
import sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT, "sprechen.db")
BACKUP_DIR = os.path.join(ROOT, "backups")
KEEP = 7


def main() -> int:
    if not os.path.isfile(DB_PATH):
        print(f"ERROR: database not found at {DB_PATH}")
        return 1

    os.makedirs(BACKUP_DIR, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d")
    dest = os.path.join(BACKUP_DIR, f"sprechen_{stamp}.db")
    shutil.copy2(DB_PATH, dest)

    # Prune — keep only the N most-recent sprechen_*.db files
    backups = sorted(
        (
            os.path.join(BACKUP_DIR, f)
            for f in os.listdir(BACKUP_DIR)
            if f.startswith("sprechen_") and f.endswith(".db")
        ),
        key=os.path.getmtime,
        reverse=True,
    )
    removed = 0
    for old in backups[KEEP:]:
        try:
            os.remove(old)
            removed += 1
        except OSError:
            pass

    size_mb = os.path.getsize(dest) / (1024 * 1024)
    print(f"Backup created: {os.path.basename(dest)} ({size_mb:.2f} MB)")
    print(f"Retained: {min(len(backups), KEEP)} / Pruned: {removed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
