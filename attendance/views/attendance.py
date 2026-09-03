import csv
from datetime import date

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from ..forms import (
    AttendanceForm,
    AttendanceStatusForm,
)

from ..models import (
    Attendance,
    Student,
    Subject,
)


# ==================================================
# Attendance Register
# ==================================================

@staff_member_required
def attendance_register(request, subject_id):

    subject = get_object_or_404(
        Subject.objects.select_related(
            "semester__course__department"
        ),
        pk=subject_id,
    )

    semester = subject.semester

    # ---------------------------------------------
    # Filters
    # ---------------------------------------------

    selected_date = request.GET.get(
        "date",
        "",
    )

    selected_student = request.GET.get(
        "student",
        "",
    )

    selected_status = request.GET.get(
        "status",
        "",
    )

    # ---------------------------------------------
    # Students currently enrolled
    # in this semester
    # ---------------------------------------------

    students = (
        Student.objects
        .filter(
            course=semester.course,
            enrollment__semester=semester,
        )
        .distinct()
        .order_by("roll_number")
    )

    # ---------------------------------------------
    # Attendance records
    # ---------------------------------------------

    attendance_records = (
        Attendance.objects
        .filter(
            subject=subject
        )
        .select_related(
            "student",
            "taken_by",
        )
        .order_by(
            "-attendance_date",
            "student__roll_number",
        )
    )

    # ---------------------------------------------
    # Available dates
    # ---------------------------------------------

    attendance_dates = (
        Attendance.objects
        .filter(
            subject=subject
        )
        .values_list(
            "attendance_date",
            flat=True,
        )
        .distinct()
        .order_by(
            "-attendance_date"
        )
    )

    # ---------------------------------------------
    # Date filter
    # ---------------------------------------------

    if selected_date:

        attendance_records = (
            attendance_records.filter(
                attendance_date=selected_date
            )
        )

    # ---------------------------------------------
    # Student filter
    # ---------------------------------------------

    if selected_student:

        attendance_records = (
            attendance_records.filter(
                student_id=selected_student
            )
        )

    # ---------------------------------------------
    # Status filter
    # ---------------------------------------------

    if selected_status in [
        Attendance.PRESENT,
        Attendance.ABSENT,
    ]:

        attendance_records = (
            attendance_records.filter(
                status=selected_status
            )
        )

    records = list(
        attendance_records
    )

    # ---------------------------------------------
    # Display rows
    # ---------------------------------------------

    attendance_rows = []

    for record in records:

        staff_name = ""

        if record.taken_by:

            staff_name = (
                record.taken_by.get_full_name()
                or record.taken_by.username
            )

        attendance_rows.append({
            "student": record.student,
            "date": record.attendance_date,
            "status": record.status,
            "status_display": (
                record.get_status_display()
            ),
            "taken_by": staff_name,
        })

    # ---------------------------------------------
    # Selected date object
    # ---------------------------------------------

    selected_date_obj = None

    if selected_date:

        try:

            selected_date_obj = (
                date.fromisoformat(
                    selected_date
                )
            )

        except ValueError:

            selected_date_obj = None

    # ---------------------------------------------
    # Summary
    # ---------------------------------------------

    total_records = len(records)

    present_count = sum(
        1
        for record in records
        if record.status == Attendance.PRESENT
    )

    absent_count = sum(
        1
        for record in records
        if record.status == Attendance.ABSENT
    )

    return render(
        request,
        "attendance/register.html",
        {
            "subject": subject,

            "students": students,
            "attendance_dates": attendance_dates,

            "selected_date": selected_date,
            "selected_date_obj": selected_date_obj,
            "selected_student": selected_student,
            "selected_status": selected_status,

            "attendance_rows": attendance_rows,

            "total_records": total_records,
            "present_count": present_count,
            "absent_count": absent_count,
        },
    )


# ==================================================
# Mark Attendance
# ==================================================

