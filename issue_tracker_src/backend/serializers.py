from rest_framework import serializers

from .models import CustomUser, TeamModel, TeamMemberModel, ProjectModel


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectModel
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectModel
        fields = "__all__"


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMemberModel
        fields = "__all__"


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamModel
        fields = ['__all__']
