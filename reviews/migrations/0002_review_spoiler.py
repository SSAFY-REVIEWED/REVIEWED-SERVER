# Generated by Django 3.2.12 on 2022-05-24 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='spoiler',
            field=models.BooleanField(default=False),
        ),
    ]
