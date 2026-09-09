from django.contrib.auth.models import User
from django.db import models


class Attendance(models.Model):

    PRESENT = "P"
    ABSENT = "A"

    STATUS_CHOICES = [
        (PRESENT, "Present"),
        (ABSENT, "Absent"),
    ]

    student = models.ForeignKey(
        "attendance.Student",
        on_delete=models.CASCADE,
        related_name="attendances",
    )

    subject = models.ForeignKey(
        "attendance.Subject",
        on_delete=models.CASCADE,
        related_name="attendances",
    )

    attendance_date = models.DateField()

    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
    )

    taken_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="attendance_sessions",
    )

    class Meta:
        ordering = [
            "attendance_date",
            "student__roll_number",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "student",
                    "subject",
                    "attendance_date",
                ],
                name="unique_attendance_per_student_subject_date",
            ),
        ]

    def __str__(self):
        return (
            f"{self.student} - "
            f"{self.subject.code} - "
            f"{self.attendance_date} - "
            f"{self.status}"
        )