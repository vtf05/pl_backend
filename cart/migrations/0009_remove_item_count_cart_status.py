# Generated by Django 4.0.4 on 2022-07-12 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0008_item_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='count',
        ),
        migrations.AddField(
            model_name='cart',
            name='status',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]