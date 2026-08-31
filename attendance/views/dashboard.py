from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q, Count
from django.shortcuts import redirect, render

from ..models import Course, Department


def home(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("dashboard")

    return render(
        request,
        "home.html",
    )


@staff_member_required
def dashboard(request):

    query = request.GET.get("q", "").strip()

    departments = (
        Department.objects
        .annotate(
            course_count=Count(
                "courses",
                distinct=True,
            )
        )
        .prefetch_related("courses")
    )

    course_results = (
        Course.objects
        .select_related("department")
        .annotate(
            semester_count=Count(
                "semesters",
                distinct=True,
            ),
            student_count=Count(
                "students",
                distinct=True,
            ),
        )
    )

    if query:

        course_results = course_results.filter(
            Q(name__icontains=query)
            | Q(code__icontains=query)
            | Q(department__name__icontains=query)
        )

    return render(
        request,
        "attendance/dashboard.html",
        {
            "departments": departments,
            "course_results": course_results[:20],
            "query": query,
        },
    )