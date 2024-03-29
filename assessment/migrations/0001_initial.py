# Generated by Django 3.2.6 on 2022-03-11 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_id', models.BigIntegerField()),
                ('question_id', models.BigIntegerField()),
                ('answer', models.CharField(max_length=130)),
                ('answer_duration', models.TimeField()),
                ('answered_at', models.DateTimeField(auto_now_add=True)),
                ('remarks', models.CharField(blank=True, default='', max_length=1)),
                ('marks', models.FloatField(default=0.0)),
                ('match_percentage', models.FloatField(default=0.0)),
                ('eval_details', models.CharField(blank=True, default='', max_length=600)),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_name', models.CharField(max_length=130, unique=True)),
                ('marks', models.IntegerField()),
                ('course', models.CharField(max_length=130)),
                ('description', models.CharField(max_length=130)),
                ('duration', models.TimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_evaluated', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ExamSubmissionDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_id', models.BigIntegerField()),
                ('student_id', models.EmailField(max_length=254)),
                ('is_submitted', models.BooleanField(default=False)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Monitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_id', models.BigIntegerField()),
                ('sudent_id', models.EmailField(max_length=254)),
                ('image', models.ImageField(upload_to='')),
                ('taken_at', models.DateTimeField(auto_now_add=True)),
                ('is_original', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_id', models.BigIntegerField()),
                ('question', models.CharField(max_length=130)),
                ('standard_ans', models.CharField(max_length=130)),
                ('qstn_marks', models.IntegerField(blank=True, default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
