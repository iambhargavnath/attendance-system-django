from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Attendance, Course, Department, Enrollment, Semester, Student, Subject

admin.site.site_header = "NIELIT Institute Administration"
admin.site.site_title = "NIELIT Administration"
admin.site.index_title = "Institute Management"


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "department")
    list_filter = ("department",)
    search_fields = ("code", "name")


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ("number", "name", "course")
    list_filter = ("course",)
    ordering = ("course", "number")


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "semester")
    list_filter = ("semester",)
    search_fields = ("code", "name")


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("roll_number", "name", "course")
    list_filter = ("course",)
    search_fields = ("roll_number", "name")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "semester", "enrolled_on")
    list_filter = ("semester",)
    search_fields = ("student__name", "student__roll_number")


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "attendance_date", "status", "taken_by")
    list_filter = ("subject", "attendance_date", "status", "taken_by")
    search_fields = ("student__name", "student__roll_number", "subject__name")
