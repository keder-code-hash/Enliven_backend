from django.db import models
from users.models import Course, Register


'''
Exam
    id
    exam_name
    marks
    course
    desc
    time
    created_by
    created_at
    
Question
    id
    exam_id
    question
    standard_ans 
    question_created_by 
    created_at

Answer
    id 
    exam_id
    question_id
    ansewer
    answered_duration
    answered_by
    answered_at

Evaluation
    id
    exam_id
    question_id 
    answer_id
    remarks
    marks
    matched_percentage


'''