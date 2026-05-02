from django.db import models
from django.contrib.auth.models import User


class AuditLog(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.user)} - {self.action}"


class SecureData(models.Model):

    objects = models.Manager()

    data_name = models.CharField(max_length=255)
    encrypted_content = models.TextField()
    integrity_hash = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    file_upload = models.FileField(upload_to='encrypted_files/', null=True, blank=True)

    def __str__(self):
        return self.data_name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    profile_pic = models.ImageField(upload_to='profile_pics/', default='default.jpg', null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return f'{self.user.username} Profile'
