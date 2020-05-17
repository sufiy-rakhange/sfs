from django.db import models
from django.contrib.auth.models import User
from django import forms

# Create your models here.
class Department(models.Model):
    department_name = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.department_name}"

SEM_CHOICES = (
        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8)
    )

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    semester = models.IntegerField(choices=SEM_CHOICES)
    attendance = models.DecimalField(max_digits=5, decimal_places=2)
    batch = models.CharField(max_length=2)
    def __str__(self):
        return f"{self.user}  {self.department}  Sem: {self.semester}  {self.attendance} Batch:{self.batch}"

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    image = models.FileField(
        upload_to="feedback/profile_picture", default="feedback/myimages/default.png",
        blank=True, null=True
        )
    hod = models.BooleanField(default=False)
    coordinator = models.BooleanField(default=False)
    def __str__(self):
        return f"Prof. {self.user}  {self.department} {self.hod}  {self.coordinator}"

class Subject(models.Model):
    subject_name = models.CharField(max_length=50)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    semester = models.IntegerField(choices=SEM_CHOICES)
    practical = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.subject_name} {self.teacher}   {self.department}   {self.semester} Practical: {self.practical}"

class Batches(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    batch = models.CharField(max_length=2)
    
    class Meta:
        unique_together = ['subject', 'batch']
    def __str__(self):
        return f"{self.subject} {self.teacher} Batch:{self.batch}"

class Feedback(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    # Question 1
    q1 = models.IntegerField()
    # Question 2
    q2 = models.IntegerField()
    # Question 3
    q3 = models.IntegerField()
    # Question 4
    q4 = models.IntegerField()
    # Question 5
    q5 = models.IntegerField()
    # Question 6
    q6 = models.IntegerField()
    # Question 7
    q7 = models.IntegerField()
    # Question 8
    q8 = models.IntegerField(default=0)
    # Question 9
    q9 = models.IntegerField(default=0)
    # Question 10
    q10 = models.IntegerField(default=0)
    # Question 11
    q11 = models.IntegerField(default=0)
    # Question 12
    q12 = models.IntegerField(default=0)
    # Suggestions or Grievance
    suggestions = models.TextField(blank=True)
    def __str__(self):
        return f"""{self.student}  {self.subject}  {self.teacher}  {self.suggestions}"""
