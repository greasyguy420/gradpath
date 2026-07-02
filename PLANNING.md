# GradPath planningdocument

## project name

**gradpath: predicting student course needs**

## description

gradpath is a course planing prototype that uses fake student records, degree requirements, prerequisites, and course offering data to estimate future course demand and identify students who may need priority access to required courses.

## project goal

the goal of this project is to build a small working prototype that helps estimate which theatre courses students may need in future semesters.

this project is not meant to replace degreeworks, advisors, or department scheduling decisions. it is only meant to create a simple planning report based on fake student data and course requirement rules.

## main problem

departments cannot always offer every course every semester. some courses have enough enrollment to be offered often, while upper-level or concentration-specific courses may be offered less often.

this can create a problem when students need a required course to stay on track for graduation, but the department does not have a fast way to estimate future demand.

right now, course need can be estimated by:

1. looking at previous enrollment numbers
2. reviewing each student’s degreeworks audit manually

previous enrollment numbers are easy to check, but they may not show true future need. manual review can be more accurate, but it takes too much time.

gradpath will try to make this process easier by using fake student records and course requirement data to estimate course demand.

## what we are building

we are building a python-based course demand planning prototype.

the system will:

1. load fake student data
2. load fake completed-course records
3. load fake degree requirement data
4. load fake prerequisite rules
5. load fake course offering information
6. compare completed courses with required courses
7. find missing required courses
8. check whether prerequisites are complete
9. estimate when each course may be needed
10. combine the results into a course demand report
11. create anonymized student priority groups

## what we are not building

gradpath will not:

1. register students for courses
2. create complete student schedules
3. assign instructors
4. assign classrooms
5. predict student grades
6. replace academic advisors
7. replace degreeworks
8. use real student data
9. handle login or user accounts
10. build a full university scheduling system

## planned stack

| area                 | tool                |
| -------------------- | ------------------- |
| programming language | python              |
| data format          | csv                 |
| data processing      | pandas              |
| planning logic       | rule based planning |
| reports              | csv output          |
| optional dashboard   | streamlit           |
| optional charts      | matplotlib          |
| version control      | github              |

## why this stack

python is a good choice because it is simple for data processing and easy to explain for this project.

csv files are enough because we are using fake data. we do not need a database for the first version.

pandas will help us load, clean, filter, and group the data.

rule-based planning makes more sense than starting with machine learning because the dataset is fake and small. the rules are also easier to explain and debug.

streamlit can be added later if we want a simple dashboard.

## project architecture

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
reports or optional dashboard
```

## data files

the project will use fake csv files inside the `data/` folder.

### 1. students.csv

stores fake student information.

expected columns:

```csv
student_id,major,concentration,expected_grad_term
```

example:

```csv
S001,Theatre,Performance,Fall 2026
S002,Theatre,Design,Spring 2027
S003,Theatre,General,Fall 2027
```

### 2. student_courses.csv

stores fake completed courses for each student.

expected columns:

```csv
student_id,course_code,semester_taken
```

example:

```csv
S001,THE 1000,Fall 2024
S001,THE 2000,Spring 2025
S001,THE 3100,Fall 2025
```

### 3. degree_requirements.csv

stores required courses by concentration.

expected columns:

```csv
concentration,course_code,requirement_type
```

example:

```csv
Performance,THE 1000,core
Performance,THE 2000,core
Performance,THE 3100,upper_level
Performance,THE 4200,upper_level
```

### 4. prerequisites.csv

stores prerequisite rules.

expected columns:

```csv
course_code,prerequisite_course
```

example:

```csv
THE 3100,THE 2000
THE 4200,THE 3100
```

### 5. course_offerings.csv

stores when courses are normally offered.

expected columns:

```csv
course_code,offered_terms
```

example:

```csv
THE 1000,Fall;Spring
THE 2000,Spring
THE 3100,Fall
THE 4200,Spring
```

## suggested folder structure

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

## core logic

### step 1: load data

the system reads all fake csv files.

input files:

```text
students.csv
student_courses.csv
degree_requirements.csv
prerequisites.csv
course_offerings.csv
```

### step 2: clean data

the system standardizes the data before using it.

cleaning checks:

1. remove duplicate rows
2. make course codes consistent
3. make concentration names consistent
4. check for missing student ids
5. check for missing course codes

example:

```text
THE3100
THE-3100
THE 3100
```

all should become:

```text
THE 3100
```

### step 3: find completed courses

for each student, the system finds the courses they already completed.

example:

```text
S001 completed:
THE 1000
THE 2000
THE 3100
```

### step 4: find required courses

the system checks the student’s concentration and finds the courses required for that concentration.

example:

```text
performance requirements:
THE 1000
THE 2000
THE 3100
THE 4200
```

### step 5: find missing courses

the system compares completed courses with required courses.

example:

```text
completed:
THE 1000
THE 2000
THE 3100

required:
THE 1000
THE 2000
THE 3100
THE 4200

