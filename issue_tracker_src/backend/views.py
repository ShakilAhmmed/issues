import sys

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum, QuerySet
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, QueryDict
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .filters import ProjectFilter
from .serializers import CustomUserSerializer
# Create your views here.
from django.views import View
from django.core.cache import cache
from .models import CustomUser, ProjectModel
from .forms import SignUpForm, ProjectForm, UserSearchForm, ProjectSearchForm, TeamForm
from django.core.paginator import Paginator

from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from django.db.models import Sum

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@login_required()
def backend(request):
    return render(request, 'admin_panel/home.html')


# class CrateUser(View):
#     template_name = 'admin_panel/Rbac/create_user.html'
#
#     def get(self, request):
#         users = CustomUser.objects.all()
#         form = SignUpForm()
#         context = {
#             'form': form,
#             'users': users
#         }
#         return render(request, self.template_name, context)
#
#     def post(self, request):
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "New User Created Successfully")
#             return HttpResponseRedirect(reverse('create_user'))


@login_required()
def create_user(request):
    users = CustomUser.objects.values()
    search_form = UserSearchForm(request.GET)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New User Created Successfully")
            return HttpResponseRedirect(reverse('create_user'))
    else:
        form = SignUpForm()
        # if 'user_data' in cache:
        #     print("Cache")
        #     users = cache.get('user_data')
        # else:
        #     print("Not Cache")
        #     users = CustomUser.objects.only('username', 'email', 'access_level', 'is_active').all()
        #     cache.set('user_data', users, timeout=CACHE_TTL)
        if request.GET.get('username'):
            users = users.filter(username__icontains=request.GET.get('username').strip())
        if request.GET.get('access_level'):
            users = users.filter(access_level=request.GET.get('access_level').strip())
    users = Paginator(users, 3)  # Show 3 contacts per page Also Works While Search
    page = request.GET.get('page')
    users = users.get_page(page)
    context = {
        'form': form,
        'users': users,
        'search_form': search_form
    }
    return render(request, 'admin_panel/Rbac/create_user.html', context)


@login_required()
def edit_user(request, pk):
    users = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = SignUpForm(request.POST, instance=users)
        if form.is_valid():
            form.save()
            messages.success(request, "User Updated Successfully")
            return HttpResponseRedirect(reverse('edit_user', kwargs={'pk': pk}))
    else:
        form = SignUpForm(instance=users)
    context = {
        'form': form,
    }
    return render(request, 'admin_panel/Rbac/edit_user.html', context)


@login_required()
def set_active(request):
    response = {}
    if request.method == "POST":
        response['status'] = 200
        get_user = get_object_or_404(CustomUser, pk=request.POST.get('id'))
        if get_user.is_active:
            get_user.is_active = False
            response['message'] = 'Inactive'
        else:
            get_user.is_active = True
            response['message'] = 'Active'
        get_user.save()
        return JsonResponse(response)


@login_required()
def edit_user_serialize(request):
    response = {}
    if request.method == "POST":
        get_user = get_object_or_404(CustomUser, pk=request.POST.get('edit_id'))
        serialize = CustomUserSerializer(get_user)
        response['status'] = 200
        response['user'] = serialize.data
        return JsonResponse(response)


@login_required()
def delete_user(request):
    if request.method == "POST":
        get_user = CustomUser.objects.filter(pk=request.POST.get('id')).delete()
        return JsonResponse({'status': 200})


@login_required()
def project(request):
    project_search_form = ProjectSearchForm(request.GET)
    projects = ProjectModel.objects.values('pk', 'project_title', 'project_status', 'created_by__username')
    # print(projects)
    # active_data = QuerySet(projects).filter(project_status='Active')
    # print(active_data)
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            save_data = form.save(commit=False)
            save_data.created_by = request.user
            save_data.save()
            cache.delete('projects')
            messages.success(request, "New Project Created Successfully")
            return HttpResponseRedirect(reverse('project'))
    else:
        form = ProjectForm()
        if request.GET.get('project_title'):
            projects = projects.filter(project_title__icontains=request.GET.get('project_title').strip())
        if request.GET.get('project_status'):
            projects = projects.filter(project_status=request.GET.get('project_status').strip())

    projects = Paginator(projects, 10)  # Show 3 contacts per page Also Works While Search
    page = request.GET.get('page')
    projects = projects.get_page(page)
    context = {
        'form': form,
        'projects': projects,
        'project_search_form': project_search_form,

    }
    return render(request, 'admin_panel/Project/project.html', context)


@login_required()
def delete_project(request):
    if request.method == "POST":
        get_project = ProjectModel.objects.filter(pk=request.POST.get('id')).delete()
        return JsonResponse({'status': 200})


@login_required()
def update_project_status(request):
    if request.method == "POST":
        get_project = ProjectModel.objects.get(pk=request.POST.get('id'))
        get_project.project_status = request.POST.get('status')
        get_project.save()
        return JsonResponse({'status': 200})


@login_required()
def edit_project(request, pk):
    project_data = get_object_or_404(ProjectModel, pk=pk)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project_data)
        if form.is_valid():
            form.save()
            messages.success(request, "Project Updated Successfully")
            return HttpResponseRedirect(reverse('project'))
    else:
        form = ProjectForm(instance=project_data)
    context = {
        'form': form
    }
    return render(request, 'admin_panel/Project/edit_project.html', context)


@login_required()
def create_team(request):
    template_name = 'admin_panel/Team/create_team.html'
    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            # project = get_object_or_404(ProjectModel, pk=request.POST.get('project'))
            # print(project)
            # form.project = project.pk
            #form.save()
            messages.success(request, "Team Created Successfully")
            return HttpResponseRedirect(reverse('create_team'))
    else:
        form = TeamForm()
        #form.fields["project"].queryset = ProjectModel.objects.filter(project_status='Active')
    context = {
        'form': form
    }
    return render(request, template_name, context)
