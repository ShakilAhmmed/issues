from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from backend.models import CustomUser, ProjectModel, TeamModel, TeamMemberModel
from tinymce.widgets import TinyMCE


class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    ACCESS_LEVEL = (
        ('Issue Creator', 'Issue Creator'),
        ('Solver', 'Solver'),
        ('Developer', 'Developer'),
        ('Monitor', 'Monitor')
    )
    access_level = forms.CharField(widget=forms.Select(choices=ACCESS_LEVEL, attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'access_level', 'password1', 'password2',)


class UserSearchForm(forms.Form):
    username = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    ACCESS_LEVEL = (
        ('', 'All'),
        ('Issue Creator', 'Issue Creator'),
        ('Solver', 'Solver'),
        ('Developer', 'Developer'),
        ('Monitor', 'Monitor')
    )
    access_level = forms.CharField(required=False, widget=forms.Select(choices=ACCESS_LEVEL, attrs={
        'class': 'form-control'
    }))


class ProjectSearchForm(forms.Form):
    project_title = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    ACCESS_LEVEL = (
        ('', 'All'),
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Complete', 'Complete')
    )
    project_status = forms.CharField(required=False, widget=forms.Select(choices=ACCESS_LEVEL, attrs={
        'class': 'form-control'
    }))


class ProjectForm(forms.ModelForm):
    class Meta:
        model = ProjectModel
        fields = "__all__"
        CHOICES = (('Active', 'Active'), ('Inactive', 'Inactive'), ('Complete', 'Complete'))
        exclude = ['created_by']
        widgets = {
            'project_title': forms.TextInput(attrs={'class': 'form-control'}),
            'project_status': forms.Select(choices=CHOICES, attrs={'class': 'form-control'}),
            'project_description': TinyMCE(attrs={'class': 'form-control', 'style': 'width:100%'})
        }


class TeamForm(forms.Form):
    team_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    project_choices = ProjectModel.objects.filter(project_status='Active').values_list('id', 'project_title')
    team_leader_choices = CustomUser.objects.exclude(access_level__in=['Issue Creator', 'Monitor']).values_list('id',
                                                                                                            'email')
    description = forms.CharField(widget=TinyMCE(attrs={'class': 'form-control', 'style': 'width:100%'}))
    project = forms.CharField(widget=forms.Select(choices=project_choices, attrs={'class': 'form-control'}))
    team_leader = forms.CharField(widget=forms.Select(choices=team_leader_choices, attrs={'class': 'form-control'}))
