from django.contrib.auth.models import User
from tasksapp.models import Task
from tasksapp.serializers import TaskSerializer, UserSerializer
from tasksapp.permissions import IsOwner
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import filters


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

    def perform_create(self, serializer):
        serializer.save(owner_id=self.request.user)

    def get_queryset(self):
        """Only can get your own tasks"""
        user = self.request.user
        return Task.objects.filter(owner_id=user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']
