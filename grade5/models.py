from django.db import models

# Subject model
class Subject(models.Model):
    name = models.CharField(max_length=100)

# Chapter model
class Chapter(models.Model):
    subject = models.ForeignKey(Subject, related_name='chapters', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False)

# TextField model
class TextField(models.Model):
    text = models.TextField(default="")
    is_completed = models.BooleanField(default=False)

# ImageField model
class ImageField(models.Model):
    image = models.URLField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)

# VideoField model
class VideoField(models.Model):
    video = models.URLField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)

# MCQ model
class MCQ(models.Model):
    question_title = models.CharField(max_length=255)
    choice1 = models.CharField(max_length=255)
    choice2 = models.CharField(max_length=255)
    choice3 = models.CharField(max_length=255)
    choice4 = models.CharField(max_length=255)
    correct_choice = models.IntegerField()  # 1, 2, 3, or 4
    is_completed = models.BooleanField(default=False)

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
    mcq = models.OneToOneField(MCQ, null=True, blank=True, on_delete=models.CASCADE)

# Module model
class Module(models.Model):
    chapter = models.ForeignKey(Chapter, related_name='modules', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    content = models.ForeignKey(Content, related_name="modules", on_delete=models.CASCADE)
