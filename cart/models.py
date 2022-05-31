from django.db import models
from django.contrib.auth import get_user_model  

User = get_user_model()

class Item(models.Model):
    name        = models.CharField( max_length=50 ,null = True ,blank= True)
    image       = models.ImageField(default="default.jpg" , upload_to='item_image',blank=True,null = True)
    price       = models.IntegerField(default = 0 ,null = True ,blank= True )
    description = models.TextField( null = True ,blank= True)

class Cart(models.Model) :
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    items       =  models.ManyToManyField(Item)
    price       = models.IntegerField(default = 0, null = True ,blank= True)
    proccessed  = models.BooleanField(default = False , null = True , blank=True)
    cashback    = models.IntegerField(default = 0, null = True ,blank= True)
    paid        = models.BooleanField( default = False , null = True , blank=True)

# Create your models here.
