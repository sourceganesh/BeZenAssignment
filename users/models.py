from ast import BinOp
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.conf.urls.static import static


class UserProfile(models.Model):

    GENDER_CHOICES = (
        (1, "Male"),
        (2, "Female"),
    )

    user            = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    avatar          = models.ImageField(upload_to="users/profiles/avatars/", null=True, blank=True)
    dob             = models.DateField(null=True, blank=True)
    gender          = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True, blank=True)
    bio             = models.CharField(max_length=400,blank=True, null=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    @property
    def get_avatar(self):
        return self.avatar.url if self.avatar else static('assets/default-profile-picture.png')
    
    def __str__(self):
        return '{}'.format(self.user)