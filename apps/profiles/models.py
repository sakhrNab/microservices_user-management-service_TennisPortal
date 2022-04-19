from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

import user_management
from apps.common.models import TimeStampedUUIDModel

User = get_user_model()


class Gender(models.TextChoices):
    MALE = "Male", _("Male")
    FEMALE = "Female", _("Female")
    OTHER = "Other", _("Other")


class SkillLevel(models.TextChoices):

    NOVICE = "Novice", _("Novice")
    ADVANCED_BEGINNER = "Advanced Beginner", _("Advanced Beginner")
    COMPETENT = "Competent", _("Competent")
    PROFICIENT = "Proficient", _("Proficient")
    EXPERT = "Expert", _("Expert")


class GameType(models.TextChoices):

    BADMINTON = "Badminton", _("Badminton")
    PADDLE_TENNIS = "Paddle Tennis", _("Paddle Tennis")
    SQUASH = "Squash", _("Sqaush")
    TABLE_TENNIS = "Table Tennis", _("Table Tennis")
    TENNIS = "Tennis", _("Tennis")


class Profile(TimeStampedUUIDModel):

    # pkid
    # id
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)

    phone_number = models.CharField(
        verbose_name=_("Phone Number"), max_length=30, default="4916319787"
    )

    zip_code = models.CharField(max_length=10)

    profile_photo = models.ImageField(default='/imgs/tennis_player_img.png',
        verbose_name=_("Profile Photo"))

    gender = models.CharField(
        verbose_name=_("Gender"),
        choices=Gender.choices,
        default=Gender.OTHER,
        max_length=20,
    )

    country = CountryField(
        verbose_name=_("Country"), default="DE", blank=False, null=False
    )

    city = models.CharField(
        verbose_name=_("City"),
        max_length=180,
        default="Berlin",
        blank=False,
        null=False,
    )

    region = models.CharField(verbose_name=_("Region"),
                              max_length=100,
                              default="Berlin",
                              blank=False,
                              null=False,)

    age = models.CharField(
        verbose_name=_("Age"), null=True,blank=True, max_length=10
    )
    skill_level = models.CharField(verbose_name=_("Skill Level"),
                                   max_length=20, choices=SkillLevel.choices,
                                   default=SkillLevel.NOVICE)

    game_type = models.CharField(max_length=20, choices=GameType.choices, default=GameType.TENNIS)
    rating = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    # rating = models.IntegerField(
    #     verbose_name=_("User Rating"), default=0, null=True, blank=True)

    num_reviews = models.IntegerField(
        verbose_name=_("Number of Reviews"), default=0, null=True, blank=True
    )

    about_me = models.TextField(
        verbose_name=_("About me"), default="say something about yourself"
    )

    is_opponent = models.BooleanField(verbose_name=_("Opponent"),
                                      default=True)

    address = models.CharField(max_length=100)
    address_2 = models.CharField(blank=True, null=True, max_length=100)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def get_profile_photo(self):
        if self.profile_photo:
            return self.profile_photo.url
        else:
            return user_management.settings.base.STATIC_URL + 'img/default/meal.png'

# Blacklisted tokens

# Outstanding tokens



# class GameCategory(models.Model):
#     title=models.CharField(max_length=150) # tennis
#     description=models.TextField()
#
#     # class meta is for modifications
#     class Meta:
#         verbose_name_plural="2. Games Categories"
#
#     def __str__(self):
#         return self.title
#
# class Game(models.Model):
#     class Meta:
#         verbose_name_plural="3. Games"
#     category=models.ForeignKey(GameCategory, on_delete=models.CASCADE)
#     tennis_player=models.ForeignKey(User, on_delete=models.CASCADE)
#     title=models.CharField(max_length=150)
#     description=models.TextField()
#
#     def __str__(self):
#         return self.title