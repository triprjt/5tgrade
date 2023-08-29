from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('subjects/', views.getSubjects),  # Pluralized
    path('subjects/<int:subject_id>/', views.getChaptersInASubject),
    path('chapter_modules/<int:chapter_id>/', views.getModulesInAChapter),
    path('module_content/<int:module_id>/', views.get_content_in_module, name='get_content_in_module'),
    
    # udpate progress of text, image, video, MCQ content 
    path('update_progress_of_content/<int:module_id>/<str:content_type>/', views.update_progress_of_content),

    # update progress of module, chapter, subject
    path('update_module_progress/<int:module_id>/', views.update_module_progress),
    path('update_chapter_progress/<int:chapter_id>/', views.update_chapter_progress),
    path('update_subject_progress/<int:subject_id>/', views.update_subject_progress),
    
    # login
    path('api-token-auth/', obtain_auth_token , name='api_token_auth'),
]
