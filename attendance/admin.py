from django.contrib import admin

from .models import Attendance, Course, Enrollment, Semester, Student, Subject


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ("course", "number", "name")
    list_filter = ("course",)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "semester")
    list_filter = ("semester",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("roll_number", "name", "course", "status")
    list_filter = ("course", "status")
    search_fields = ("roll_number", "name")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "semester", "enrolled_on")
    list_filter = ("semester",)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "attendance_date", "status", "taken_by")
    list_filter = ("status", "attendance_date", "subject")
    search_fields = ("student__name", "student__roll_number")
