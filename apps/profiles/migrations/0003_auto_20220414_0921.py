# Generated by Django 3.2.7 on 2022-04-14 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20220414_0911'),
    ]

    operations = [

        migrations.AlterField(
            model_name='profile',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