missing:
THE 4200
```

### step 6: check prerequisites

the system checks whether the student completed the prerequisites for each missing course.

example:

```text
THE 4200 requires THE 3100.
S001 completed THE 3100.
S001 is eligible for THE 4200.
```

### step 7: estimate course need

the system places each missing course into a need category.

suggested rule:

| condition                                                  | need category          |
| ---------------------------------------------------------- | ---------------------- |
| missing course and prerequisites are complete              | needed in 1 semester   |
| missing course and one prerequisite is missing             | needed in 2 semesters  |
| missing course and multiple prerequisite steps are missing | needed in 3 semesters  |
| course is needed later or unclear                          | needed in 4+ semesters |

### step 8: assign priority

the system assigns a priority group to each student and course.

suggested rule:

| priority | meaning                                                       |
| -------- | ------------------------------------------------------------- |
| high     | course is required soon and prerequisites are complete        |
| medium   | course is required but another course must be completed first |
| low      | course is needed later                                        |

example:

```text
S001 needs THE 4200.
prerequisites are complete.
THE 4200 is required.
priority: high
```

### step 9: aggregate course demand

the system counts how many students need each course in each future-semester category.

example output:

```csv
course_code,needed_1_semester,needed_2_semesters,needed_3_semesters,needed_4_plus_semesters,total_demand
THE 4200,8,4,1,0,13
THE 3100,5,7,2,1,15
```

### step 10: generate reports

the system exports two main reports.

#### course_demand_report.csv

shows total course demand.

expected columns:

```csv
course_code,needed_1_semester,needed_2_semesters,needed_3_semesters,needed_4_plus_semesters,total_demand
```

#### priority_students.csv

shows anonymized students who may need priority.

expected columns:

```csv
student_id,course_code,priority,reason
```

example:

```csv
S001,THE 4200,High,Prerequisites complete and course is required
S002,THE 4400,Medium,Required course but prerequisite is missing
```

## optional streamlit dashboard later

if time allows, the group may add a simple streamlit dashboard.

the dashboard may show:

1. course demand report
2. priority student report
3. filter by course
4. filter by concentration
5. bar chart of demand by course

dashboard layout:

```text
gradpath dashboard

course demand summary
[table]

priority students
[table]

demand by course
[bar chart]
```

## development phases

### phase 1: setup

tasks:

1. create the github repository
2. create the project folders
3. create fake csv data
4. create `requirements.txt`
5. create the first version of `README.md`

goal:

the project should have a clean structure and fake data ready to use.

### phase 2: data loading

tasks:

1. read all csv files using pandas
2. print sample rows from each file
3. check that columns are loaded correctly
4. add basic error handling for missing files or missing columns

goal:

the system should successfully load all fake data.

### phase 3: requirement matching

tasks:

1. group completed courses by student
2. match each student to their concentration requirements
3. identify missing required courses

goal:

the system should know which courses each student still needs.

### phase 4: prerequisite checking

tasks:

1. read prerequisite rules
2. check whether each missing course has prerequisites
3. check whether the student completed those prerequisites
4. mark courses as eligible or blocked

goal:

the system should know whether each missing course can be taken soon.

### phase 5: course need estimation

tasks:

1. create rules for semester need categories
2. apply those rules to each student and missing course
3. label each course as needed in one, two, three, or four or more semesters

goal:

the system should estimate when each student may need each course.

### phase 6: report generation

tasks:

1. count demand by course
2. count demand by semester category
3. create priority student groups
4. export final csv reports

goal:

the system should produce useful output files.

### phase 7: optional dashboard

tasks:

1. create a streamlit app
2. display the course demand report
3. display the priority student report
4. add simple filters or charts

goal:

the project should have a simple visual demo.

## team roles

these can be adjusted later may be.

| team member        | possible role                                    |
| ------------------ | ------------------------------------------------ |
| sneha lama         | data structure, planning logic, documentation    |
| christopher pyfrom | fake data creation, requirement mapping, testing |
| joshua smith       | reports, dashboard, final presentation support   |

## minimum working version

the minimum version should include:

1. fake data files
2. python code that loads the data
3. logic that finds missing requirements
4. logic that checks prerequisites
5. logic that estimates course need categories
6. a course demand report
7. a priority student report
8. a README explaining how the project works

## later stretch features

if time allows,wecan add:

1. streamlit dashboard
2. bar chart for demand by course
3. filter by concentration
4. more fake students
5. more realistic prerequisite chains
6. simple backtesting using older fake semesters
7. summary explanation for each priority student

## risks and limits

| risk                                                | how we will handle it                                                |
| --------------------------------------------------- | -------------------------------------------------------------------- |
| fake data may not represent real students perfectly | we will clearly state that the data is fictional                     |
| course rules may be simplified                      | we will limit the project to selected theatre courses                |
| the model may not be true machine learning          | we will frame it as rule-based planning and course demand estimation |
| scope may become too large                          | we will avoid full scheduling, registration, and grade prediction    |
| requirements may vary by catalog year               | we may use one simplified requirement set for the prototype          |

## final demo plan

the final demo should show:

1. the fake data files
2. the project architecture
3. how the system loads the data
4. how missing courses are identified
5. how prerequisites are checked
6. how course need categories are assigned
7. the final course demand report
8. the priority student report
9. optional dashboard if completed

## success criteria

the project is successful if it can:

1. use fake student records
2. identify missing required courses
3. check prerequisites
4. estimate future course need categories
5. count demand by course
6. produce readable reports
7. explain why students are placed into priority groups

## final project summary

gradpath is a small course demand planning prototype. it uses fake student records, degree requirements, prerequisites, and course offering data to estimate when students may need required theatre courses. the system produces course demand counts and anonymized student priority groups to support future course planning.
