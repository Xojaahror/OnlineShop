# Generated by Django 5.0 on 2023-12-19 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_alter_brands_name_alter_color_name_alter_size_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='products_cate', to='home.category'),
        ),
    ]