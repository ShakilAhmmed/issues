from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
# Create your views here.
from .forms import SignUpForm


@login_required()
def backend(request):
    return render(request, 'admin_panel/home.html')


@login_required()
def create_user(request):
    users = User.objects.all()
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
