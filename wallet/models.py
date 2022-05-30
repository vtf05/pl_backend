from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class UserWallet (models.Model):
    user                = models.ForeignKey(User, on_delete = models.CASCADE)                
    cur_balance         = models.IntegerField(default = 0)   
    subscribe           = models.BooleanField(default = False)


class Payment(models.Model):
    user                = models.ForeignKey(User, on_delete = models.CASCADE) 
    payment_amount      = models.CharField(max_length=25)
    payment_id          = models.CharField(max_length=100)
    isPaid              = models.BooleanField(default=False)
    payment_date        = models.DateTimeField(auto_now=True)

        