@staff_member_required
def mark_attendance(request, subject_id):

    subject = get_object_or_404(
        Subject.objects.select_related(
            "semester__course"
        ),
        pk=subject_id,
    )

    students = list(
        Student.objects
        .filter(
            enrollment__semester=subject.semester
        )
        .distinct()
        .order_by("roll_number")
    )

    staff = (
        User.objects
        .filter(
            is_staff=True,
            is_active=True,
        )
        .order_by(
            "first_name",
            "username",
        )
    )

    selected_date = (
        request.GET.get("date")
        or request.POST.get(
            "attendance_date"
        )
        or str(date.today())
    )

    existing = Attendance.objects.filter(
        subject=subject,
        attendance_date=selected_date,
    )

    existing_status = {
        record.student_id: record.status
        for record in existing
    }

    initial = {
        "attendance_date": selected_date,
        "taken_by": request.user.pk,
    }

    session_form = AttendanceForm(
        request.POST or None,
        initial=(
            initial
            if request.method == "GET"
            else None
        ),
        staff_queryset=staff,
    )

    status_initial = {
        f"status_{student.pk}": existing_status.get(
            student.pk,
            Attendance.PRESENT,
        )
        for student in students
    }

    status_form = AttendanceStatusForm(
        students,
        request.POST or None,
        initial=status_initial,
    )

    if (
        request.method == "POST"
        and session_form.is_valid()
        and status_form.is_valid()
    ):

        attendance_date = (
            session_form.cleaned_data[
                "attendance_date"
            ]
        )

        taken_by = (
            session_form.cleaned_data[
                "taken_by"
            ]
        )

        with transaction.atomic():

            for student in students:

                Attendance.objects.update_or_create(
                    student=student,
                    subject=subject,
                    attendance_date=attendance_date,
                    defaults={
                        "status": (
                            status_form.cleaned_data[
                                f"status_{student.pk}"
                            ]
                        ),
                        "taken_by": taken_by,
                    },
                )

        messages.success(
            request,
            (
                f"Attendance saved for "
                f"{attendance_date}."
            ),
        )

        return redirect(
            "attendance_register",
            subject_id=subject.pk,
        )

    return render(
        request,
        "attendance/mark_attendance.html",
        {
            "subject": subject,
            "students": students,
            "session_form": session_form,
            "status_form": status_form,
            "selected_date": selected_date,
        },
    )


# ==================================================
# Export Attendance
# ==================================================

@staff_member_required
def export_attendance(request):

    # --------------------------------------------------
    # Filters
    # --------------------------------------------------

    department_id = request.GET.get(
        "department",
        "",
    )

    course_id = request.GET.get(
        "course",
        "",
    )

    semester_id = request.GET.get(
        "semester",
        "",
    )

    subject_id = request.GET.get(
        "subject",
        "",
    )

    attendance_date = request.GET.get(
        "date",
        "",
    )

    student_id = request.GET.get(
        "student",
        "",
    )

    status = request.GET.get(
        "status",
        "",
    )

    # --------------------------------------------------
    # Base queryset
    # --------------------------------------------------

    records = (
        Attendance.objects
        .select_related(
            "student",
            "student__course",
            "student__course__department",
            "subject",
            "subject__semester",
            "subject__semester__course",
            "subject__semester__course__department",
            "taken_by",
        )
        .all()
    )

    # --------------------------------------------------
    # Department
    # --------------------------------------------------

    if department_id:

        records = records.filter(
            subject__semester__course__department_id=department_id
        )

    # --------------------------------------------------
    # Course
    # --------------------------------------------------

    if course_id:

        records = records.filter(
            subject__semester__course_id=course_id
        )

    # --------------------------------------------------
    # Semester
    # --------------------------------------------------

    if semester_id:

        records = records.filter(
            subject__semester_id=semester_id
        )

    # --------------------------------------------------
    # Subject
    # --------------------------------------------------

    if subject_id:

        records = records.filter(
            subject_id=subject_id
        )

    # --------------------------------------------------
    # Date
    # --------------------------------------------------

    if attendance_date:

        records = records.filter(
            attendance_date=attendance_date
        )

    # --------------------------------------------------
    # Student
    # --------------------------------------------------

    if student_id:

        records = records.filter(
            student_id=student_id
        )

    # --------------------------------------------------
    # Status
    # --------------------------------------------------

    if status in [
        Attendance.PRESENT,
        Attendance.ABSENT,
    ]:

        records = records.filter(
            status=status
        )

    # --------------------------------------------------
    # Ordering
    # --------------------------------------------------

    records = records.order_by(
        "subject__semester__course__department__code",
        "subject__semester__course__code",
        "subject__semester__number",
        "subject__code",
        "attendance_date",
        "student__roll_number",
    )

    # --------------------------------------------------
    # CSV response
    # --------------------------------------------------

    response = HttpResponse(
        content_type="text/csv; charset=utf-8",
    )

    response["Content-Disposition"] = (
        'attachment; filename="attendance_report.csv"'
    )

    writer = csv.writer(response)

    # --------------------------------------------------
    # Header
    # --------------------------------------------------

    writer.writerow([
        "Department Code",
        "Department Name",

        "Course Code",
        "Course Name",

        "Semester Number",
        "Semester",

        "Subject Code",
        "Subject Name",

        "Attendance Date",

        "Roll Number",
        "Student Name",

        "Status",

        "Class Taken By",
        "Class Taken By Username",
    ])

    # --------------------------------------------------
    # Data
    # --------------------------------------------------

    for record in records:

        department = (
            record.subject
            .semester
            .course
            .department
        )

        course = (
            record.subject
            .semester
            .course
        )

        semester = (
            record.subject
            .semester
        )

        subject = record.subject

        student = record.student

        taken_by_name = ""
        taken_by_username = ""

        if record.taken_by:

            taken_by_name = (
                record.taken_by.get_full_name()
                or record.taken_by.username
            )

            taken_by_username = (
                record.taken_by.username
            )

        writer.writerow([
            department.code,
            department.name,

            course.code,
            course.name,

            semester.number,
            semester.name,

            subject.code,
            subject.name,

            record.attendance_date.strftime(
                "%d/%m/%Y"
            ),

            student.roll_number,
            student.name,

            record.get_status_display(),

            taken_by_name,
            taken_by_username,
        ])

    return response


