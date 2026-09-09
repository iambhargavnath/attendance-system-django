from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=30, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.code} - {self.name}"


class Semester(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="semesters",
    )
    name = models.CharField(max_length=100)
    number = models.PositiveIntegerField()

    class Meta:
        ordering = ["number"]
        constraints = [
            models.UniqueConstraint(
                fields=["course", "number"],
                name="unique_semester_per_course",
            ),
        ]

    def __str__(self):
        return f"{self.course.code} - {self.name}"


class Subject(models.Model):
    semester = models.ForeignKey(
        Semester,
        on_delete=models.CASCADE,
        related_name="subjects",
    )
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=30)

    class Meta:
        ordering = ["code"]
        constraints = [
            models.UniqueConstraint(
                fields=["semester", "code"],
                name="unique_subject_code_per_semester",
            ),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"
