# Generated by Django 5.1.5 on 2025-03-08 10:31

import ckeditor.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('ordered', models.BooleanField(default=False)),
                ('ordered_date', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('orders', models.ManyToManyField(to='store.order')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('name_en', models.CharField(max_length=200, null=True)),
                ('name_fr', models.CharField(max_length=200, null=True)),
                ('name_nl', models.CharField(max_length=200, null=True)),
                ('slug', models.SlugField(blank=True, max_length=100, unique=True)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('available', models.BooleanField(default=True)),
                ('description', ckeditor.fields.RichTextField(blank=True)),
                ('description_en', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('description_fr', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('description_nl', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='products')),
                ('stripe_id', models.CharField(blank=True, max_length=90)),
                ('variants', models.ManyToManyField(blank=True, to='store.product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product'),
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='product_images')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='store.product')),
            ],
        ),
    ]
