from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [("auth", "0012_alter_user_first_name_max_length")]
    operations = [
        migrations.CreateModel(name="Department", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("name", models.CharField(max_length=150, unique=True)),
            ("code", models.CharField(max_length=30, unique=True)),
        ], options={"ordering": ["name"]}),
        migrations.CreateModel(name="Course", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("name", models.CharField(max_length=150)),
            ("code", models.CharField(max_length=30)),
            ("department", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="courses", to="attendance.department")),
        ], options={"ordering": ["name"]}),
        migrations.CreateModel(name="Semester", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("name", models.CharField(max_length=100)),
            ("number", models.PositiveIntegerField()),
            ("course", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="semesters", to="attendance.course")),
        ], options={"ordering": ["number"]}),
        migrations.CreateModel(name="Subject", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("name", models.CharField(max_length=200)),
            ("code", models.CharField(max_length=30)),
            ("semester", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="subjects", to="attendance.semester")),
        ], options={"ordering": ["code"]}),
        migrations.CreateModel(name="Student", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("roll_number", models.CharField(max_length=50)),
            ("name", models.CharField(max_length=150)),
            ("course", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="students", to="attendance.course")),
        ], options={"ordering": ["roll_number"]}),
        migrations.CreateModel(name="Enrollment", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("enrolled_on", models.DateField(auto_now_add=True)),
            ("semester", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="enrollments", to="attendance.semester")),
            ("student", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="enrollments", to="attendance.student")),
        ], options={"ordering": ["semester__number"]}),
        migrations.CreateModel(name="Attendance", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("attendance_date", models.DateField()),
            ("status", models.CharField(choices=[("P", "Present"), ("A", "Absent")], max_length=1)),
            ("student", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="attendances", to="attendance.student")),
            ("subject", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="attendances", to="attendance.subject")),
            ("taken_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="attendance_sessions", to="auth.user")),
        ], options={"ordering": ["attendance_date", "student__roll_number"]}),
        migrations.AddConstraint(model_name="course", constraint=models.UniqueConstraint(fields=("department", "code"), name="unique_course_code_per_department")),
        migrations.AddConstraint(model_name="semester", constraint=models.UniqueConstraint(fields=("course", "number"), name="unique_semester_per_course")),
        migrations.AddConstraint(model_name="subject", constraint=models.UniqueConstraint(fields=("semester", "code"), name="unique_subject_code_per_semester")),
        migrations.AddConstraint(model_name="student", constraint=models.UniqueConstraint(fields=("course", "roll_number"), name="unique_roll_number_per_course")),
        migrations.AddConstraint(model_name="enrollment", constraint=models.UniqueConstraint(fields=("student", "semester"), name="unique_student_semester_enrollment")),
        migrations.AddConstraint(model_name="attendance", constraint=models.UniqueConstraint(fields=("student", "subject", "attendance_date"), name="unique_attendance_per_student_subject_date")),
    ]
