from django.urls import path
from . import views

urlpatterns = [
    path('', views.backend, name="backend"),
    # path('create_user', views.CrateUser.as_view(), name="create_user"),
    path('create_user', views.create_user, name="create_user"),
    path('delete_user', views.delete_user, name="delete_user"),
    path('edit_user/<int:pk>', views.edit_user, name="edit_user"),
    path('set_active', views.set_active, name="set_active"),
    path('project', views.project, name="project"),
    path('delete_project', views.delete_project, name="delete_project"),
    path('update_project_status', views.update_project_status, name="update_project_status"),
    path('edit_project/<int:pk>', views.edit_project, name="edit_project"),
    path('create_team', views.create_team, name="create_team"),
    path('team_list', views.team_list, name="team_list"),
    path('delete_team', views.delete_team, name="delete_team"),
    path('view_team', views.view_team, name="view_team"),
    path('edit_team/<int:pk>', views.edit_team, name="edit_team")
]
