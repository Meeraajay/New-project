from django.contrib.auth.models import User
from django.db import models



class Student(models.Model):

    student_id = models.AutoField(primary_key=True)

    BOARD_CHOICES = [
        ('CBSE', 'CBSE'),
        ('KERALA', 'Kerala State'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),       # after registration
        ('active', 'Active'),         # profile completed
        ('submitted', 'Application Submitted'),   # final application submitted
        ('ranked', 'Ranked the Lists'),        # after admin processing
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Basic details
    name = models.CharField(max_length=100)
    dob = models.DateField(null=True, blank=True)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    register_number = models.CharField(max_length=30, unique=True)

    # Academic system selector
    board = models.CharField(
        max_length=10,
        choices=BOARD_CHOICES,
        null=False,
        blank=False
    )

    # Workflow status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    



class CBSEAcademicDetails(models.Model):

    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name='cbse_details'
    )

    science = models.FloatField()
    social_science = models.FloatField()
    maths = models.FloatField()
    english = models.FloatField()
    language = models.FloatField()
    it = models.FloatField()

    total = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student.name
    



class KeralaAcademicDetails(models.Model):

    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name='kerala_details'
    )

    language1 = models.CharField(max_length=5)
    language2 = models.CharField(max_length=5)

    english = models.CharField(max_length=5)
    hindi = models.CharField(max_length=5)

    social_science = models.CharField(max_length=5)

    physics = models.CharField(max_length=5)
    chemistry = models.CharField(max_length=5)
    biology = models.CharField(max_length=5)

    mathematics = models.CharField(max_length=5)
    it = models.CharField(max_length=5)

    total = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student.name
    


class Extracurricular(models.Model):

    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name='extracurricular'
    )

    # NCC / NSS / Scouts / SPC
    ncc_nss_spc = models.BooleanField(default=False)
    ncc_certificate = models.FileField(
        upload_to='certificates/',
        blank=True,
        null=True
    )

    # Sports Participation
    sports_district = models.BooleanField(default=False)
    sports_state = models.BooleanField(default=False)
    sports_national = models.BooleanField(default=False)

    sports_certificate = models.FileField(
        upload_to='certificates/',
        blank=True,
        null=True
    )

    # Youth Festival Participation
    youth_district = models.BooleanField(default=False)
    youth_state = models.BooleanField(default=False)
    youth_national = models.BooleanField(default=False)

    youth_certificate = models.FileField(
        upload_to='certificates/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student.name


class CoursePreference(models.Model):

    COURSE_CHOICES = [

        ("Computer Science", "Computer Science"),
        ("Bio-Mathematics", "Bio-Mathematics"),
        ("Commerce", "Commerce"),
        ("Humanities", "Humanities"),

    ]

    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name='course_preference'
    )

    pref1 = models.CharField(
        max_length=50,
        choices=COURSE_CHOICES
    )

    pref2 = models.CharField(
        max_length=50,
        choices=COURSE_CHOICES
    )

    pref3 = models.CharField(
        max_length=50,
        choices=COURSE_CHOICES
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - Course Preferences"