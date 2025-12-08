from django.contrib import admin
# Импортируем mark_safe для отображения картинок в админке (опционально)
from django.utils.html import mark_safe 
from .models import JournalIssue, Article, EditorialBoard, ContactMessage, JournalInfo, ArchiveYear

# --- Inline для статей внутри выпуска ---
class ArticleInline(admin.StackedInline):
    """Позволяет добавлять/редактировать статьи прямо внутри страницы выпуска"""
    model = Article
    extra = 1  # Количество пустых форм для новых статей
    fields = ('title', 'authors', 'rubric', 'page_start', 'page_end', 'pdf_file', 'is_published')
    # show_change_link = True # Если нужно переходить к полному редактированию статьи


@admin.register(JournalIssue)
class JournalIssueAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'year', 'is_current', 'has_cover', 'has_pdf', 'created_at']
    list_filter = ['year', 'is_current']
    search_fields = ['number', 'year', 'volume'] # Убрал title, если его нет в модели, заменил на актуальные
    ordering = ['-year', '-number']
    
    # Подключаем Inline
    inlines = [ArticleInline]
    
    # Группировка полей для удобства (Fieldsets)
    fieldsets = (
        ('Основная информация', {
            'fields': ('year', 'volume', 'number', 'publication_date', 'is_current')
        }),
        ('Файлы', {
            'fields': ('cover', 'full_pdf'),
            'description': 'Загрузите обложку (JPG/PNG) и полный выпуск (PDF).'
        }),
    )

    # Кастомные методы для list_display
    def has_cover(self, obj):
        return bool(obj.cover)
    has_cover.boolean = True
    has_cover.short_description = "Обложка"

    def has_pdf(self, obj):
        return bool(obj.full_pdf)
    has_pdf.boolean = True
    has_pdf.short_description = "PDF"


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'authors', 'issue', 'rubric', 'has_pdf', 'is_published']
    list_filter = ['is_published', 'issue__year', 'rubric']
    search_fields = ['title', 'authors', 'abstract']
    ordering = ['-issue__year', 'issue__number', 'page_start'] # Сортировка по порядку в журнале
    
    autocomplete_fields = ['issue'] # Удобный поиск выпуска при редактировании статьи
    
    def has_pdf(self, obj):
        return bool(obj.pdf_file)
    has_pdf.boolean = True
    has_pdf.short_description = "PDF"


@admin.register(EditorialBoard)
class EditorialBoardAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'institution', 'order']
    list_filter = ['position']
    search_fields = ['name', 'position', 'institution']
    list_editable = ['order'] # Позволяет менять порядок прямо в списке
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
    # Обычно настройки журнала - это одна запись, запретим создавать дубли
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return True


@admin.register(ArchiveYear)
class ArchiveYearAdmin(admin.ModelAdmin):
    list_display = ('start_year', 'end_year', 'slug', 'is_active') 
    list_filter = ('is_active',) 
    search_fields = ('slug',) 
    ordering = ('-end_year',)
