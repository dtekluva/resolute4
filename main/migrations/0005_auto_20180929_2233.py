# Generated by Django 2.0 on 2018-09-29 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]