# Generated by Django 5.1.3 on 2024-11-19 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedstock', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=20),
        ),
    ]
