# Generated by Django 4.2.4 on 2023-09-08 09:15

import apps.product.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_productline_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productline',
            name='order',
            field=apps.product.fields.OrderField(blank=True),
        ),
    ]
