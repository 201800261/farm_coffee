# Generated by Django 3.2.3 on 2022-04-26 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm_coffee_app', '0011_products_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='pub_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
