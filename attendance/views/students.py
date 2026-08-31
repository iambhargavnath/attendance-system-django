from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.urls import reverse

from ..forms import StudentForm

from ..models import (
    Department,
    Course,
    Semester,
    Student,
)


@staff_member_required
def student_list(request):

    department_id = request.GET.get(
        "department"
    )

    course_id = request.GET.get(
        "course"
    )

    semester_id = request.GET.get(
        "semester"
    )

    status = request.GET.get(
        "status",
        "active",
    )

    query = request.GET.get(
        "q",
        "",
    ).strip()

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
    # Students
    # ---------------------------------------------

    students = (
        Student.objects
        .select_related("course")
        .prefetch_related(
            "enrollments__semester"
        )
        .order_by("roll_number")
    )

    if department_id:

        students = students.filter(
            course__department_id=department_id
        )

    if course_id:

        students = students.filter(
            course_id=course_id
        )

    if semester_id:

        students = students.filter(
            enrollments__semester_id=semester_id
        ).distinct()

    # ---------------------------------------------
    # Status
    # ---------------------------------------------

    if status in [
        Student.ACTIVE,
        Student.PASSED_OUT,
        Student.DROPPED,
    ]:

        students = students.filter(
            status=status
        )

    # ---------------------------------------------
    # Search
    # ---------------------------------------------

    if query:

        students = students.filter(
            Q(name__icontains=query)
            | Q(roll_number__icontains=query)
        )

    return render(
        request,
        "attendance/student_list.html",
        {
            "students": students,

            "departments": departments,
            "courses": courses,
            "semesters": semesters,

            "selected_department": department_id,
            "selected_course": course_id,
            "selected_semester": semester_id,
            "selected_status": status,

            "query": query,
        },
    )


# ==================================================
# Enroll Student
# ==================================================

@staff_member_required
def enroll_student(request):

    form = StudentForm(
        request.POST or None
    )

    if request.method == "POST" and form.is_valid():

        student = form.save()

        first_semester = (
            student.enroll_in_first_semester()
        )

        if first_semester:

            messages.success(
                request,
                (
                    f"{student.name} enrolled in "
                    f"{student.course.name}, "
                    f"{first_semester.name}."
                ),
            )

        else:

            messages.warning(
                request,
                (
                    "Student saved, but the selected "
                    "course has no semesters yet."
                ),
            )

        return redirect(
            "student_list_all"
        )

    return render(
        request,
        "attendance/form_page.html",
        {
            "title": "Enroll Student",
            "subtitle": (
                "Enroll a student in a course. "
                "New students start in the first semester."
            ),
            "form": form,
            "back_url": reverse(
                "student_list_all"
            ),
            "back_label": "Student Registry",
        },
    )


# ==================================================
# Pass Out
# ==================================================

@staff_member_required
def passout_student(request, student_id):

    if request.method != "POST":

        return redirect(
            "student_list_all"
        )

    student = get_object_or_404(
        Student,
        pk=student_id,
    )

    student.status = Student.PASSED_OUT

    student.save(
        update_fields=["status"]
    )

    messages.success(
        request,
        (
            f"{student.name} has been "
            "marked as passed out."
        ),
    )

    return redirect(
        "student_list_all"
    )


# ==================================================
# Promote
# ==================================================

@staff_member_required
def promote_student(request, student_id):

    if request.method != "POST":

        return redirect(
            "student_list_all"
        )

    student = get_object_or_404(
        Student,
        pk=student_id,
    )

    # Don't promote passed-out/dropped students
    if student.status != Student.ACTIVE:

        messages.warning(
            request,
            (
                f"{student.name} cannot be "
                "promoted because the student "
                "is not active."
            ),
        )

        return redirect(
            "student_list_all"
        )

    next_semester = student.promote()

    if next_semester:

        messages.success(
            request,
            (
                f"{student.name} promoted to "
                f"{next_semester.name}."
            ),
        )

    else:

        messages.info(
            request,
            (
                f"{student.name} is already "
                "in the final semester."
            ),
        )

    return redirect(
        "student_list_all"
    )


# ==================================================
# Demote
# ==================================================

@staff_member_required
def demote_student(request, student_id):

    if request.method != "POST":

        return redirect(
            "student_list_all"
        )

    student = get_object_or_404(
        Student,
        pk=student_id,
    )

    # Don't demote passed-out/dropped students
    if student.status != Student.ACTIVE:

        messages.warning(
            request,
            (
                f"{student.name} cannot be "
                "demoted because the student "
                "is not active."
            ),
        )

        return redirect(
            "student_list_all"
        )

    previous_semester = student.demote()

    if previous_semester:

        messages.success(
            request,
            (
                f"{student.name} demoted to "
                f"{previous_semester.name}."
            ),
        )

    else:

        messages.info(
            request,
            (
                f"{student.name} is already "
                "in the first semester."
            ),
        )

    return redirect(
        "student_list_all"
    )