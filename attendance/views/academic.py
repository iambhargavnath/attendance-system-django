from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q, Count
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.urls import reverse

from ..forms import (
    DepartmentForm,
    CourseForm,
    SemesterForm,
    SubjectForm,
)

from ..models import (
    Department,
    Course,
    Semester,
)


def is_admin(user):
    return user.is_authenticated and user.is_superuser


# ==================================================
# Department
# ==================================================

@staff_member_required
def department_list(request):

    query = request.GET.get("q", "").strip()

    departments = (
        Department.objects
        .annotate(
            course_count=Count(
                "courses",
                distinct=True,
            )
        )
    )

    if query:

        departments = departments.filter(
            Q(name__icontains=query)
            | Q(code__icontains=query)
        )

    return render(
        request,
        "attendance/department_list.html",
        {
            "departments": departments,
            "query": query,
        },
    )


@user_passes_test(is_admin)
def add_department(request):

    form = DepartmentForm(
        request.POST or None
    )

    if request.method == "POST" and form.is_valid():

        form.save()

        messages.success(
            request,
            "Department added successfully.",
        )

        return redirect("department_list")

    return render(
        request,
        "attendance/form_page.html",
        {
            "title": "Add Department",
            "subtitle": "Create an academic department.",
            "form": form,
            "back_url": reverse(
                "department_list"
            ),
            "back_label": "Departments",
        },
    )


# ==================================================
# Course
# ==================================================

@staff_member_required
def course_list(request, department_id=None):

    department = (
        get_object_or_404(
            Department,
            pk=department_id,
        )
        if department_id
        else None
    )

    query = request.GET.get(
        "q",
        "",
    ).strip()

    courses = (
        department.courses.all()
        if department
        else Course.objects
        .select_related("department")
        .all()
    )

    if query:

        courses = courses.filter(
            Q(name__icontains=query)
            | Q(code__icontains=query)
        )

    return render(
        request,
        "attendance/course_list.html",
        {
            "courses": courses,
            "department": department,
            "query": query,
        },
    )


@user_passes_test(is_admin)
def add_course(request):

    form = CourseForm(
        request.POST or None
    )

    if request.method == "POST" and form.is_valid():

        obj = form.save()

        messages.success(
            request,
            "Course added successfully.",
        )

        return redirect(
            "course_list",
            department_id=obj.department_id,
        )

    return render(
        request,
        "attendance/form_page.html",
        {
            "title": "Add Course",
            "subtitle": (
                "Create a course under a department."
            ),
            "form": form,
            "back_url": reverse(
                "course_list_all"
            ),
            "back_label": "Courses",
        },
    )


# ==================================================
# Semester
# ==================================================

@staff_member_required
def semester_list(request, course_id):

    course = get_object_or_404(
        Course.objects.select_related(
            "department"
        ),
        pk=course_id,
    )

    query = request.GET.get(
        "q",
        "",
    ).strip()

    semesters = course.semesters.all()

    if query:

        semesters = semesters.filter(
            Q(name__icontains=query)
            | Q(number__icontains=query)
        )

    return render(
        request,
        "attendance/semester_list.html",
        {
            "course": course,
            "semesters": semesters,
            "query": query,
        },
    )


@user_passes_test(is_admin)
def add_semester(request, course_id=None):

    form = SemesterForm(
        request.POST or None
    )

    course = (
        get_object_or_404(
            Course,
            pk=course_id,
        )
        if course_id
        else None
    )

    if course:

        form.fields[
            "course"
        ].queryset = Course.objects.filter(
            pk=course.pk
        )

        form.initial[
            "course"
        ] = course

    if request.method == "POST" and form.is_valid():

        obj = form.save()

        messages.success(
            request,
            "Semester added successfully.",
        )

        return redirect(
            "semester_list",
            course_id=obj.course_id,
        )

    return render(
        request,
        "attendance/form_page.html",
        {
            "title": "Add Semester",
            "subtitle": "Add a semester to a course.",
            "form": form,
            "back_url": (
                reverse(
                    "semester_list",
                    args=[course.pk],
                )
                if course
                else reverse(
                    "course_list_all"
                )
            ),
            "back_label": (
                "Semesters"
                if course
                else "Courses"
            ),
        },
    )


# ==================================================
# Subject
# ==================================================

@staff_member_required
def subject_list(request, semester_id):

    semester = get_object_or_404(
        Semester.objects.select_related(
            "course__department"
        ),
        pk=semester_id,
    )

    query = request.GET.get(
        "q",
        "",
    ).strip()

    subjects = semester.subjects.all()

    if query:

        subjects = subjects.filter(
            Q(name__icontains=query)
            | Q(code__icontains=query)
        )

    return render(
        request,
        "attendance/subject_list.html",
        {
            "semester": semester,
            "subjects": subjects,
            "query": query,
        },
    )


@user_passes_test(is_admin)
def add_subject(request, semester_id=None):

    form = SubjectForm(
        request.POST or None
    )

    semester = (
        get_object_or_404(
            Semester.objects.select_related(
                "course"
            ),
            pk=semester_id,
        )
        if semester_id
        else None
    )

    if semester:

        form.fields[
            "semester"
        ].queryset = Semester.objects.filter(
            pk=semester.pk
        )

        form.initial[
            "semester"
        ] = semester

    if request.method == "POST" and form.is_valid():

        obj = form.save()

        messages.success(
            request,
            "Subject added successfully.",
        )

        return redirect(
            "subject_list",
            semester_id=obj.semester_id,
        )

    return render(
        request,
        "attendance/form_page.html",
        {
            "title": "Add Subject",
            "subtitle": (
                "Add a subject to a semester."
            ),
            "form": form,
            "back_url": (
                reverse(
                    "subject_list",
                    args=[semester.pk],
                )
                if semester
                else reverse("dashboard")
            ),
            "back_label": (
                "Subjects"
                if semester
                else "Dashboard"
            ),
        },
    )