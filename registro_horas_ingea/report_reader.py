from __future__ import annotations

from datetime import datetime, timedelta, date
from pathlib import Path
from typing import Dict, List, Optional

import openpyxl

REPORT_HEADERS = [
    "Subproyecto",
    "Fecha",
    "Horas",
    "Tipo",
    "Etapa",
    "Area",
    "Lugar Trabajo",
    "ID Tarea (Planner/Jira)",
    "Comentario",
]


def get_previous_week_range(today: Optional[date] = None) -> tuple[date, date]:
    if today is None:
        today = datetime.now().date()
    start_date = today - timedelta(days=today.weekday() + 7)
    end_date = start_date + timedelta(days=6)
    return start_date, end_date


def get_previous_week_report_path(report_dir: Optional[Path] = None) -> Path:
    if report_dir is None:
        report_dir = Path(__file__).resolve().parent.parent / "reporte_excel" / "reportes"
    start_date, end_date = get_previous_week_range()
    filename = f"reporte_horas_{start_date.strftime('%Y%m%d')}_to_{end_date.strftime('%Y%m%d')}.xlsx"
    return report_dir / filename


def _normalize_date(value) -> str:
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, str):
        for fmt in ("%m/%d/%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(value.strip(), fmt).date().isoformat()
            except ValueError:
                continue
    raise ValueError(f"Unsupported date value: {value}")


def _format_hours(value) -> str:
    if value is None:
        return "0"
    if isinstance(value, (int, float)):
        return f"{value:g}"
    return str(value).strip()


def load_report_rows(report_path: Path) -> List[Dict[str, str]]:
    if not report_path.exists():
        raise FileNotFoundError(f"Report not found: {report_path}")

    workbook = openpyxl.load_workbook(report_path, data_only=True)
    sheet = workbook.active

    header_row = [cell.value for cell in sheet[1]]
    header_to_index = {name: idx for idx, name in enumerate(header_row) if name}

    missing = [name for name in REPORT_HEADERS if name not in header_to_index]
    if missing:
        raise ValueError(f"Missing headers: {', '.join(missing)}")

    rows: List[Dict[str, str]] = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        if not any(row):
            continue
        row_data = {name: row[header_to_index[name]] for name in REPORT_HEADERS}
        normalized = {
            "Fecha": _normalize_date(row_data["Fecha"]),
            "Horas": _format_hours(row_data["Horas"]),
            "Tipo": str(row_data["Tipo"]).strip() if row_data["Tipo"] else "",
            "Etapa": str(row_data["Etapa"]).strip() if row_data["Etapa"] else "",
            "Area": str(row_data["Area"]).strip() if row_data["Area"] else "",
            "Lugar Trabajo": str(row_data["Lugar Trabajo"]).strip() if row_data["Lugar Trabajo"] else "",
            "ID Tarea (Planner/Jira)": str(row_data["ID Tarea (Planner/Jira)"]).strip()
            if row_data["ID Tarea (Planner/Jira)"]
            else "",
            "Comentario": str(row_data["Comentario"]).strip() if row_data["Comentario"] else "",
        }
        rows.append(normalized)

    return rows
