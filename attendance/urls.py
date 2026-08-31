from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),

    # Separate management section
    path("manage/", views.management, name="management"),
    path("manage/staff/", views.staff_list, name="staff_list"),
    path("manage/staff/add/", views.add_staff, name="add_staff"),
    path("manage/departments/", views.department_list, name="department_list"),
    path("manage/departments/add/", views.add_department, name="add_department"),
    path("manage/courses/", views.course_list, name="course_list_all"),
    path("manage/courses/add/", views.add_course, name="add_course"),
    path("manage/courses/<int:department_id>/", views.course_list, name="course_list"),
    path("manage/courses/<int:course_id>/semesters/add/", views.add_semester, name="add_semester"),
    path("manage/semesters/<int:semester_id>/subjects/add/", views.add_subject, name="add_subject"),

    # Academic navigation
    path("courses/<int:course_id>/semesters/", views.semester_list, name="semester_list"),
    path("semesters/<int:semester_id>/subjects/", views.subject_list, name="subject_list"),

    # Students
    path("students/", views.student_list, name="student_list_all"),
    path("students/enroll/", views.enroll_student, name="enroll_student"),
    path("students/<int:student_id>/promote/", views.promote_student, name="promote_student"),
    path("students/<int:student_id>/demote/", views.demote_student, name="demote_student"),
    path("students/<int:student_id>/passout/", views.passout_student, name="passout_student"),

    # Attendance
    path("subjects/<int:subject_id>/attendance/", views.attendance_register, name="attendance_register"),
    path("subjects/<int:subject_id>/attendance/mark/", views.mark_attendance, name="mark_attendance"),
    path("attendance/export/", views.export_attendance, name="export_attendance"),
    path("attendance/reports/", views.attendance_report, name="attendance_report"),
]
