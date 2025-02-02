# Generated by Django 5.1.5 on 2025-01-30 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='variantIds',
        ),
        migrations.AddField(
            model_name='product',
            name='variants',
            field=models.ManyToManyField(blank=True, to='store.variant'),
        ),
    ]
