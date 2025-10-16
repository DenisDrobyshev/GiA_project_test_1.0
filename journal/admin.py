from django.contrib import admin
from .models import JournalIssue, Article, EditorialBoard, ContactMessage, JournalInfo, ArchiveYear


@admin.register(JournalIssue)
class JournalIssueAdmin(admin.ModelAdmin):
    list_display = ['year', 'number', 'title', 'is_current', 'created_at']
    list_filter = ['year', 'is_current']
    search_fields = ['title', 'description']
    ordering = ['-year', '-number']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'authors', 'issue', 'is_published', 'created_at']
    list_filter = ['is_published', 'issue__year', 'created_at']
    search_fields = ['title', 'authors', 'abstract']
    ordering = ['-created_at']


@admin.register(EditorialBoard)
class EditorialBoardAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'institution', 'order']
    list_filter = ['position']
    search_fields = ['name', 'position', 'institution']
    ordering = ['order', 'name']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at', 'is_processed']
    list_filter = ['is_processed', 'created_at']
    search_fields = ['name', 'email', 'message']
    ordering = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(JournalInfo)
class JournalInfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'issn_print', 'issn_online', 'publisher']


@admin.register(ArchiveYear)
class ArchiveYearAdmin(admin.ModelAdmin):
    list_display = ('start_year', 'end_year', 'slug', 'is_active') 
    list_filter = ('is_active',) 
    search_fields = ('slug',) 
    ordering = ('-end_year',) 