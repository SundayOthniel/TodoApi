from rest_framework import serializers
from .models import UserTask, Users, ProfilePicture
from django.core.files import File
import os
from django.conf import settings


class UsersSerializer(serializers.ModelSerializer):
    date_joined = serializers.SerializerMethodField()
    phone = serializers.CharField(max_length=11)
    is_superuser = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True)
    c_password = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email', 'phone',
                  'password', 'date_joined', 'is_superuser', 'c_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['c_password']:
            raise serializers.ValidationError(
                'Be sure if password and comfirm password are the same')
        elif Users.objects.filter(phone=attrs['phone']).exists():
            raise serializers.ValidationError(
                'Phone number already exist. Please use a different phone number.'
            )
        else:
            return attrs

    def validate_phone(self, phone):
        if len(phone) > 11:
            raise serializers.ValidationError(
                'Be sure your input is less than 11 digits')
        else:
            return phone

    def create(self, validated_data):
        user = Users(
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            email=validated_data.get('email'),
            phone=validated_data.get('phone'),
            date_joined=validated_data.get('date_joined')
        )
        user.set_password(validated_data.get('password'))
        user.save()
        self.assign_default_profile_picture(user)
        return user

    def assign_default_profile_picture(self, user):
        default_img_path = os.path.join(
            settings.BASE_DIR, 'todoApp', 'static', 'default-avatar.jpg')
        if not os.path.exists(default_img_path):
            raise FileNotFoundError(
                'Default profile picture not found at the specified path.')

        else:
            with open(default_img_path, 'rb') as img_file:
                ProfilePicture.objects.update_or_create(
                    user=user,
                    defaults={'profile_pic': File(
                        img_file, name='default_profile_picture.jpg')}
                )

    def get_date_joined(self, obj):
        date = obj.date_joined.strftime('%B, %Y') if obj.date_joined else None
        return date


class ViewUserSerializer(serializers.ModelSerializer):
    date_joined = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = ['id', 'first_name', 'last_name',
                  'email', 'phone', 'date_joined']

    def get_date_joined(self, obj):
        date = obj.date_joined.strftime('%B, %Y') if obj.date_joined else None
        return date


class UserTaskSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    title = serializers.CharField(max_length=255)

    class Meta:
        model = UserTask
        fields = ['title', 'todo', 'user']

    def validate_title(self, title):
        if UserTask.objects.filter(title=title).exists():
            raise serializers.ValidationError(
                'This Task already exist, create a different task')
        else:
            return title


class ViewTaskSerializers(serializers.ModelSerializer):
    date_created = serializers.SerializerMethodField()
    last_edit = serializers.SerializerMethodField()

    class Meta:
        model = UserTask
        fields = ['title', 'todo', 'date_created', 'last_edit']

    def get_date_created(self, obj):
        return obj.date_created.strftime('%Y-%m-%d %H:%M:%S') if obj.date_created else None

    def get_last_edit(self, obj):
        return obj.last_edit.strftime('%Y-%m-%d %H:%M:%S') if obj.last_edit else None