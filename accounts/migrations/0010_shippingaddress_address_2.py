# Generated by Django 5.1.5 on 2025-02-28 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_remove_shippingaddress_address_2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='address_2',
            field=models.CharField(blank=True, help_text='Bâtiment, étage, appartement, etc.', max_length=1024, null=True),
        ),
    ]
