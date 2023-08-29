from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .models import Subject, Chapter, Module, Content, TextField, ImageField, VideoField, MCQ, MCQSet
from .serializers import SubjectSerializer, ChapterSerializer, ModuleSerializer, MCQSerializer, TextFieldSerializer, ImageFieldSerializer, VideoFieldSerializer, MCQSetSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication

class ModuleNotCompletedException(Exception):
    pass

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getSubjects(request):
    subjects = Subject.objects.filter(user=request.user)
    serializer = SubjectSerializer(subjects, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getChaptersInASubject(request, subject_id):
    chapters = Chapter.objects.filter(user=request.user, subject_id=subject_id)
    serializer = ChapterSerializer(chapters, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getModulesInAChapter(request, chapter_id):
    modules = Module.objects.filter(chapter_id=chapter_id, user=request.user)
    serializer = ModuleSerializer(modules, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_content_in_module(request, module_id):
    module = get_object_or_404(Module, id=module_id, user=request.user)
    content = module.content
    content_list = []

    if content.text:
        text_serializer = TextFieldSerializer(content.text)
        content_list.append({'type': 'text', 'body': text_serializer.data})

    if content.image:
        image_serializer = ImageFieldSerializer(content.image)
        content_list.append({'type': 'image', 'body': image_serializer.data})

    if content.video:
        video_serializer = VideoFieldSerializer(content.video)
        content_list.append({'type': 'video', 'body': video_serializer.data})

    if content.mcq_set:
        mcq_set = get_object_or_404(MCQSet, id=content.mcq_set.id)
        mcq_serializer = MCQSetSerializer(mcq_set)
        content_list.append({'type': 'mcq', 'body': mcq_serializer.data})

    return Response(content_list)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_progress_of_content(request, module_id, content_type):
    module = get_object_or_404(Module, id=module_id, user=request.user)
    content = module.content

    if content_type.upper() == 'TEXT':
        content.text.is_completed = True
        content.text.save()

    elif content_type.upper() == 'IMAGE':
        content.image.is_completed = True
        content.image.save()

    elif content_type.upper() == 'VIDEO':
        content.video.is_completed = True
        content.video.save()

    elif content_type.upper() == 'MCQ':
        content.mcq_set.is_completed = True
        content.mcq_set.save()

    else:
        return Response({"status": "Invalid content type"}, status=400)

    return Response({"status": f"{content_type} marked as completed"}, status=200)

def _is_module_completed(module):
    content = module.content

    if content.text and not content.text.is_completed:
        raise ModuleNotCompletedException("Module not completed, text content pending")

    if content.image and not content.image.is_completed:
        raise ModuleNotCompletedException("Module not completed, image content pending")

    if content.video and not content.video.is_completed:
        raise ModuleNotCompletedException("Module not completed, video content pending")

    if content.mcq_set and not content.mcq_set.is_completed:
        raise ModuleNotCompletedException("Module not completed, MCQ content pending")

    return True
    
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_module_progress(request, module_id):
    module = get_object_or_404(Module, id=module_id, user=request.user)
    
    try:
        if _is_module_completed(module):
            module.is_completed = True
            module.save()
            return Response({"status": "Module is completed"}, status=200)
    except ModuleNotCompletedException as e:
        return Response({"status": str(e)}, status=400)

def _is_chapter_completed(chapter):
    modules = Module.objects.filter(chapter=chapter)
    for module in modules:
        if not _is_module_completed(module):
            return False
    return True

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_chapter_progress(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id, user=request.user)
    if _is_chapter_completed(chapter):
        chapter.is_completed = True
        chapter.save()
        return Response({"status": "Chapter is completed"}, status=200)
    else:
        return Response({"status": "Chapter is not completed"}, status=400)

def _is_subject_completed(subject):
    chapters = Chapter.objects.filter(subject=subject)
    for chapter in chapters:
        if not _is_chapter_completed(chapter):
            return False
    return True

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_subject_progress(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id, user=request.user)
    if _is_subject_completed(subject):
        subject.is_completed = True
        subject.save()
        return Response({"status": "Subject is completed"}, status=200)
    else:
        return Response({"status": "Subject is not completed"}, status=400)

