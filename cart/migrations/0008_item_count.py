# Generated by Django 4.0.4 on 2022-07-10 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]