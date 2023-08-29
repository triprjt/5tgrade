from rest_framework import serializers
from .models import Subject, Chapter, Module, MCQ, TextField, ImageField, VideoField, Content, MCQSet

class MCQSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCQ
        fields = '__all__'

class TextFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextField
        fields = '__all__'

class ImageFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageField
        fields = '__all__'

class VideoFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoField
        fields = '__all__'

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'name', 'is_completed',]

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']

class MCQSetSerializer(serializers.ModelSerializer):
    questions = MCQSerializer(many=True, read_only=True)

    class Meta:
        model = MCQSet
        fields = ['id', 'questions', 'is_completed']

