from django.contrib import admin
from .models import Subject, Chapter, Module, MCQ

class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0

class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 0

class ChapterAdmin(admin.ModelAdmin):
    inlines = [ModuleInline]
    list_display = ['name', 'subject', 'is_completed']
    list_filter = ['subject']

class SubjectAdmin(admin.ModelAdmin):
    inlines = [ChapterInline]
    list_display = ['name']

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Module)
admin.site.register(MCQ)