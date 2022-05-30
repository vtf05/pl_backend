from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from wallet.models import UserWallet
from django.contrib.auth import get_user_model
User = get_user_model()

 
@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if created:
        UserWallet.objects.create(user=instance)
  
