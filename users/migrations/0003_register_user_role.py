# Generated by Django 3.2.6 on 2022-01-29 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='user_role',
            field=models.CharField(blank=True, default='s', max_length=5),
        ),
    ]