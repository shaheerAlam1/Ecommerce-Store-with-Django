# Generated by Django 4.0 on 2021-12-26 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_cart_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='user',
        ),
    ]
