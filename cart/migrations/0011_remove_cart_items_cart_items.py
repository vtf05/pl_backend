# Generated by Django 4.0.4 on 2022-07-13 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0010_remove_cart_items_cartitem_cart_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='items',
        ),
        migrations.AddField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(to='cart.cartitem'),
        ),
    ]