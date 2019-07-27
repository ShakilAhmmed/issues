from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse


# Create your views here.
def admin_login(request):
    if request.method == "POST":
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        try:
            get_user_name = User.objects.get(email=email)
            user_logged_in = authenticate(username=get_user_name, password=password)
            if user_logged_in is not None:
                login(request, user_logged_in)
                messages.success(request, f"Welcome Back {user_logged_in.username}")
                return HttpResponseRedirect(reverse('backend'))
            else:
                messages.error(request, 'Invalid Credentials')
                return HttpResponseRedirect(reverse('admin_login'))
        except:
            messages.warning(request, 'Wrong Email')
            return HttpResponseRedirect(reverse('admin_login'))

    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('backend'))
        return render(request, 'login_panel/login.html')


@login_required()
def admin_logout(request):
    logout(request)
    messages.success(request, "You're Logged Out Successfully")
    return HttpResponseRedirect(reverse('admin_login'))



