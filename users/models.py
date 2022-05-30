# Create your models here.

from django.db import models

from django.contrib.auth.models import AbstractUser

from django.utils.translation import gettext_lazy as _
from django.conf import settings
from datetime import date
from verification.models import phoneModel
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    username         = models.CharField( max_length=50 , null= True , blank= True)
    email            = models.EmailField(_('email address'), blank=True , null= True)
    profile_photo    = models.ImageField(default="default.jpg", upload_to='profile_image', blank=True,null = True)
    mobile           =  PhoneNumberField(unique=True)

    USERNAME_FIELD = 'mobile'
   
    REQUIRED_FIELDS = [ 'username' ,'first_name', 'last_name'] 
  

    def __str__(self):
        return "{}".format(self.username)    


