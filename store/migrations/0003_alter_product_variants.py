# Generated by Django 5.1.5 on 2025-01-30 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_variant_remove_product_variantids_product_variants'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='variants',
            field=models.ManyToManyField(blank=True, to='store.product'),
        ),
    ]
