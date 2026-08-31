from django.db import models


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
        enrollment = (
            self.enrollments
            .select_related("semester")
            .order_by("semester__number")
            .last()
        )

        return enrollment.semester if enrollment else None

    def enroll_in_first_semester(self):
        first_semester = (
            self.course.semesters
            .order_by("number")
            .first()
        )

        if first_semester:
            Enrollment.objects.get_or_create(
                student=self,
                semester=first_semester,
            )

        return first_semester

    def promote(self):
        current = self.current_semester

        if not current:
            return self.enroll_in_first_semester()

        next_semester = (
            self.course.semesters
            .filter(number__gt=current.number)
            .order_by("number")
            .first()
        )

        if next_semester:
            Enrollment.objects.get_or_create(
                student=self,
                semester=next_semester,
            )

            return next_semester

        return None

    def demote(self):
        current = self.current_semester

        if not current:
            return None

        previous_semester = (
            self.course.semesters
            .filter(number__lt=current.number)
            .order_by("-number")
            .first()
        )

        if previous_semester:
            Enrollment.objects.get_or_create(
                student=self,
                semester=previous_semester,
            )

            return previous_semester

        return None


class Enrollment(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )

    semester = models.ForeignKey(
        "attendance.Semester",
        on_delete=models.CASCADE,
        related_name="enrollments",
    )

    enrolled_on = models.DateField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["semester__number"]

        constraints = [
            models.UniqueConstraint(
                fields=["student", "semester"],
                name="unique_student_semester_enrollment",
            ),
        ]

    def __str__(self):
        return f"{self.student} - {self.semester}"

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.semester.course_id != self.student.course_id:
            raise ValidationError(
                "Enrollment semester must belong to the student's course."
            )