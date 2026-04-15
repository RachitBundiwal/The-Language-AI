"""Administrative routes: database export, reset."""
from __future__ import annotations

import os
from datetime import datetime

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])

_DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sprechen.db"
)


@router.get("/export")
async def export_database() -> FileResponse:
    if not os.path.isfile(_DB_PATH):
        raise HTTPException(status_code=404, detail="Database file not found")
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return FileResponse(
        _DB_PATH,
        media_type="application/octet-stream",
        filename=f"sprechen_{stamp}.db",
    )
