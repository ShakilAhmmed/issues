from .models import ProjectModel
import django_filters
from django import forms


class ProjectFilter(django_filters.FilterSet):
    project_title = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={
            'placeholder': 'Search place', 'class': 'form-control'
        }))
    CHOICES = (('', 'All'), ('Active', 'Active'), ('Inactive', 'Inactive'), ('Complete', 'Complete'))
    project_status = django_filters.ChoiceFilter(
        choices=CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }))

    class Meta:
        model = ProjectModel
        fields = ['project_title', 'project_status']
