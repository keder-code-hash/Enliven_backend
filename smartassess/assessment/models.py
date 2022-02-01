from django.db import models
from users.models import Course, Register


class Exam(models.Model):
    _id = models.BigIntegerField(unique=True, primary_key=True, blank=False)
    exam_name = models.CharField(blank=False)
    marks = models.IntegerField(blank=False)
    course = models.CharField(blank=False)
    description = models.CharField()
    duration = models.TimeField(blank=False)
    created_by = models.ManyToManyField(Register)
    created_at = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    _id = models.BigIntegerField(unique=True, primary_key=True, blank=False)
    exam_id = models.BigIntegerField(blank=False)
    question = models.CharField(blank=False)
    standard_ans = models.CharField(blank=False)
    created_by = models.ManyToManyField(Register)
    created_at = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    _id = models.BigIntegerField(unique=True, primary_key=True, blank=False)
    exam_id = models.BigIntegerField(blank=False)
    question_id = models.BigIntegerField(unique=True, blank=False)
    answer = models.CharField(blank=False)
    answer_duration = models.TimeField(blank=False)
    answered_by = models.ManyToManyField(Register)
    answered_at = models.DateTimeField(auto_now_add=True)


class Evaluation(models.Model):
    _id = models.BigIntegerField(unique=True, primary_key=True, blank=False)
    exam_id = models.BigIntegerField(blank=False)
    question_id = models.BigIntegerField(unique=True, blank=False)
    answer_id = models.BigIntegerField(unique=True, blank=False)
    remarks = models.CharField()
    score = models.IntegerField(blank=False)
    match_percentage = models.FloatField(blank=False)


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

"""
