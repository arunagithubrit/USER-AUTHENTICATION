from django.db import models

# Create your models here.

class Registration(models.Model):
    username=models.CharField(max_length=200)
    email=models.EmailField()
    password=models.CharField(max_length=100)
    is_verified = models.BooleanField(default=0)

