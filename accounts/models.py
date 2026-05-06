from django.contrib.auth.models import User
from django.db import models


class Student(models.Model):

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