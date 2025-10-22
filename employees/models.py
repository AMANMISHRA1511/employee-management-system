from django.db import models
from django.utils import timezone
from django.conf import settings

class Employee(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employee_profile'
    )
    department = models.CharField(max_length=50, choices=[
        ('HR', 'Human Resources'),
        ('IT', 'Information Technology'),
        ('Finance', 'Finance'),
        ('Marketing', 'Marketing'),
        ('Sales', 'Sales'),
        ('Operations', 'Operations'),
    ])
    position = models.CharField(max_length=100)
    join_date = models.DateField(default=timezone.now)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Active', 'Active'),
            ('Inactive', 'Inactive'),
            ('On Leave', 'On Leave'),
        ],
        default='Active'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return f"{self.user.first_name} {self.user.last_name}"
        return f"Employee #{self.id}"

    @property
    def full_name(self):
        if self.user:
            return f"{self.user.first_name} {self.user.last_name}"
        return f"Employee #{self.id}"

    @property
    def email(self):
        return self.user.email if self.user else "No Email"
