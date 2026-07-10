# builds student-level graduation summary reports from readiness status data.

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_READINESS_PATH = PROJECT_ROOT / "data" / "intermediate" / "student_readiness_status.csv"
DEFAULT_OUTPUT_PATH = PROJECT_ROOT / "outputs" / "student_graduation_summary.csv"

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


def load_readiness_status(path=None):
    path = Path(path) if path else DEFAULT_READINESS_PATH
    return pd.read_csv(path)


def get_graduation_status(missing_requirements):
    if missing_requirements == 0:
        return "ready or nearly complete"
    if missing_requirements <= 2:
        return "close"
    if missing_requirements <= 5:
        return "moderate remaining"
    return "needs planning"


def build_student_graduation_summary(readiness_df):
    rows = []

    # group by student so each output row represents one student.
    for student_id, student_rows in readiness_df.groupby("student_id", sort=False):
        first_row = student_rows.iloc[0]
        total_requirements = len(student_rows)
        complete_requirements = _count_status(student_rows, "complete")
        in_progress_requirements = _count_status(student_rows, "in_progress")
        ready_missing_requirements = _count_status(student_rows, "missing_ready")
        blocked_missing_requirements = _count_status(student_rows, "missing_blocked")
        missing_requirements = ready_missing_requirements + blocked_missing_requirements

        rows.append(
            {
                "student_id": student_id,
                "student_name": first_row.get("student_name", ""),
                "degree": first_row.get("degree", ""),
                "concentration": first_row.get("concentration", ""),
                "class_year": first_row.get("class_year", ""),
                "usf_earned_hours": first_row.get("usf_earned_hours", ""),
                "overall_earned_hours": first_row.get("overall_earned_hours", ""),
                "gpa": first_row.get("gpa", ""),
                "total_requirements": total_requirements,
                "complete_requirements": complete_requirements,
                "in_progress_requirements": in_progress_requirements,
                "ready_missing_requirements": ready_missing_requirements,
                "blocked_missing_requirements": blocked_missing_requirements,
                "missing_requirements": missing_requirements,
                "completion_percent": _completion_percent(
                    complete_requirements, total_requirements
                ),
                "graduation_status": get_graduation_status(missing_requirements),
            }
        )

    return pd.DataFrame(rows, columns=OUTPUT_COLUMNS)


def save_student_graduation_summary(readiness_path=None, output_path=None):
    output_path = Path(output_path) if output_path else DEFAULT_OUTPUT_PATH
    readiness_df = load_readiness_status(readiness_path)
    summary_df = build_student_graduation_summary(readiness_df)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    summary_df.to_csv(output_path, index=False)
    return output_path, len(summary_df)


# keep repeated status counting readable inside the student loop.
def _count_status(student_rows, status):
    return int((student_rows["need_status"] == status).sum())


def _completion_percent(complete_requirements, total_requirements):
    if total_requirements == 0:
        return 0.0
    return round(complete_requirements / total_requirements * 100, 2)


if __name__ == "__main__":
    saved_path, row_count = save_student_graduation_summary()
    print(saved_path)
    print(f"rows written: {row_count}")