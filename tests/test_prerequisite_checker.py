# tests readiness conversion from intermediate tap data into a long student status file.

import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.prerequisite_checker import (
    build_student_readiness_status,
    get_semester_bucket,
    normalize_status,
)


OUTPUT_COLUMNS = [
    "student_id",
    "student_name",
    "term",
    "class_year",
    "admit_term",
    "student_type",
    "usf_earned_hours",
    "overall_earned_hours",
    "gpa",
    "degree",
    "concentration",
    "requirement",
    "status_code",
    "need_status",
    "distance",
    "semester_bucket",
    "prereq_ready",
    "missing_prerequisites",
    "readiness_reason",
]


def test_normalize_status_maps_codes_to_labels():
    assert normalize_status("c") == "complete"
    assert normalize_status("ip") == "in_progress"
    assert normalize_status("r") == "missing_ready"
    assert normalize_status("n") == "missing_blocked"


def test_get_semester_bucket_maps_distance_values():
    assert get_semester_bucket("1/4") == "needed_1_semester"
    assert get_semester_bucket("2/4") == "needed_2_semesters"
    assert get_semester_bucket("3/4") == "needed_3_semesters"
    assert get_semester_bucket("4/4") == "needed_4_plus_semesters"
    assert get_semester_bucket("9") == "needed_4_plus_semesters"


def test_build_student_readiness_status_creates_one_row_per_student_per_requirement():
    intermediate_df = pd.DataFrame(
        [
            {
                "Term": 202608,
                "Last Name": "One",
                "First Name": "Student",
                "UID": "U1",
                "Class": 1,
                "Admit Term": 202608,
                "Stu Type": "B",
                "USF Earned Hours": 0,
                "Overall Earned Hours": 6,
                "USF GPA": 3.1,
                "Theatre Major": "TAR",
                "Theatre Conc": "TAP",
                "Script Analysis": "r",
                "Script Analysis Dist": "1/4",
                "Acting II": "n",
                "Acting II Dist": "2/4",
            },
            {
                "Term": 202608,
                "Last Name": "Two",
                "First Name": "Student",
                "UID": "U2",
                "Class": 2,
                "Admit Term": 202508,
                "Stu Type": "J",
                "USF Earned Hours": 30,
                "Overall Earned Hours": 45,
                "USF GPA": 3.5,
                "Theatre Major": "TAR",
                "Theatre Conc": "TAP",
                "Script Analysis": "c",
                "Script Analysis Dist": "0",
                "Acting II": "ip",
                "Acting II Dist": "0",
            },
        ]
    )

    result = build_student_readiness_status(intermediate_df)

    assert len(result) == 4
    assert list(result.columns) == OUTPUT_COLUMNS
    assert set(result["requirement"]) == {"Script Analysis", "Acting II"}
    assert not result["requirement"].str.endswith("Dist").any()


def test_build_student_readiness_status_sets_readiness_fields():
    intermediate_df = pd.DataFrame(
        [
            {
                "Term": 202608,
                "Last Name": "Blocked",
                "First Name": "Student",
                "UID": "U3",
                "Class": 3,
                "Admit Term": 202408,
                "Stu Type": "B",
                "USF Earned Hours": 63,
                "Overall Earned Hours": 66,
                "USF GPA": 3.2,
                "Theatre Major": "TAR",
                "Theatre Conc": "TAP",
                "Performance Electives": "n",
                "Performance Electives Dist": "9",
            }
        ]
    )

    result = build_student_readiness_status(intermediate_df)
    row = result.iloc[0]

    assert row["student_id"] == "U3"
    assert row["student_name"] == "Student Blocked"
    assert row["status_code"] == "n"
    assert row["need_status"] == "missing_blocked"
    assert row["distance"] == "9"
    assert row["semester_bucket"] == "needed_4_plus_semesters"
    assert row["prereq_ready"] == "no"
    assert row["missing_prerequisites"] == "unknown prerequisite or earlier requirement"
