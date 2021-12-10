# Generated by Django 3.2.3 on 2021-12-09 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_auto_20211209_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=2, default=100.0, max_digits=8),
            preserve_default=False,
        ),
    ]