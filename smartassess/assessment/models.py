from tokenize import blank_re
from django.db import models
from users.models import Course, Register


class Exam(models.Model):
    exam_name = models.CharField(max_length=130, blank=False)
    marks = models.IntegerField(blank=False)
    course = models.CharField(max_length=130, blank=False)
    description = models.CharField(
        max_length=130,
    )
    duration = models.TimeField(blank=False)
    created_by = models.ManyToManyField(Register)
    created_at = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    exam_id = models.BigIntegerField(blank=False)
    question = models.CharField(max_length=130, blank=False)
    standard_ans = models.CharField(max_length=130, blank=False)
    created_by = models.ManyToManyField(Register)
    created_at = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    exam_id = models.BigIntegerField(blank=False)
    question_id = models.BigIntegerField(unique=True, blank=False)
    answer = models.CharField(max_length=130, blank=False)
    answer_duration = models.TimeField(blank=False)
    answered_by = models.ManyToManyField(Register)
    answered_at = models.DateTimeField(auto_now_add=True)


class Evaluation(models.Model):
    exam_id = models.BigIntegerField(blank=False)
    question_id = models.BigIntegerField(unique=True, blank=False)
    answer_id = models.BigIntegerField(unique=True, blank=False)
    remarks = models.CharField(
        max_length=130,
    )
    score = models.IntegerField(blank=False)
    match_percentage = models.FloatField(blank=False)


class Monitor(models.Model):
    exam_id = models.BigIntegerField(blank=False)
    sudent_id = models.EmailField(blank=False)
    image = models.ImageField(blank=False)
    taken_at = models.DateTimeField(auto_now_add=True)
    is_original = models.BooleanField(default=False)


"""
Evaluation
    id
    exam_id
    question_id 
    answer_id
    remarks
    marks/score
    matched_percentage

Answer
    id 
    exam_id
    question_id
    ansewer
    answered_duration
    answered_by
    answered_at

Exam
    id
    exam_name
    marks
    course
    desc
    time/duration
    created_by
    created_at
    
Question
    id
    exam_id
    question
    standard_ans 
    question_created_by 
    created_at

Monitor
    exam_id
    std_id
    image
    taken_at

"""
