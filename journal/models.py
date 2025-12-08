import os
from django.db import models

# --- Вспомогательные функции для путей сохранения ---
def issue_cover_path(instance, filename):
    return f'covers/{instance.year}/{instance.number}/{filename}'

def issue_pdf_path(instance, filename):
    return f'issues/{instance.year}/{instance.number}/{filename}'

def article_pdf_path(instance, filename):
    return f'articles/{instance.issue.year}/{instance.issue.number}/{filename}'

# --- Основные модели ---

class JournalIssue(models.Model):
    """Модель выпуска журнала"""
    year = models.IntegerField(verbose_name="Год издания", default=2024)
    volume = models.CharField(max_length=50, verbose_name="Том (например, 67)", blank=True)
    number = models.CharField(max_length=50, verbose_name="Номер выпуска")
    publication_date = models.DateField(verbose_name="Дата выхода", blank=True, null=True)
    is_current = models.BooleanField(default=False, verbose_name="Текущий выпуск (на главной)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания записи")
    
    # Файлы
    cover = models.ImageField(upload_to=issue_cover_path, verbose_name="Обложка (картинка)", blank=True, null=True)
    full_pdf = models.FileField(upload_to=issue_pdf_path, verbose_name="Полный PDF выпуска", blank=True, null=True)

    def __str__(self):
        return f"{self.year}. Т.{self.volume}. №{self.number}"

    class Meta:
        verbose_name = "Выпуск"
        verbose_name_plural = "Выпуски"
        ordering = ['-year', '-number']


class Article(models.Model):
    """Модель отдельной статьи"""
    issue = models.ForeignKey(JournalIssue, on_delete=models.CASCADE, related_name='articles', verbose_name="Выпуск")
    
    title = models.CharField(max_length=500, verbose_name="Название статьи")
    rubric = models.CharField(max_length=200, verbose_name="Рубрика", blank=True)
    authors = models.CharField(max_length=500, verbose_name="Авторы")
    abstract = models.TextField(verbose_name="Аннотация", blank=True)
    
    # Файл
    pdf_file = models.FileField(upload_to=article_pdf_path, verbose_name="PDF файл статьи", blank=True, null=True)
    
    # Дополнительно
    page_start = models.IntegerField(verbose_name="Стр. начало", default=0)
    page_end = models.IntegerField(verbose_name="Стр. конец", default=0)
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title[:50] + "..."

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['page_start']


class EditorialBoard(models.Model):
    """Редакционная коллегия"""
    name = models.CharField(max_length=200, verbose_name="ФИО")
    position = models.CharField(max_length=200, verbose_name="Должность/Статус", blank=True)
    institution = models.CharField(max_length=300, verbose_name="Организация", blank=True)
    photo = models.ImageField(upload_to='editorial/', verbose_name="Фото", blank=True, null=True)
    order = models.IntegerField(default=0, verbose_name="Порядок сортировки")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Член редсовета"
        verbose_name_plural = "Редакционная коллегия"
        ordering = ['order', 'name']


class ContactMessage(models.Model):
    """Сообщения из формы обратной связи"""
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True, null=True) 
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")
    is_processed = models.BooleanField(default=False, verbose_name="Обработано")

    def __str__(self):
        return f"Сообщение от {self.name} ({self.created_at})"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения с сайта"


class JournalInfo(models.Model):
    """Общая информация о журнале (ISSN и прочее)"""
    title = models.CharField(max_length=200, default="Известия вузов. Геодезия и аэрофотосъемка", verbose_name="Название")
    issn_print = models.CharField(max_length=20, verbose_name="ISSN (Print)", blank=True)
    issn_online = models.CharField(max_length=20, verbose_name="ISSN (Online)", blank=True)
    publisher = models.CharField(max_length=200, verbose_name="Издатель", default="МИИГАиК")
    description = models.TextField(verbose_name="Описание журнала", blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Информация о журнале"
        verbose_name_plural = "Информация о журнале"


class ArchiveYear(models.Model):
    """Модель для управления диапазонами архива (например, 2020-2025)"""
    start_year = models.IntegerField(verbose_name="Год начала")
    end_year = models.IntegerField(verbose_name="Год конца")
    slug = models.SlugField(unique=True, verbose_name="URL slug (например, 2020-2025)")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    def __str__(self):
        return f"{self.start_year}-{self.end_year}"

    class Meta:
        verbose_name = "Архивный период"
        verbose_name_plural = "Архивные периоды"
