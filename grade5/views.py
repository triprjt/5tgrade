from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Subject, Chapter, Module, Content, TextField, ImageField, VideoField, MCQ
from .serializers import SubjectSerializer, ChapterSerializer, ModuleSerializer, MCQSerializer, TextFieldSerializer, ImageFieldSerializer, VideoFieldSerializer
@api_view(['GET'])
def getSubjects(request):
    subjects = Subject.objects.all()
    serializer = SubjectSerializer(subjects, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getChaptersInASubject(request, subject_id):
    chapters = Chapter.objects.filter(subject_id=subject_id)
    serializer = ChapterSerializer(chapters, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getModulesInAChapter(request, chapter_id):
    modules = Module.objects.filter(chapter_id=chapter_id)
    serializer = ModuleSerializer(modules, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_content_in_module(request, module_id, content_type):
    module = get_object_or_404(Module, id=module_id)
    
    if content_type.upper() == 'TEXT':
        content = get_object_or_404(TextField, id=module.content.text_id)
        serializer = TextFieldSerializer(content)

    elif content_type.upper() == 'IMAGE':
        content = get_object_or_404(ImageField, id=module.content.image_id)
        serializer = ImageFieldSerializer(content)
        
    elif content_type.upper() == 'VIDEO':
        content = get_object_or_404(VideoField, id=module.content.video_id)
        serializer = VideoFieldSerializer(content)
        
    elif content_type.upper() == 'MCQ':
        content = get_object_or_404(MCQ, id=module.content.mcq_id)
        serializer = MCQSerializer(content)

    else:
        return Response({"status": "Invalid content type"}, status=400)

    return Response(serializer.data)

@api_view(['PUT'])
def update_progress_of_content(request, module_id, content_type):
    module = get_object_or_404(Module, id=module_id)
    
    if content_type.upper() == 'TEXT':
        content = get_object_or_404(TextField, id=module.content.text_id)
        content.is_completed = True
        content.save()
        
    elif content_type.upper() == 'IMAGE':
        content = get_object_or_404(ImageField, id=module.content.image_id)
        content.is_completed = True
        content.save()
        
    elif content_type.upper() == 'VIDEO':
        content = get_object_or_404(VideoField, id=module.content.video_id)
        content.is_completed = True
        content.save()
        
    elif content_type.upper() == 'MCQ':
        content = get_object_or_404(MCQ, id=module.content.mcq_id)
        content.is_completed = True
        content.save()

    else:
        return Response({"status": "Invalid content type"}, status=400)

    return Response({"status": f"{content_type} marked as completed"}, status=200)