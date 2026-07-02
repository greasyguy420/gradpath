# gradpath

## Project Description

gradpath is a course demand planning prototype that uses fake student records, degree requirements, prerequisites, and course offering data to estimate future course demand.

the goal is to help show how many students may need selected theatre courses in future semesters and which students may need priority access to stay on track for graduation.

this project uses fictional data only. it does not use real student records.

## Team Members

* sneha lama
* christopher pyfrom
* joshua smith

## Problem

departments cannot always offer every course every semester. some required courses are offered often, while upper-level or concentration-specific courses may be offered less often.

this can become a problem when students need a course to graduate on time, but the department does not have a quick way to estimate future demand.

common methods include:

1. checking previous enrollment numbers
2. reviewing student degree audits manually

previous enrollment numbers may not show future need accurately. manual review may be more accurate, but it takes too much time.

gradpath tries to make this easier by using fake student data and course rules to estimate course demand.

## What the Project Does

gradpath will:

1. load fake student data
2. load fake completed-course records
3. load fake degree requirements
4. load fake prerequisite rules
5. load fake course offering data
6. compare completed courses with required courses
7. identify missing required courses
8. check whether prerequisites are complete
9. estimate when each course may be needed
10. create a course demand report
11. create anonymized student priority groups

## Planned Stack

| part               | tool                |
| ------------------ | ------------------- |
| language           | python              |
| data format        | csv                 |
| data processing    | pandas              |
| logic              | rule-based planning |
| reports            | csv output          |
| optional dashboard | streamlit           |
| optional charts    | matplotlib          |

## Project Architecture

```text
fake csv data
      |
      v
data loading
      |
      v
data cleaning
      |
      v
requirement matching
      |
      v
prerequisite checking
      |
      v
course need estimation
      |
      v
demand aggregation
      |
      v
reports or dashboard
```

## Folder Structure

```text
gradpath/
│
├── data/
│   ├── students.csv
│   ├── student_courses.csv
│   ├── degree_requirements.csv
│   ├── prerequisites.csv
│   └── course_offerings.csv
│
├── src/
│   ├── load_data.py
│   ├── planner.py
│   ├── demand_report.py
│   └── utils.py
│
├── outputs/
│   ├── course_demand_report.csv
│   └── priority_students.csv
│
├── app.py
├── requirements.txt
├── README.md
└── PLANNING.md
```

## Data Files

### students.csv

stores fake student information.

expected columns:

```csv
student_id,major,concentration,expected_grad_term
```

### student_courses.csv

stores fake completed courses for each student.

expected columns:

```csv
student_id,course_code,semester_taken
```

### degree_requirements.csv

stores required courses by concentration.

expected columns:

```csv
concentration,course_code,requirement_type
```

### prerequisites.csv

stores course prerequisite rules.

expected columns:

```csv
course_code,prerequisite_course
```

### course_offerings.csv

stores when courses are normally offered.

expected columns:

```csv
course_code,offered_terms
```

## How the Logic Works

for each student, the system will:

1. find the student’s concentration
2. find the courses required for that concentration
3. find the courses the student already completed
4. compare completed courses with required courses
5. identify missing courses
6. check whether prerequisites are complete
7. estimate when each course may be needed
8. assign a priority level if needed

example:

```text
student S001 completed:
THE 1000
THE 2000
THE 3100

performance requirements:
THE 1000
THE 2000
THE 3100
THE 4200

missing course:
THE 4200

THE 4200 requires THE 3100.
S001 completed THE 3100.
S001 may need THE 4200 within 1 semester.
priority: high
```

## Need Categories

| condition                                                  | category               |
| ---------------------------------------------------------- | ---------------------- |
| missing course and prerequisites are complete              | needed in 1 semester   |
| missing course and one prerequisite is missing             | needed in 2 semesters  |
| missing course and multiple prerequisite steps are missing | needed in 3 semesters  |
| course is needed later or unclear                          | needed in 4+ semesters |

## Priority Levels

| priority | meaning                                                       |
| -------- | ------------------------------------------------------------- |
| high     | course is required soon and prerequisites are complete        |
| medium   | course is required but another course must be completed first |
| low      | course is needed later                                        |

## Expected Outputs

### course_demand_report.csv

this report shows how many students may need each course.

example columns:

```csv
course_code,needed_1_semester,needed_2_semesters,needed_3_semesters,needed_4_plus_semesters,total_demand
```

### priority_students.csv

this report shows anonymized students who may need priority.

example columns:

```csv
student_id,course_code,priority,reason
```

## How to Run the Project

### 1. Clone the Repository

```bash
git clone <repository-url>
cd gradpath
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

on windows:

```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Main Report Script

```bash
python src/demand_report.py
```

### 5. Check the Output Files

the generated reports should appear inside the `outputs/` folder.

```text
outputs/course_demand_report.csv
outputs/priority_students.csv
```

## Optional Dashboard

if the streamlit dashboard is added, run:

```bash
streamlit run app.py
```

the dashboard may show:

1. course demand summary
2. student priority groups
3. filter by course
4. filter by concentration
5. chart of demand by course

## Project Scope

this project will focus on:

1. fake theatre student data
2. selected required theatre courses
3. prerequisite checking
4. estimated course need categories
5. course demand reports
6. anonymized priority groups

this project will not:

1. use real student data
2. replace degreeworks
3. replace academic advisors
4. register students
5. create full student schedules
6. assign instructors
7. assign classrooms
8. predict grades

## Current Status

planned features:

* [ ] create fake csv data
* [ ] load data with pandas
* [ ] clean course codes and records
* [ ] match students to degree requirements
* [ ] identify missing courses
* [ ] check prerequisites
* [ ] estimate course need categories
* [ ] generate course demand report
* [ ] generate priority student report
* [ ] add optional streamlit dashboard

## Final Goal

the final goal is to create a working prototype that shows how course history, degree requirements, prerequisites, and course offering data can be used to estimate future course demand.

gradpath is meant to support department planning by producing clear course demand counts and student priority groups from fake data.
