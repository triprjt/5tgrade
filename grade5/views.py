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
def get_content_in_module(request, module_id, content_type):
    module = get_object_or_404(Module, id=module_id, user=request.user)
    content = module.content

    if content_type.upper() == 'TEXT':
        serializer = TextFieldSerializer(content.text)

    elif content_type.upper() == 'IMAGE':
        serializer = ImageFieldSerializer(content.image)

    elif content_type.upper() == 'VIDEO':
        serializer = VideoFieldSerializer(content.video)

    elif content_type.upper() == 'MCQ':
        mcq_set = get_object_or_404(MCQSet, id=content.mcq_set.id)
        serializer = MCQSetSerializer(mcq_set)

    else:
        return Response({"status": "Invalid content type"}, status=400)

    return Response(serializer.data)


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

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def is_module_completed(request, module_id):
    module = get_object_or_404(Module, id=module_id, user=request.user)
    content = module.content

    if content.text and not content.text.is_completed:
        return Response({"status": "Module not completed, text content pending"}, status=200)

    if content.image and not content.image.is_completed:
        return Response({"status": "Module not completed, image content pending"}, status=200)

    if content.video and not content.video.is_completed:
        return Response({"status": "Module not completed, video content pending"}, status=200)

    if content.mcq and not content.mcq_set.is_completed:
        return Response({"status": "Module not completed, MCQ content pending"}, status=200)

    return Response({"status": "Module is completed"}, status=200)
    
