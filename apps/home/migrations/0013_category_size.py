# Generated by Django 5.0 on 2023-12-26 16:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_brands_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.size'),
        ),
    ]