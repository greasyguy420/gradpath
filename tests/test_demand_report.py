# tests student graduation summary totals from readiness status rows.

import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.demand_report import (
    build_student_graduation_summary,
    get_graduation_status,
)


OUTPUT_COLUMNS = [
    "student_id",
    "student_name",
    "degree",
    "concentration",
    "class_year",
    "usf_earned_hours",
    "overall_earned_hours",
    "gpa",
    "total_requirements",
    "complete_requirements",
    "in_progress_requirements",
    "ready_missing_requirements",
    "blocked_missing_requirements",
    "missing_requirements",
    "completion_percent",
    "graduation_status",
]


def test_get_graduation_status_maps_missing_counts():
    assert get_graduation_status(0) == "ready or nearly complete"
    assert get_graduation_status(2) == "close"
    assert get_graduation_status(5) == "moderate remaining"
    assert get_graduation_status(6) == "needs planning"


def test_build_student_graduation_summary_creates_one_row_per_student():
    readiness_df = pd.DataFrame(
        [
            _readiness_row("U1", "Student One", "complete"),
            _readiness_row("U1", "Student One", "in_progress"),
            _readiness_row("U1", "Student One", "missing_ready"),
            _readiness_row("U1", "Student One", "missing_blocked"),
            _readiness_row("U2", "Student Two", "complete", class_year=2),
            _readiness_row("U2", "Student Two", "complete", class_year=2),
        ]
    )

    result = build_student_graduation_summary(readiness_df)

    assert len(result) == 2
    assert list(result.columns) == OUTPUT_COLUMNS


def test_build_student_graduation_summary_calculates_totals():
    readiness_df = pd.DataFrame(
        [
            _readiness_row("U1", "Student One", "complete"),
            _readiness_row("U1", "Student One", "complete"),
            _readiness_row("U1", "Student One", "in_progress"),
            _readiness_row("U1", "Student One", "missing_ready"),
            _readiness_row("U1", "Student One", "missing_blocked"),
        ]
    )

    result = build_student_graduation_summary(readiness_df)
    row = result.iloc[0]

    assert row["total_requirements"] == 5
    assert row["complete_requirements"] == 2
    assert row["in_progress_requirements"] == 1
    assert row["ready_missing_requirements"] == 1
    assert row["blocked_missing_requirements"] == 1
    assert row["missing_requirements"] == 2
    assert row["completion_percent"] == 40.0
    assert row["graduation_status"] == "close"


# keep fixture rows tiny so the summary math is the thing under test.
def _readiness_row(student_id, student_name, need_status, class_year=1):
    return {
        "student_id": student_id,
        "student_name": student_name,
        "degree": "TAR",
        "concentration": "TAP",
        "class_year": class_year,
        "usf_earned_hours": 30,
        "overall_earned_hours": 45,
        "gpa": 3.4,
        "requirement": "Some Requirement",
        "need_status": need_status,
    }
