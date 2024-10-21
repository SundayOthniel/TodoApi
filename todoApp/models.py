from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('Email is missing')
        elif not phone:
            raise ValueError('Phone is missing')
        else:
            phone = str(phone)
            user = self.model(phone=phone, email=email, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user
        
    def create_superuser(self, email, phone, password=None, **extra_fields):
        # Defaulf for extra fields can be define with .setdefault() and useful for consistency
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        elif extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        else:
            return self.create_user(email=email, phone=phone, password=password, **extra_fields)

class Users(AbstractBaseUser):
    phone = models.CharField(max_length=11, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    username = None
    
    objects = UserManager()
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'users'

class ProfilePicture(models.Model):
    user = models.OneToOneField(Users, related_name='user', on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='Profile pictures')
    class Meta:
        db_table = 'profile_pic'

class UserTask(models.Model):
    user = models.ForeignKey(Users, related_name='task', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False, null=False)
    todo = models.TextField()
    date_created = models.DateField(auto_now_add=True)
    last_edit = models.DateTimeField( auto_now=True)
    
    class Meta:
        db_table = 'todo'