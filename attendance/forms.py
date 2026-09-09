from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Attendance, Course, Enrollment, Semester, Student, Subject



class StaffCreationForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        help_text="Use a strong password for the staff account.",
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password", "confirm_password"]

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with this username already exists.")
        return username

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get("password")
        confirm = cleaned.get("confirm_password")
        if password:
            try:
                validate_password(password)
            except forms.ValidationError as exc:
                self.add_error("password", exc)
        if password and confirm and password != confirm:
            self.add_error("confirm_password", "Passwords do not match.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_staff = True
        user.is_active = True
        if commit:
            user.save()
        return user

class CrispyModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save"))


class CourseForm(CrispyModelForm):
    class Meta:
        model = Course
        fields = ["name", "code"]


class SemesterForm(CrispyModelForm):
    class Meta:
        model = Semester
        fields = ["course", "name", "number"]


class SubjectForm(CrispyModelForm):
    class Meta:
        model = Subject
        fields = ["semester", "name", "code"]


class StudentForm(CrispyModelForm):
    class Meta:
        model = Student
        fields = ["course", "roll_number", "name"]


class AttendanceStaffChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return obj.get_full_name() or obj.username


class AttendanceForm(forms.Form):

    attendance_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date"
            }
        )
    )

    taken_by = AttendanceStaffChoiceField(
        queryset=User.objects.none(),
        label="Class Taken By",
    )

    def __init__(self, *args, **kwargs):

        staff_queryset = kwargs.pop("staff_queryset")

        super().__init__(*args, **kwargs)

        self.fields["taken_by"].queryset = staff_queryset

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(
            Submit(
                "submit",
                "Save Attendance"
            )
        )


class AttendanceStatusForm(forms.Form):
    def __init__(self, students, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for student in students:
            self.fields[f"status_{student.pk}"] = forms.ChoiceField(
                label=student.name,
                choices=Attendance.STATUS_CHOICES,
                widget=forms.RadioSelect,
                initial=Attendance.PRESENT,
            )
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save Attendance"))
