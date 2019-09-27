from django.db import models
from django.contrib.auth.models import AbstractUser
from tinymce.widgets import TinyMCE
from tinymce.models import HTMLField
from .validators import check_project_name


# Create your models here.
class CustomUser(AbstractUser):
    # Issue Creator, Solver , Developer , Monitor
    access_level = models.CharField(max_length=20, default='Solver')


class ProjectModel(models.Model):
    project_title = models.CharField(max_length=30, unique=True, db_index=True, validators=[check_project_name])
    project_status = models.CharField(max_length=20, db_index=True)
    project_description = HTMLField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project_title

    #
    # class Meta:
    #     ordering = ['-id']

    @classmethod
    def paginate(self):
        return "<h1>Hello</h1>"


class TeamModel(models.Model):
    team_name = models.CharField(unique=True, db_index=True, max_length=50, validators=[check_project_name])
    description = HTMLField()
    project = models.OneToOneField(ProjectModel, on_delete=models.CASCADE, related_name='project', unique=True)
    team_leader = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='team_leader', unique=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TeamMemberModel(models.Model):
    team = models.ForeignKey(TeamModel, on_delete=models.CASCADE, related_name='team')
    member_name = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='member_name')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
