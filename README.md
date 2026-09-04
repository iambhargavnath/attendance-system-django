# Attendance Management System

A Django-based web application for managing student attendance.

## Tech Stack

* Python
* Django
* SQLite
* Bootstrap 5
* django-crispy-forms

## Project Structure

```text
.
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── attendance/
│   ├── models/
│   ├── views/
│   ├── migrations/
│   ├── templates/

Django-based attendance management system for managing departments, courses, semesters, subjects, students, staff, and attendance.

## Requirements

* Python 3.12+
* Django 6.1
* SQLite (default) or another supported database

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Create sample data:

```bash
python manage.py seed_data
```

Start the server:

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Sample Login

### Admin

```text
Username: admin
Password: Admin123!
```

### Staff

```text
Username: bhargav.nath
Password: ChangeMe123!
```

The sample passwords should be changed before production use.

## How It Works

Academic hierarchy:

```text
Department
    ↓
Course
    ↓
Semester
    ↓
Subject
    ↓
Attendance
```

Students belong to a course and progress through semesters using enrollments.

```text
Student
    ↓
Course
    ↓
Enrollment
    ↓
Semester 1 → Semester 2 → Semester 3 → ...
```

## Main Sections

### Dashboard

Navigate through:

```text
Department → Course → Semester → Subject → Attendance
```

Courses can also be searched directly from the dashboard.

### Student Registry

Staff can:

* Enroll students
* Search students
* Filter by department/course/semester/status
* Promote students
* Demote students
* Mark students as passed out

### Attendance

From a subject:

```text
Subject
    ↓
Attendance
    ↓
Take Attendance
```

Select:

* Attendance date
* Staff member
* Present/Absent for each student

Attendance history can be filtered by:

* Date
* Student
* Status

### Attendance Reports

The report section supports:

* Department
* Course
* Semester
* Subject
* Date
* Student
* Status

Filtered attendance can be exported to CSV.

## Adding / Modifying Data

### Add Department

Admin:

```text
Management → Departments → Add Department
```

### Add Course

Admin:

```text
Department → Add Course
```

### Add Semester

Admin:

```text
Course → Add Semester
```

### Add Subject

Admin:

```text
Semester → Add Subject
```

### Add Staff

Admin:

```text
Management → Staff → Add Staff
```

### Enroll Student

Staff:

```text
Student Registry → Enroll Student
```

A new student automatically starts from the first semester of the selected course.

## Modifying the Application

### Models

Academic models:

```text
attendance/models/academic.py
```

Contains:

```text
Department
Course
Semester
Subject
```

Student-related models:

```text
attendance/models/student.py
```

Contains:

```text
Student
Enrollment
```

Attendance model:

```text
attendance/models/attendance.py
```

### Views

Views are separated by responsibility:

```text
attendance/views/dashboard.py
attendance/views/management.py
attendance/views/academic.py
attendance/views/students.py
attendance/views/attendance.py
```

Add or modify functionality in the appropriate file instead of putting everything into one `views.py`.

### Forms

Forms are located in:

```text
attendance/forms.py
```

Use this file when changing:

* Form fields
* Validation
* Staff creation
* Student enrollment
* Academic forms
* Attendance forms

### Templates

Application templates:

```text
attendance/templates/attendance/
```

Global templates:

```text
templates/
```

Bootstrap is used for the UI and django-crispy-forms is used for form rendering.

## Project Structure

```text
nielit_attendance_system/
│
├── manage.py
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── attendance/
│   │
│   ├── migrations/
│   │
│   ├── management/
│   │   └── commands/
│   │       └── seed_data.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── academic.py
│   │   ├── student.py
│   │   └── attendance.py
│   │
│   ├── views/
│   │   ├── __init__.py
│   │   ├── dashboard.py
│   │   ├── management.py
│   │   ├── academic.py
│   │   ├── students.py
│   │   └── attendance.py
│   │
│   ├── templates/
│   │   └── attendance/
│   │       ├── dashboard.html
│   │       ├── management.html
│   │       ├── student_list.html
│   │       ├── department_list.html
│   │       ├── course_list.html
│   │       ├── semester_list.html
│   │       ├── subject_list.html
│   │       ├── register.html
│   │       ├── mark_attendance.html
│   │       └── report.html
│   │
│   ├── forms.py
│   ├── urls.py
│   └── ...
│
├── templates/
│   ├── base.html
│   └── home.html
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Useful Commands

Check the project:

```bash
python manage.py check
```

Create migrations:

```bash
python manage.py makemigrations
```

Apply migrations:

```bash
python manage.py migrate
```

Create a superuser:

```bash
python manage.py createsuperuser
```

Seed sample data:

```bash
python manage.py seed_data
```

Run the server:

```bash
python manage.py runserver
```

## Database Changes

After modifying models:

```bash
python manage.py makemigrations
python manage.py migrate
```

For production, configure the database and secrets in:

```text
config/settings.py
```

Do not commit passwords, secret keys, or production database credentials to Git.

```

## Setup

### 1. Clone the project

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Create virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows**

```bash
.venv\Scripts\activate
```

**macOS/Linux**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

Create `.env` in the project root:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

Generate a secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create admin user

```bash
python manage.py createsuperuser
```

### 7. Start the server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

Admin:

```text
http://127.0.0.1:8000/admin/
```

## Common Commands

```bash
# Run server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test

# Check project
python manage.py check
```

## Environment Variables

| Variable          | Description               |
| ----------------- | ------------------------- |
| `SECRET_KEY`    | Django secret key         |
| `DEBUG`         | Enable/disable debug mode |
| `ALLOWED_HOSTS` | Allowed hostnames         |

> Never commit `.env` to Git. Use `.env.example` as a template.

## License

Copyright © 2026 Bhargav Nath.

This project is provided for educational purposes only.

You are free to view, study, and use the code for learning and educational purposes. Please do not claim the project or its code as your own.

For any other use, please contact the author for permission.
