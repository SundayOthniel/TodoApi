from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.exceptions import NotFound
from rest_framework.decorators import api_view
from .serializers import UserTaskSerializer, UsersSerializer, ViewTaskSerializers, ViewUserSerializer
from rest_framework import generics, mixins
from rest_framework.response import Response
from .models import UserTask, Users
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework import permissions
from rest_framework import authentication


@api_view(http_method_names=['GET'])
def index(request, format=None):
    
    if request.user.is_authenticated:
        response_url = ({
            'create_user': reverse('create_user', request=request, format=format),
            'list_users': reverse('list_user', request=request, format=format),
            'create_task': reverse('create_task', request=request, format=format),
            'view_task': reverse('view_task', request=request, format=format),
        })
        task = UserTask.objects.filter(user=request.user).first()
        user = Users.objects.first()
        if user:
            response_url['view_user'] = reverse(
                'view_user', kwargs={'pk': user.pk}, request=request, format=format)
            response_url['delete_user'] = reverse(
                'delete_user', kwargs={'pk': user.pk}, request=request, format=format)
        if task:
            response_url['delete_task'] = reverse(
                'delete_task', kwargs={'pk': task.pk}, request=request, format=format)
        return Response(response_url)
    else:
        response_url = ({
            'create_user': reverse('create_user', request=request, format=format) })
        return Response(response_url)


# AdminView
class CreateUser(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = UsersSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class AdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            if request.user.is_superuser:
                return True
            else:
                raise PermissionDenied(
                    {'Message': 'Only superusers have access to this view.'})
        else:
            raise PermissionDenied({'Message': 'Method not supported'})

# AdminView


class ViewUsers(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = UsersSerializer
    permission_classes = [AdminPermission, permissions.IsAuthenticated]
    authentication_classes = [authentication.BasicAuthentication]

    def get_queryset(self):
        return Users.objects.filter(is_superuser=False)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({'Error': 'No users found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return super().list(request, *args, **kwargs)

# AdminView


class DeleteUser(generics.GenericAPIView, mixins.DestroyModelMixin):
    queryset = Users.objects.all()
    permission_classes = [AdminPermission, permissions.IsAuthenticated]
    authentication_classes = [authentication.BasicAuthentication]
    serializer_class = UsersSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get_object(self):
        pk = self.kwargs.get('pk')
        try:
            user = Users.objects.get(pk=pk)
            return user
        except Users.DoesNotExist:
            raise NotFound({'Error': 'User does not exist.'})

# AdminView or UserView


class ViewUser(generics.GenericAPIView, mixins.RetrieveModelMixin):
    queryset = Users.objects.all()
    serializer_class = ViewUserSerializer
    lookup_field = 'pk'
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def get_object(self):
        pk = self.kwargs.get('pk')
        try:
            user = Users.objects.get(pk=pk)
            return user
        except Users.DoesNotExist:
            raise NotFound({'Error': 'User does not exist.'})

# UserView


class CreateTask(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = UserTaskSerializer
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return Response({'Error': 'You are not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

# UserView only


class ViewTask(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = ViewTaskSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return Response({"Error": "You are not logged in"}, status=status.HTTP_403_FORBIDDEN)
        elif self.request.user.is_superuser:
            raise PermissionDenied(
                {"Error": "Superusers are not allowed to access this view."}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return self.list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = UserTask.objects.filter(user=self.request.user).exists()
        if not queryset:
            raise NotFound({'Message': 'You have no task'})
        else:
            queryset = UserTask.objects.filter(user=self.request.user)
            return queryset


class DeleteTask(generics.GenericAPIView, mixins.DestroyModelMixin):
    serializer_class = ViewTaskSerializers
    lookup_field = 'pk'
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            return Response({"Error": "Admin are not allowed here"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return self.destroy(request, *args, **kwargs)

    def get_queryset(self):
        queryset = UserTask.objects.filter(user=self.request.user)
        if not queryset:
            return NotFound({"Message": "No task for you"})
        else:
            return queryset

    def get_object(self):
        try:
            task = UserTask.objects.get(
                pk=self.kwargs['pk'], user=self.request.user)
            return task
        except UserTask.DoesNotExist:
            raise NotFound({"Error": "Task not found"})

# AdminView or UserView
class UpdateProfile(generics.GenericAPIView, mixins.UpdateModelMixin):
    pass