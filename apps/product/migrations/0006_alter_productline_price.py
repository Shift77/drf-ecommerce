# Generated by Django 4.2.4 on 2023-09-07 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_alter_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productline',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
    ]
