# Generated by Django 4.0.4 on 2022-05-25 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='phoneModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Mobile', models.IntegerField()),
                ('isVerified', models.BooleanField(default=False)),
                ('counter', models.IntegerField(default=0)),
            ],
        ),
    ]
