from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('employee', 'Employee'),
        ('admin', 'Admin'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='employee')
    phone = models.CharField(max_length=20, blank=True)
    two_factor_enabled = models.BooleanField(default=False)
    two_factor_method = models.CharField(max_length=20, choices=[
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('authenticator', 'Authenticator App'),
    ], blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_user_type_display()})"

class TwoFactorCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    def __str__(self):
        return f"2FA code for {self.user.username}"
    
    @property
    def is_valid(self):
        return not self.is_used and timezone.now() < self.expires_at