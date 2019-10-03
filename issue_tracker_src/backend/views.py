import sys

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum, QuerySet
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, QueryDict
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db import transaction
from .filters import ProjectFilter
from .serializers import CustomUserSerializer, TeamSerializer
# Create your views here.
from django.views import View
from django.core.cache import cache
from .models import CustomUser, ProjectModel, TeamModel, TeamMemberModel
from .forms import SignUpForm, ProjectForm, UserSearchForm, ProjectSearchForm, TeamForm
from django.core.paginator import Paginator
from django.core import serializers
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from django.db.models import Sum
from django.core import serializers

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
        members = request.POST.getlist("member_name[]")
        if form.is_valid():
            if '' in members:
                messages.error(request, 'Please Select Team Members')
            else:
                with transaction.atomic():
                    team_object = TeamModel()
                    team_object.team_name = form.cleaned_data['team_name']
                    team_object.description = form.cleaned_data['description']
                    team_object.project = get_object_or_404(ProjectModel, pk=request.POST.get('project'))
                    team_object.team_leader = get_object_or_404(CustomUser, pk=request.POST.get('team_leader'))
                    team_object.created_by = get_object_or_404(CustomUser, pk=request.POST.get('created_by'))
                    team_object.save()
                    for data in members:
                        if data != '':
                            team_members = TeamMemberModel()
                            team_members.team = team_object
                            team_members.member_name = get_object_or_404(CustomUser, pk=data)
                            team_members.save()
                messages.success(request, "Team Created Successfully")
            return HttpResponseRedirect(reverse('team_list'))
    else:
        form = TeamForm()
    team_leader = CustomUser.objects.exclude(access_level__in=['Issue Creator', 'Monitor'])
    context = {
        'form': form,
        'team_leader': team_leader,
    }
    return render(request, template_name, context)


@login_required
def team_list(request):
    template_name = 'admin_panel/Team/team_list.html'
    team_list_data = TeamModel.objects.select_related().all()
    team_list_data = Paginator(team_list_data, 10)  # Show 3 contacts per page Also Works While Search
    page = request.GET.get('page')
    team_list_data = team_list_data.get_page(page)
    context = {
        'team_list_data': team_list_data,
    }
    return render(request, template_name, context)


@login_required
def delete_team(request):
    if request.method == "POST":
        get_project = TeamModel.objects.filter(pk=request.POST.get('id')).delete()
        return JsonResponse({'status': 200})


@login_required
def view_team(request):
    if request.method == "POST":
        get_team = get_object_or_404(TeamModel, pk=request.POST.get('id'))
        team_members = TeamMemberModel.objects.filter(team=get_team.id)
        table = ""
        table += "<div class=\"row\">"
        table += "<div class=\"col-sm-6\">"
        table += "<label>Team Name:</label>"
        table += "<p>" + get_team.team_name + "</p>"
        table += "</div>"
        table += "<div class=\"col-sm-6\">"
        table += "<label> TeamLeader: </label>"
        table += "<p>" + get_team.team_leader.username + "(" + get_team.team_leader.email + ")</p>"
        table += "</div>"
        table += "<hr>"
        table += "<table class =\"table table-bordered\">"
        table += "<tr>"
        table += "<th> Member Name </th>"
        table += "<th> Member Access Level </th>"
        table += "</tr>"
        for data in team_members:
            table += "<tr>"
            table += "<td>" + data.member_name.username + "(" + data.member_name.email + ")</td>"
            table += "<td>" + data.member_name.access_level + "</td>"
            table += "</tr>"
        table += "</table>"
        table += "</div>"
        return HttpResponse(table)
