from django.db import models
from .academic import Semester


class Student(models.Model):

    ACTIVE = "active"
    PASSED_OUT = "passed_out"
    DROPPED = "dropped"

    STATUS_CHOICES = [
        (ACTIVE, "Active"),
        (PASSED_OUT, "Passed Out"),
        (DROPPED, "Dropped"),
    ]

    course = models.ForeignKey(
        "attendance.Course",
        on_delete=models.CASCADE,
        related_name="students",
    )

    roll_number = models.CharField(
        max_length=50,
    )

    name = models.CharField(
        max_length=150,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=ACTIVE,
    )

    class Meta:
        ordering = ["roll_number"]

        constraints = [
            models.UniqueConstraint(
                fields=["course", "roll_number"],
                name="unique_roll_number_per_course",
            ),
        ]

    def __str__(self):
        return f"{self.roll_number} - {self.name}"

    @property
    def current_semester(self):
        try:
            return self.enrollment.semester
        except Enrollment.DoesNotExist:
            return None

    def enroll_in_first_semester(self):

        first_semester = (
            self.course.semesters
            .order_by("number")
            .first()
        )

        if not first_semester:
            return None

        enrollment, _ = Enrollment.objects.update_or_create(
            student=self,
            defaults={
                "semester": first_semester,
            },
        )

        return enrollment.semester
    

    def promote(self):

        current = self.current_semester

        if not current:
            return self.enroll_in_first_semester()

        next_semester = (
            self.course.semesters
            .filter(
                number__gt=current.number
            )
            .order_by("number")
            .first()
        )

        if not next_semester:
            return None

        self.enrollment.semester = next_semester
        self.enrollment.save(
            update_fields=["semester"]
        )

        return next_semester
    

    def demote(self):

        current = self.current_semester

        if not current:
            return None

        previous_semester = (
            self.course.semesters
            .filter(
                number__lt=current.number
            )
            .order_by("-number")
            .first()
        )

        if not previous_semester:
            return None

        self.enrollment.semester = previous_semester
        self.enrollment.save(
            update_fields=["semester"]
        )

        return previous_semester


class Enrollment(models.Model):
    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name="enrollment",
    )

    semester = models.ForeignKey(
        Semester,
        on_delete=models.PROTECT,
        related_name="current_students",
    )

    enrolled_on = models.DateField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-enrolled_on"]

    def __str__(self):
        return (
            f"{self.student} - "
            f"{self.semester}"
        )

    def clean(self):
        from django.core.exceptions import ValidationError

        if (
            self.semester.course_id
            != self.student.course_id
        ):
            raise ValidationError(
                "Enrollment semester must belong to the student's course."
            )