# Generated by Django 5.1.5 on 2025-02-26 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_shopper_stripe_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='country',
            field=models.CharField(default='BE', max_length=24),
        ),
    ]
