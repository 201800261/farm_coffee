# Generated by Django 3.2.3 on 2022-04-24 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm_coffee_app', '0005_products_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='image',
            field=models.ImageField(default=0, upload_to='farm_coffee_app/static/farm_coffee_app/images'),
        ),
    ]
