from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('subjects/', views.getSubjects),  # Pluralized
    path('subjects/<int:subject_id>/', views.getChaptersInASubject),
    path('chapter_modules/<int:chapter_id>/', views.getModulesInAChapter),
    path('module_content/<int:module_id>/<str:content_type>/', views.get_content_in_module),  # Added 'content_type'
    path('update_progress_of_content/<int:module_id>/<str:content_type>/', views.update_progress_of_content),
    path('isModuleCompleted/<int:module_id>', views.is_module_completed),
    path('api-token-auth/', obtain_auth_token , name='api_token_auth'),
]
