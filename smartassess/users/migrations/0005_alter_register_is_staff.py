# Generated by Django 3.2.6 on 2022-02-07 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_course_course_mentor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='is_staff',
            field=models.BooleanField(default=True),
        ),
    ]