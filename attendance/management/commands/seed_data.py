from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from attendance.models import (
    Attendance,
    Course,
    Enrollment,
    Semester,
    Student,
    Subject,
)


class Command(BaseCommand):
    help = "Create realistic sample NIELIT attendance data."

    def handle(self, *args, **options):

        self.stdout.write(
            self.style.WARNING(
                "Creating realistic NIELIT sample data..."
            )
        )

        # ==========================================================
        # STAFF USERS
        # ==========================================================

        staff_users = []

        staff_data = [
            {
                "username": "bhargav.nath",
                "first_name": "Bhargav",
                "last_name": "Nath",
                "email": "bhargav@nielit.local",
            },
            {
                "username": "anupam.sarma",
                "first_name": "Anupam",
                "last_name": "Sarma",
                "email": "anupam@nielit.local",
            },
            {
                "username": "priyanka.das",
                "first_name": "Priyanka",
                "last_name": "Das",
                "email": "priyanka@nielit.local",
            },
        ]

        for data in staff_data:

            user, created = User.objects.get_or_create(
                username=data["username"],
                defaults={
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "email": data["email"],
                    "is_staff": True,
                },
            )

            if created:

                user.set_password(
                    "ChangeMe123!"
                )

                user.is_staff = True

                user.save()

                self.stdout.write(
                    f"Created staff: {user.get_full_name()}"
                )

            staff_users.append(user)

        # ==========================================================
        # ADMIN USER
        # ==========================================================

        admin, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "first_name": "System",
                "last_name": "Administrator",
                "email": "admin@nielit.local",
                "is_staff": True,
                "is_superuser": True,
            },
        )

        if created:

            admin.set_password(
                "Admin123!"
            )

            admin.is_staff = True
            admin.is_superuser = True

            admin.save()

            self.stdout.write(
                self.style.WARNING(
                    "Created admin: admin / Admin123!"
                )
            )

        # ==========================================================
        # COURSES
        # ==========================================================

        courses_data = [
            {
                "code": "BCA",
                "name": "Bachelor of Computer Applications",
                "semesters": 6,
            },
            {
                "code": "PGDCA",
                "name": "Post Graduate Diploma in Computer Applications",
                "semesters": 2,
            },
            {
                "code": "DECE",
                "name": "Diploma in Electronics & Communication Engineering",
                "semesters": 6,
            },
            {
                "code": "ADCA",
                "name": "Advanced Diploma in Computer Applications",
                "semesters": 4,
            },
        ]

        courses = {}

        for data in courses_data:
            course, _ = Course.objects.get_or_create(
                code=data["code"],
                defaults={"name": data["name"]},
            )
            courses[data["code"]] = course

        # ==========================================================
        # SEMESTERS
        # ==========================================================

        semesters = {}

        semester_names = {
            1: "1st Semester",
            2: "2nd Semester",
            3: "3rd Semester",
            4: "4th Semester",
            5: "5th Semester",
            6: "6th Semester",
        }

        for data in courses_data:

            course = courses[data["code"]]

            semesters[data["code"]] = {}

            for number in range(
                1,
                data["semesters"] + 1,
            ):

                semester, _ = Semester.objects.get_or_create(
                    course=course,
                    number=number,
                    defaults={
                        "name": semester_names[number],
                    },
                )

                semesters[
                    data["code"]
                ][number] = semester

        # ==========================================================
        # SUBJECTS
        # ==========================================================

        subjects_data = {

            "BCA": {

                1: [
                    ("BCA101", "Programming Fundamentals"),
                    ("BCA102", "Computer Fundamentals"),
                    ("BCA103", "Mathematics-I"),
                    ("BCA104", "Digital Logic"),
                    ("BCA105", "Communication Skills"),
                ],

                2: [
                    ("BCA201", "Data Structures"),
                    ("BCA202", "Database Management Systems"),
                    ("BCA203", "Mathematics-II"),
                    ("BCA204", "Computer Organization"),
                    ("BCA205", "Operating Systems Fundamentals"),
                ],

                3: [
                    ("BCA301", "Object Oriented Programming in Java"),
                    ("BCA302", "Web Technologies"),
                    ("BCA303", "Computer Networks"),
                    ("BCA304", "Software Engineering"),
                    ("BCA305", "Management Information Systems"),
                ],

                4: [
                    ("BCA401", "Python Programming"),
                    ("BCA402", "Advanced Database Systems"),
                    ("BCA403", "Operating Systems"),
                    ("BCA404", "Mobile Application Development"),
                    ("BCA405", "Computer Graphics"),
                ],

                5: [
                    ("BCA501", "Artificial Intelligence"),
                    ("BCA502", "Cloud Computing"),
                    ("BCA503", "Cyber Security"),
                    ("BCA504", "Data Analytics"),
                    ("BCA505", "Project Management"),
                ],

                6: [
                    ("BCA601", "Machine Learning"),
                    ("BCA602", "Distributed Systems"),
                    ("BCA603", "Internet of Things"),
                    ("BCA604", "Software Project"),
                    ("BCA605", "Industrial Training"),
                ],
            },

            "PGDCA": {

                1: [
                    ("PG101", "Computer Fundamentals"),
                    ("PG102", "Programming in C"),
                    ("PG103", "Database Management Systems"),
                    ("PG104", "Operating Systems"),
                    ("PG105", "Computer Networks"),
                ],

                2: [
                    ("PG201", "Java Programming"),
                    ("PG202", "Web Development"),
                    ("PG203", "Software Engineering"),
                    ("PG204", "Python Programming"),
                    ("PG205", "Project Work"),
                ],
            },

            "DECE": {

                1: [
                    ("ECE101", "Engineering Mathematics-I"),
                    ("ECE102", "Basic Electronics"),
                    ("ECE103", "Electrical Engineering"),
                    ("ECE104", "Engineering Physics"),
                    ("ECE105", "Engineering Drawing"),
                ],

                2: [
                    ("ECE201", "Engineering Mathematics-II"),
                    ("ECE202", "Electronic Devices"),
                    ("ECE203", "Digital Electronics"),
                    ("ECE204", "Network Theory"),
                    ("ECE205", "Communication Skills"),
                ],

                3: [
                    ("ECE301", "Microprocessors"),
                    ("ECE302", "Analog Communication"),
                    ("ECE303", "Digital Communication"),
                    ("ECE304", "Signals & Systems"),
                    ("ECE305", "Electronic Measurements"),
                ],

                4: [
                    ("ECE401", "Microcontrollers"),
                    ("ECE402", "Data Communication"),
                    ("ECE403", "Control Systems"),
                    ("ECE404", "Embedded Systems"),
                    ("ECE405", "Industrial Electronics"),
                ],

                5: [
                    ("ECE501", "VLSI Design"),
                    ("ECE502", "Optical Communication"),
                    ("ECE503", "Wireless Communication"),
                    ("ECE504", "Digital Signal Processing"),
                    ("ECE505", "Embedded Programming"),
                ],

                6: [
                    ("ECE601", "Advanced Communication Systems"),
                    ("ECE602", "IoT Systems"),
                    ("ECE603", "Industrial Automation"),
                    ("ECE604", "Project Work"),
                    ("ECE605", "Industrial Training"),
                ],
            },

            "ADCA": {

                1: [
                    ("AD101", "Computer Fundamentals"),
                    ("AD102", "Office Automation"),
                    ("AD103", "Programming Fundamentals"),
                    ("AD104", "Database Fundamentals"),
                ],

                2: [
                    ("AD201", "Web Development"),
                    ("AD202", "Python Programming"),
                    ("AD203", "Computer Networks"),
                    ("AD204", "Linux Administration"),
                ],

                3: [
                    ("AD301", "Java Programming"),
                    ("AD302", "Software Engineering"),
                    ("AD303", "Cloud Computing"),
                    ("AD304", "Cyber Security"),
                ],

                4: [
                    ("AD401", "Advanced Web Development"),
                    ("AD402", "Data Analytics"),
                    ("AD403", "Machine Learning"),
                    ("AD404", "Project Work"),
                ],
            },
        }

        subjects = {}

        for course_code, semester_data in subjects_data.items():

            subjects[course_code] = {}

            for semester_number, subject_list in semester_data.items():

                semester = semesters[
                    course_code
                ][semester_number]

                subjects[course_code][
                    semester_number
                ] = []

                for code, name in subject_list:

                    subject, _ = Subject.objects.get_or_create(
                        semester=semester,
                        code=code,
                        defaults={
                            "name": name,
                        },
                    )

                    subjects[
                        course_code
                    ][semester_number].append(
                        subject
                    )

        # ==========================================================
        # STUDENTS
        # ==========================================================

        students_data = {

            "BCA": [
                "JAIPRAKASH SHARMA",
                "MOHIT MANDAL",
                "UPENDRA BAISHYA",
                "BHANUSPRIYA DEORI",
                "JUBIN PEGU",
                "ANSAIGRA DAIMARI",
                "BITOPAN HALOI",
                "PRIYAM RABHA",
                "PINTU SARKAR",
                "ARNABJAN DEKA",
                "DHARMENDRA CHAMUAH",
                "RAJ PEGU",
                "ABHINAV SHARMA",
                "ANKIT DAS",
                "BIKASH BORAH",
                "DIPANKAR DEKA",
                "GAURAV SAIKIA",
                "HIMANSHU DAS",
                "KUNAL KALITA",
                "MANISH THAKUR",
                "NITISH KUMAR",
                "PRANAB DAS",
                "RAHUL SINGH",
                "ROHIT BORAH",
                "SAGAR DEKA",
            ],

            "PGDCA": [
                "AMIT KUMAR",
                "PRIYANKA SHARMA",
                "RAHUL DAS",
                "MONIKA DEVI",
                "SUBHAM SAIKIA",
                "NEHA BORAH",
                "AKASH DAS",
                "RUPALI DEKA",
                "SOURAV KALITA",
                "TANIA SHARMA",
            ],

            "DECE": [
                "ABHISHEK BORAH",
                "ANJALI DAS",
                "BIPUL SAIKIA",
                "CHANDAN DEKA",
                "DEBASHREE PEGU",
                "DHRUBA KALITA",
                "JAYANTA DAS",
                "KARABI DEORI",
                "MUKUL BORAH",
                "NABAJIT SAIKIA",
                "PAYEL DAS",
                "RITUPARNA DEKA",
                "ROBIN PEGU",
                "SNEHA KALITA",
                "TAPAN BORAH",
            ],

            "ADCA": [
                "ARPAN DAS",
                "BARNALI SAIKIA",
                "DEEPAK KALITA",
                "GEETANJALI DAS",
                "KISHAN BORAH",
                "LOPAMUDRA DEKA",
                "NIKHIL SINGH",
                "PALLABI DAS",
                "RAJIB SAIKIA",
                "SONALI BORAH",
            ],
        }

        students = {}

        for course_code, names in students_data.items():

            course = courses[course_code]

            students[course_code] = []

            for index, name in enumerate(
                names,
                start=1,
            ):

                roll_number = (
                    f"{course_code}-{index:03d}"
                )

                student, _ = Student.objects.get_or_create(
                    course=course,
                    roll_number=roll_number,
                    defaults={
                        "name": name,
                        "status": Student.ACTIVE,
                    },
                )

                students[
                    course_code
                ].append(student)

        # ==========================================================
        # ENROLLMENT / CURRENT SEMESTER
        # ==========================================================

        # Different students are placed in different semesters
        # to make the dashboard look realistic.

        for course_code, course_students in students.items():

            max_semester = len(
                semesters[course_code]
            )

            for index, student in enumerate(
                course_students
            ):

                # Spread students across semesters.
                current_semester_number = (
                    index % max_semester
                ) + 1

                # Create progression history from
                # semester 1 to current semester.

                for semester_number in range(
                    1,
                    current_semester_number + 1,
                ):

                    Enrollment.objects.get_or_create(
                        student=student,
                        semester=semesters[
                            course_code
                        ][semester_number],
                    )

        # ==========================================================
        # MARK SOME STUDENTS AS PASSED OUT
        # ==========================================================

        for course_code in [
            "BCA",
            "DECE",
        ]:

            course_students = students[
                course_code
            ]

            for student in course_students[:2]:

                student.status = Student.PASSED_OUT

                student.save(
                    update_fields=[
                        "status"
                    ]
                )

        # ==========================================================
        # ATTENDANCE
        # ==========================================================

        # Generate attendance for the last 15 working days.
        #
        # Attendance is only generated for subjects belonging
        # to the student's current semester.

        today = date.today()

        attendance_dates = []

        current_date = today

        while len(attendance_dates) < 15:

            # Monday-Friday only
            if current_date.weekday() < 5:

                attendance_dates.append(
                    current_date
                )

            current_date -= timedelta(
                days=1
            )

        for course_code, course_students in students.items():

            course_subjects = subjects[
                course_code
            ]

            for student in course_students:

                current_semester = (
                    student.current_semester
                )

                if not current_semester:
                    continue

                # Don't generate normal attendance
                # for passed-out students.
                if student.status != Student.ACTIVE:
                    continue

                semester_subjects = course_subjects[
                    current_semester.number
                ]

                for subject_index, subject in enumerate(
                    semester_subjects
                ):

                    # Generate attendance on all dates.
                    for attendance_date in attendance_dates:

                        # Create a reasonably varied attendance
                        # pattern instead of making everyone present.

                        seed_value = (
                            student.pk
                            + subject.pk
                            + attendance_date.day
                            + subject_index
                        )

                        is_present = (
                            seed_value % 10
                        ) not in [0, 1]

                        status = (
                            Attendance.PRESENT
                            if is_present
                            else Attendance.ABSENT
                        )

                        # Rotate staff members.
                        taken_by = staff_users[
                            (
                                student.pk
                                + subject.pk
                                + attendance_date.day
                            )
                            % len(staff_users)
                        ]

                        Attendance.objects.update_or_create(
                            student=student,
                            subject=subject,
                            attendance_date=attendance_date,
                            defaults={
                                "status": status,
                                "taken_by": taken_by,
                            },
                        )

        # ==========================================================
        # SUMMARY
        # ==========================================================

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "========================================"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "NIELIT sample data created successfully."
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "========================================"
            )
        )

        self.stdout.write(
        )

        self.stdout.write(
            f"Courses     : {Course.objects.count()}"
        )

        self.stdout.write(
            f"Semesters   : {Semester.objects.count()}"
        )

        self.stdout.write(
            f"Subjects    : {Subject.objects.count()}"
        )

        self.stdout.write(
            f"Students    : {Student.objects.count()}"
        )

        self.stdout.write(
            f"Enrollments : {Enrollment.objects.count()}"
        )

        self.stdout.write(
            f"Attendance  : {Attendance.objects.count()}"
        )

        self.stdout.write(
            f"Staff       : {User.objects.filter(is_staff=True).count()}"
        )

        self.stdout.write("")
        self.stdout.write(
            self.style.WARNING(
                "Login credentials:"
            )
        )

        self.stdout.write(
            "Admin  : admin / Admin123!"
        )

        self.stdout.write(
            "Staff  : bhargav.nath / ChangeMe123!"
        )

        self.stdout.write(
            "Staff  : anupam.sarma / ChangeMe123!"
        )

        self.stdout.write(
            "Staff  : priyanka.das / ChangeMe123!"
        )

        self.stdout.write("")

        self.stdout.write(
            self.style.WARNING(
                "Change these passwords before production use."
            )
        )