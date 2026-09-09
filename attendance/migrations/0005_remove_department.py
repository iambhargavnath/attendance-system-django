from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("attendance", "0004_alter_enrollment_options_and_more"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="course",
            name="unique_course_code_per_department",
        ),
        migrations.RemoveField(
            model_name="course",
            name="department",
        ),
        migrations.AlterField(
            model_name="course",
            name="code",
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.DeleteModel(
            name="Department",
        ),
    ]
