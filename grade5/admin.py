from django.contrib import admin
from .models import Subject, Chapter, Module, TextField, ImageField, VideoField, MCQ, Content

# Inline classes for nested models
class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0

class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 0

# Admin classes for each model
class SubjectAdmin(admin.ModelAdmin):
    inlines = [ChapterInline]
    list_display = ['name']

class ChapterAdmin(admin.ModelAdmin):
    inlines = [ModuleInline]
    list_display = ['name', 'subject', 'is_completed']
    list_filter = ['subject']

class ModuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'chapter']
    list_filter = ['chapter']

class TextFieldAdmin(admin.ModelAdmin):
    list_display = ['text', 'is_completed']

class ImageFieldAdmin(admin.ModelAdmin):
    list_display = ['image', 'is_completed']

class VideoFieldAdmin(admin.ModelAdmin):
    list_display = ['video', 'is_completed']

class MCQAdmin(admin.ModelAdmin):
    list_display = ['question_title', 'correct_choice']

class ContentAdmin(admin.ModelAdmin):
    list_display = ['type']

# Register models and admin classes
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(TextField, TextFieldAdmin)
admin.site.register(ImageField, ImageFieldAdmin)
admin.site.register(VideoField, VideoFieldAdmin)
admin.site.register(MCQ, MCQAdmin)
admin.site.register(Content, ContentAdmin)
