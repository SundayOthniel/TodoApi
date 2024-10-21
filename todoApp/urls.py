from django.urls import path 
from .views import CreateUser, ViewUser, ViewUsers, DeleteUser, CreateTask, index

urlpatterns = [
    path('create_user/', CreateUser.as_view(), name='create_user'),
    path('list_user/', ViewUsers.as_view(), name='list_user'),
    path('delete_user/<int:pk>/', DeleteUser.as_view(), name='delete_user'),
    path('view_user/<int:pk>/', ViewUser.as_view(), name='view_user'),
    path('create_task/', CreateTask.as_view(), name='create_task'),
    path('', index, name='index'),
]
