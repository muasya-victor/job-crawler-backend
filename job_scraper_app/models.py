# models.py

from django.contrib.auth.models import AbstractUser, Permission, Group
from django.contrib.auth.models import Group as AuthGroup
from django.db import models


class User(AbstractUser):
    user_phone_code = models.CharField(max_length=5, null=True, blank=True)
    user_phone_number = models.CharField(max_length=15, null=True, blank=True)
    user_interest = models.JSONField(default=list)
    user_avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='custom_users',
        help_text='Specific permissions for this user.',
        related_query_name='custom_user',
    )

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='custom_users',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='custom_user',
    )

    class Meta:
        permissions = [
            ("create_job", "Can Create Job"),
        ]


class Job(models.Model):
    job_title = models.CharField(max_length=255, null=True, blank=True)
    job_company_name = models.CharField(max_length=255, null=True, blank=True)
    job_location = models.CharField(max_length=100, null=True, blank=True)
    job_id = models.CharField(max_length=100, null=True, blank=True)
    job_level = models.CharField(max_length=100, null=True, blank=True)
    job_description = models.CharField(max_length=100, null=True, blank=True)
    job_link = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.job_title} at {self.job_company_name} in {self.job_location}"


class Portfolio(models.Model):
    portfolio_user = models.ForeignKey(User, on_delete=models.CASCADE)
    portfolio_jobs = models.ManyToManyField(Job, through='AttemptedJobs')

    def __str__(self):
        return f"Portfolio of {self.portfolio_user.username}"


class AttemptedJobs(models.Model):
    ATTEMPTED_JOB_STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('complete', 'Complete'),
    ]

    attempted_job = models.ForeignKey(Job, on_delete=models.CASCADE, blank=True, null=True)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date_attempted = models.DateTimeField(auto_now_add=True)
    attempted_job_status = models.CharField(max_length=10, choices=ATTEMPTED_JOB_STATUS_CHOICES, default='ongoing')

    def __str__(self):
        return f"{self.date_attempted}  {self.attempted_job_status}"

