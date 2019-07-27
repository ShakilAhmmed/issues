from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

from . import views

urlpatterns = [
    path('', views.admin_login, name="admin_login"),
    path('admin_logout', views.admin_logout, name="admin_logout"),
    path('admin/', admin.site.urls),
    path('accounts/password_reset/', PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('accounts/password_reset/done/', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/reset/done/', PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]
