# Generated by Django 5.1.5 on 2025-02-26 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_cart_ordered_cart_ordered_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='ordered',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='ordered_date',
        ),
    ]
