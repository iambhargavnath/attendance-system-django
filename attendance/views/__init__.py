from .dashboard import home, dashboard

from .management import staff_list, add_staff, management

from .academic import (
    course_list,
    add_course,
    semester_list,
    add_semester,
    subject_list,
    add_subject,
)

from .students import (
    student_list,
    enroll_student,
    passout_student,
    promote_student,
    demote_student,
)

from .attendance import (
    attendance_register,
    mark_attendance,
    export_attendance,
    attendance_report,
)
