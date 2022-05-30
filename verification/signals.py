from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from users.models import User 
from .models import phoneModel
 
 
@receiver(post_save, sender=phoneModel)
def create_profile(sender, instance, created, **kwargs):
    if created:
        User.objects.create(mobile_no=instance)
  
