from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

# Create your views here.
from .models import CustomUser
from .forms import SignUpForm


@login_required()
def backend(request):
    return render(request, 'admin_panel/home.html')


@login_required()
def create_user(request):
    users = CustomUser.objects.all()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New User Created Successfully")
            return HttpResponseRedirect(reverse('create_user'))
    else:
        form = SignUpForm()
    context = {
        'form': form,
        'users': users
    }
    return render(request, 'admin_panel/Rbac/create_user.html', context)


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
def delete_user(request):
    if request.method == "POST":
        get_user = CustomUser.objects.filter(pk=request.POST.get('id')).delete()
        return JsonResponse({'status': 200})


@login_required()
def project(request):
    return HttpResponse("Ok")
