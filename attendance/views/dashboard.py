from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q, Count
from django.shortcuts import render

from ..models import Course


def home(request):
    return render(request, "home.html")


@staff_member_required
def dashboard(request):
    query = request.GET.get("q", "").strip()

    course_results = (
        Course.objects
        .annotate(
            semester_count=Count("semesters", distinct=True),
            student_count=Count("students", distinct=True),
        )
        .order_by("name")
    )

    if query:
        course_results = course_results.filter(
            Q(name__icontains=query) | Q(code__icontains=query)
        )

    return render(
        request,
        "attendance/dashboard.html",
        {
            "course_results": course_results[:20],
            "courses": course_results,
            "query": query,
        },
    )
