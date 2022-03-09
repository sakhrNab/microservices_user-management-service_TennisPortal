from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# from rest_framework.validators import UniqueValidator
# from . import serializers

class GenericFileUpload(models.Model):
    file_upload = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_upload}"

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, first_name, last_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email,  first_name, last_name, password, **other_fields)

    def create_user(self, email, first_name, last_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email,
                          first_name=first_name, last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

#### this is the method which creates the superuser
#### email, user_name, password
class NewUser(AbstractBaseUser, PermissionsMixin):

    # email = models.EmailField(_('email address'), unique=True)
    # user_name = models.CharField(max_length=150, unique=True)
    # first_name = models.CharField(max_length=150, blank=True)
    class Meta:
        verbose_name_plural="1. NewUser"
    ## permission roles - given by django
    username = None
    email= models.EmailField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=100)
    start_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    about = models.TextField(_(
        'about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True) # change this later to true
    is_online = models.DateTimeField(default=timezone.now)
    date_created=models.DateTimeField(default=timezone.now)


    ####
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

# class DeleteUser(AbstractBaseUser)Ö




class UserProfile(models.Model):
    class Meta:
        verbose_name_plural="2. Tennisplayer"

    #### the fields to be serialized and deserialized
    GENDER_CHOICE = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    SKILL_LEVEL = (
        ('1', 'Novice'),
        ('2', 'Advanced Beginner'),
        ('3', 'Competent'),
        ('4', 'Proficient'),
        ('5', 'Expert')
    )
    GAME_TYPE = (
        ('B', 'Badminton'),
        ('PT', 'Paddle tennis'),
        ('S', 'Squash'),
        ('TT', 'Table Tennis'),
        ('T', 'Tennis')
    )

    user_profile = models.OneToOneField(NewUser,
                                related_name="user_profile",
                                on_delete=models.CASCADE)

    country = models.CharField(max_length=100)

    profile_picture = models.ForeignKey(
        GenericFileUpload, related_name="user_image", on_delete=models.SET_NULL, null=True, blank=True
    )

    address = models.CharField(max_length=100)
    address_2 = models.CharField(null=True, max_length=100)
    mobile_no = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    age = models.CharField(null=True,blank=True, max_length=10)
    skill_level = models.CharField(max_length=10, choices=SKILL_LEVEL)
    game_type = models.CharField(max_length=20, choices=GAME_TYPE)
    password = models.CharField(max_length=100)
    # confirm_password = models.CharField(max_length=100)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICE)
    # date_created=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return " {}".format(self.user_profile)

class GameCategory(models.Model):
    title=models.CharField(max_length=150) # tennis
    description=models.TextField()

    # class meta is for modifications
    class Meta:
        verbose_name_plural="2. Games Categories"

    def __str__(self):
        return self.title

# a game without a GameCategory can't exist
class Game(models.Model):
    class Meta:
        verbose_name_plural="3. Games"
    category=models.ForeignKey(GameCategory, on_delete=models.CASCADE)
    tennis_player=models.ForeignKey(NewUser, on_delete=models.CASCADE)
    title=models.CharField(max_length=150)
    description=models.TextField()

    def __str__(self):
        return self.title
