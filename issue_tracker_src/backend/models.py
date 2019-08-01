from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    # Issue Creator, Solver , Developer , Monitor
    access_level = models.CharField(max_length=20, default='Solver')
