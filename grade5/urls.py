from django.urls import path
from . import views

urlpatterns = [
    path('subjects/', views.getSubjects),  # Pluralized
    path('subjects/<int:subject_id>/', views.getChaptersInASubject),
    path('chapter_modules/<int:chapter_id>/', views.getModulesInAChapter),
    path('module_content/<int:module_id>/<str:content_type>/', views.get_content_in_module),  # Added 'content_type'
    path('update_progress_of_content/<int:module_id>/<str:content_type>/', views.update_progress_of_content),
    path('isModuleCompleted/<int:module_id>', views.is_module_completed),
]
