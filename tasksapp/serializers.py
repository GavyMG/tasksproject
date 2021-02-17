from django.contrib.auth.models import User
from rest_framework import serializers
from tasksapp.models import Task


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    owner_id = serializers.ReadOnlyField(source='owner_id.username')

    class Meta:
        model = Task
        fields = ['url', 'id', 'name', 'description', 'completed', 'owner_id', 'create_date', 'update_date']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    task_ids = serializers.HyperlinkedRelatedField(many=True, view_name='task-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'task_ids']
