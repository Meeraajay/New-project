from django.db import models
from accounts.models import Student

COURSE_CHOICES = [

    ("Computer Science", "Computer Science"),
    ("Bio-Mathematics", "Bio-Mathematics"),
    ("Commerce", "Commerce"),
    ("Humanities", "Humanities"),

]


class AdmissionResult(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    course = models.CharField(
        max_length=50,
        choices=COURSE_CHOICES
    )

    preference_order = models.IntegerField(default=1)

    index_mark = models.FloatField(default=0)

    bonus_mark = models.FloatField(default=0)

    final_score = models.FloatField(default=0)
    
    stream_score = models.FloatField(default=0)

    rank = models.IntegerField(
        null=True,
        blank=True
    )

    allotted = models.BooleanField(default=False)

    def __str__(self):

        return f"{self.student.name} - {self.course}"
