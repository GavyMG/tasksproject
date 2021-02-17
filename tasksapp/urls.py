from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tasksapp import views


router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls))
]
