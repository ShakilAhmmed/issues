from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from backend.models import CustomUser, ProjectModel, TeamModel, TeamMemberModel
from django.core.exceptions import ValidationError
from tinymce.widgets import TinyMCE

from .validators import check_project_name


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


# class TeamForm(forms.ModelForm):
#     # team_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
#     # description = TinyMCE(attrs={'class': 'form-control', 'style': 'width:100%'})
#     project = forms.ModelChoiceField(queryset=ProjectModel.objects.filter(project_status='Active'),
#                                      widget=forms.Select(attrs={'class': 'form-control'}),
#                                      empty_label='Please Select A Project')
#     team_leader = forms.ModelChoiceField(
#         queryset=CustomUser.objects.exclude(access_level__in=['Issue Creator', 'Monitor']),
#         widget=forms.Select(attrs={'class': 'form-control members'}), empty_label='Please Select A Team Leader')
#
#     class Meta:
#         model = TeamModel
#         fields = ['team_name', 'description', 'project', 'team_leader']
#         widgets = {
#             'team_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'description': TinyMCE(attrs={'class': 'form-control', 'style': 'width:100%'}),
#         }

# def __init__(self, *args, **kwargs):
#     super(TeamForm, self).__init__(*args, **kwargs)
#     self.fields['project'].queryset = ProjectModel.objects.filter(project_status='Active')
#     self.fields['team_leader'].queryset = CustomUser.objects.exclude(access_level__in=['Issue Creator', 'Monitor'])
class TeamModelForm(forms.ModelForm):
    class Meta:
        model = TeamModel
        fields = "__all__"
        project_data = ProjectModel.objects.filter(project_status='Active')
        choices = [(value.id, value.project_title) for value in project_data]
        team_data = CustomUser.objects.exclude(access_level__in=['Issue Creator', 'Monitor'])
        team_choices = [(value.id, value.email) for value in team_data]
        widgets = {
            'team_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': TinyMCE(attrs={'class': 'form-control', 'style': 'width:100%'}),
            'project': forms.Select(choices=choices, attrs={'class': 'form-control'}),
            'team_leader': forms.Select(choices=team_choices, attrs={'class': 'form-control'}),

        }


class TeamForm(forms.Form):
    team_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                validators=[check_project_name])
    description = forms.CharField(widget=TinyMCE(attrs={'class': 'form-control', 'style': 'width:100%'}))
    project_data = ProjectModel.objects.filter(project_status='Active')
    choices = [(value.id, value.project_title) for value in project_data]
    project = forms.CharField(widget=forms.Select(choices=choices, attrs={'class': 'form-control'}))

    team_data = CustomUser.objects.exclude(access_level__in=['Issue Creator', 'Monitor'])
    choices = [('', 'Please Select A Team Leader')]
    for value in team_data:
        choices.append((value.id, value.email))
    team_leader = forms.CharField(widget=forms.Select(choices=choices, attrs={'class': 'form-control members'}))

    # Whole Form Field Validation
    def clean(self):
        cleaned_data = super(TeamForm, self).clean()
        existing_team_data = TeamModel.objects.filter(team_name=cleaned_data.get('team_name'))

        if existing_team_data.exists():
            raise forms.ValidationError("Team Name Exists")

        existing_project_data = TeamModel.objects.filter(project=self.cleaned_data.get('project'))
        if existing_project_data.exists():
            raise forms.ValidationError("Project Already Selected For Another Team")

        existing_leader_data = TeamModel.objects.filter(team_leader=self.cleaned_data.get('team_leader'))
        if existing_leader_data.exists():
            raise forms.ValidationError("Member Selected For Another Team")

    # Single Field Validation
    # def clean_team_name(self):
    #     existing_data = TeamModel.objects.filter(project=self.cleaned_data['team_name'])
    #     if existing_data.exists():
    #         raise ValidationError("Team Name Exists")
    #
    # def clean_project(self):
    #     existing_data = TeamModel.objects.filter(project=self.cleaned_data['project'])
    #     if existing_data.exists():
    #         raise ValidationError("Project Already Selected For Another Team")
    #
    # def clean_team_leader(self):
    #     existing_data = TeamModel.objects.filter(team_leader=self.cleaned_data['team_leader'])
    #     if existing_data.exists():
    #         raise ValidationError("Member Selected For Another Team")


class TeamSearch(forms.Form):
    team_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    project_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    leader_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
