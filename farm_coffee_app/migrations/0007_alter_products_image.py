# Generated by Django 3.2.3 on 2022-04-24 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm_coffee_app', '0006_alter_products_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='image',
            field=models.ImageField(default=0, upload_to='farm_coffee_app\\static\x0carm_coffee_app\\images'),
        ),
    ]
