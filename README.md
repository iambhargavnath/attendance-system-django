# NIELIT Attendance Management System

A Django-based attendance management system for managing courses, semesters, subjects, students, staff, and attendance.

## Academic Structure

```text
Course
  └── Semester
       └── Subject
            └── Attendance
```

Departments are not used. **Course is the top-level academic entity.**

## Features

- Staff authentication and management
- Course management
- Semester management
- Subject management
- Student enrollment
- Student promotion and demotion
- Student status: Active, Passed Out, Dropped
- Subject-wise attendance
- Attendance history and filtering
- CSV attendance export
- Django admin

## Setup

```bash
git clone <repository-url>
cd attendance-system-django

python -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Sample Accounts

The seed command creates:

- Admin: `admin` / `Admin123!`
- Staff: `bhargav.nath` / `ChangeMe123!`
- Staff: `anupam.sarma` / `ChangeMe123!`
- Staff: `priyanka.das` / `ChangeMe123!`

Change these passwords before production use.

## Development Branch

```bash
git checkout -b dev
git add .
git commit -m "Remove department and use course as top-level entity"
git push -u origin dev
```

## Migration

For an existing installation, run:

```bash
python manage.py migrate
```

Migration `0005_remove_department` removes the Department model and the Course → Department relationship while keeping existing Course records.

## Management Flow

1. Create a Course.
2. Add Semesters to the Course.
3. Add Subjects to each Semester.
4. Enroll Students in a Course.
5. Students automatically start in the first Semester.
6. Take attendance for each Subject.
7. Review or export attendance reports.
