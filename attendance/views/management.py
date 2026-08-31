from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse

from ..forms import StaffCreationForm


def is_admin(user):
    return user.is_authenticated and user.is_superuser


@user_passes_test(is_admin)
def management(request):
    return render(
        request,
        "attendance/management.html",
    )


@user_passes_test(is_admin)
def staff_list(request):

    query = request.GET.get("q", "").strip()

    staff = (
        User.objects
        .filter(
            is_staff=True,
            is_superuser=False,
        )
        .order_by(
            "first_name",
            "username",
        )
    )

    if query:

        staff = staff.filter(
            Q(username__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(email__icontains=query)
        )

    return render(
        request,
        "attendance/staff_list.html",
        {
            "staff": staff,
            "query": query,
        },
    )


@user_passes_test(is_admin)
def add_staff(request):

    form = StaffCreationForm(
        request.POST or None
    )

    if request.method == "POST" and form.is_valid():

        user = form.save()

        messages.success(
            request,
            f"Staff account '{user.username}' created successfully.",
        )

        return redirect("staff_list")

    return render(
        request,
        "attendance/form_page.html",
        {
            "title": "Add Staff",
            "subtitle": (
                "Create a staff account. "
                "Staff can log in through the normal Staff Login page."
            ),
            "form": form,
            "back_url": reverse("staff_list"),
            "back_label": "Staff",
        },
    )