#==================================================
# Attendance Report
#==================================================


@staff_member_required
def attendance_report(request):

    department_id = request.GET.get(
        "department",
        "",
    )

    course_id = request.GET.get(
        "course",
        "",
    )

    semester_id = request.GET.get(
        "semester",
        "",
    )

    subject_id = request.GET.get(
        "subject",
        "",
    )

    selected_date = request.GET.get(
        "date",
        "",
    )

    student_id = request.GET.get(
        "student",
        "",
    )

    status = request.GET.get(
        "status",
        "",
    )

    # ---------------------------------------------
    # Departments
    # ---------------------------------------------

    departments = Department.objects.all()

    # ---------------------------------------------
    # Courses
    # ---------------------------------------------

    courses = Course.objects.all()

    if department_id:

        courses = courses.filter(
            department_id=department_id
        )

    # ---------------------------------------------
    # Semesters
    # ---------------------------------------------

    semesters = Semester.objects.all()

    if course_id:

        semesters = semesters.filter(
            course_id=course_id
        )

    # ---------------------------------------------
    # Subjects
    # ---------------------------------------------

    subjects = Subject.objects.all()

    if semester_id:

        subjects = subjects.filter(
            semester_id=semester_id
        )

    # ---------------------------------------------
    # Students
    # ---------------------------------------------

    students = Student.objects.all()

    if course_id:

        students = students.filter(
            course_id=course_id
        )

    if semester_id:

        students = students.filter(
            enrollment__semester_id=semester_id
        ).distinct()

    students = students.order_by(
        "roll_number"
    )

    # ---------------------------------------------
    # Attendance
    # ---------------------------------------------

    records = (
        Attendance.objects
        .select_related(
            "student",
            "subject",
            "subject__semester",
            "subject__semester__course",
            "subject__semester__course__department",
            "taken_by",
        )
        .all()
    )

    # ---------------------------------------------
    # Filters
    # ---------------------------------------------

    if department_id:

        records = records.filter(
            subject__semester__course__department_id=department_id
        )

    if course_id:

        records = records.filter(
            subject__semester__course_id=course_id
        )

    if semester_id:

        records = records.filter(
            subject__semester_id=semester_id
        )

    if subject_id:

        records = records.filter(
            subject_id=subject_id
        )

    if selected_date:

        records = records.filter(
            attendance_date=selected_date
        )

    if student_id:

        records = records.filter(
            student_id=student_id
        )

    if status in [
        Attendance.PRESENT,
        Attendance.ABSENT,
    ]:

        records = records.filter(
            status=status
        )

    records = records.order_by(
        "subject__semester__course__department__code",
        "subject__semester__course__code",
        "subject__semester__number",
        "subject__code",
        "attendance_date",
        "student__roll_number",
    )

    total_records = records.count()

    present_count = records.filter(
        status=Attendance.PRESENT
    ).count()

    absent_count = records.filter(
        status=Attendance.ABSENT
    ).count()

    return render(
        request,
        "attendance/report.html",
        {
            "departments": departments,
            "courses": courses,
            "semesters": semesters,
            "subjects": subjects,
            "students": students,

            "records": records,

            "selected_department": department_id,
            "selected_course": course_id,
            "selected_semester": semester_id,
            "selected_subject": subject_id,
            "selected_date": selected_date,
            "selected_student": student_id,
            "selected_status": status,

            "total_records": total_records,
            "present_count": present_count,
            "absent_count": absent_count,
        },
    )