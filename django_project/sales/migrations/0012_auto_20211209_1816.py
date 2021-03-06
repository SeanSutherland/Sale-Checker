# Generated by Django 3.2.3 on 2021-12-09 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0011_auto_20211209_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='last_price',
            field=models.DecimalField(decimal_places=2, default=models.DecimalField(decimal_places=2, max_digits=8), max_digits=8),
        ),
        migrations.AlterField(
            model_name='item',
            name='regular_price',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]
