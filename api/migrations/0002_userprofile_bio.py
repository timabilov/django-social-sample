# Generated by Django 2.0 on 2018-12-05 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(default=''),
        ),
    ]
