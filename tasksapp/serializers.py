from rest_framework import serializers
from tasksapp.models import Task


class TaskSerializer(serializers.Serializer):
    class Meta:
        model = Task
        fields = '__all__'
