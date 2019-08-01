from django.urls import path
from . import views
urlpatterns = [
    path('', views.backend, name="backend"),
    path('create_user', views.create_user, name="create_user"),
    path('delete_user', views.delete_user, name="delete_user"),
    path('set_active', views.set_active, name="set_active"),
    path('project', views.project, name="project"),
]
