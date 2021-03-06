# Generated by Django 3.2.3 on 2022-05-11 11:06

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('category', models.CharField(blank=True, max_length=50, null=True)),
                ('price', models.FloatField()),
                ('image', models.ImageField(default='static/farm_coffee_app/images/default.jpg', upload_to='static/farm_coffee_app/images')),
                ('availability', models.BooleanField()),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('reviews_id', models.AutoField(primary_key=True, serialize=False)),
                ('rating', models.FloatField()),
                ('review_description', models.TextField()),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('product_fk_product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to='farm_coffee_app.product')),
                ('users_fk_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Quantity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(null=True)),
                ('item', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='farm_coffee_app.item')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farm_coffee_app.profile'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('status_name', models.CharField(choices=[('ORD', 'Ordering'), ('PRE', 'Preparing'), ('DEL', 'Delivering'), ('DED', 'Delivered')], default='ORD', max_length=50)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('street', models.CharField(max_length=150)),
                ('city', models.CharField(max_length=150)),
                ('province', models.CharField(max_length=150)),
                ('zip_code', models.CharField(max_length=150)),
                ('phone_number', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')])),
                ('order_created_time', models.DateTimeField(blank=True, null=True)),
                ('time_of_delivery', models.DateTimeField(blank=True, null=True)),
                ('delivery_completion', models.DateTimeField(blank=True, null=True)),
                ('payment_received', models.BooleanField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='farm_coffee_app.order'),
        ),
        migrations.AddField(
            model_name='item',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='farm_coffee_app.product'),
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='farm_coffee_app.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='farm_coffee_app.profile')),
            ],
        ),
    ]
