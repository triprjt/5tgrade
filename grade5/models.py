from django.db import models
from django.contrib.postgres.fields import JSONField  
from django.contrib.auth.models import User

# Subject model
class Subject(models.Model):
    name = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # <-- Null allowed here

# Chapter model
class Chapter(models.Model):
    subject = models.ForeignKey(Subject, related_name='chapters', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # <-- Null allowed here

# TextField model
class TextField(models.Model):
    text = models.TextField(default="")
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # <-- Null allowed here

# ImageField model
class ImageField(models.Model):
    image = models.JSONField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # <-- Null allowed here

# VideoField model
class VideoField(models.Model):
    video = models.URLField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # <-- Null allowed here

# MCQSet model
class MCQSet(models.Model):
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # <-- Null allowed here

    def __str__(self):
        return f"MCQ Set {self.id}"

# MCQ model
class MCQ(models.Model):
    question_title = models.CharField(max_length=255)
    choice1 = models.CharField(max_length=255)
    choice2 = models.CharField(max_length=255)
    choice3 = models.CharField(max_length=255)
    choice4 = models.CharField(max_length=255)
    correct_choice = models.IntegerField()  
    mcq_set = models.ForeignKey(MCQSet, related_name='questions', null=True, on_delete=models.CASCADE)

# Content model
class Content(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('TEXT', 'Text'),
        ('IMAGE', 'Image'),
        ('VIDEO', 'Video'),
        ('MCQ', 'MCQ'),
    ]
    type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES)
    text = models.OneToOneField(TextField, null=True, blank=True, on_delete=models.CASCADE)
    image = models.OneToOneField(ImageField, null=True, blank=True, on_delete=models.CASCADE)
    video = models.OneToOneField(VideoField, null=True, blank=True, on_delete=models.CASCADE)
    mcq_set = models.OneToOneField(MCQSet, null=True, blank=True, on_delete=models.CASCADE)

# Module model
class Module(models.Model):
    chapter = models.ForeignKey(Chapter, related_name='modules', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    content = models.ForeignKey(Content, related_name="modules", on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # <-- Null allowed here
