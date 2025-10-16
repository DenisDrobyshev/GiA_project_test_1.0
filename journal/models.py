# models.py

from django.db import models
from django.utils import timezone
from django.urls import reverse


class ArchiveYear(models.Model):
    """Модель для архивных промежутков лет (например, 1957-1959)"""
    start_year = models.IntegerField(verbose_name="Год начала")
    end_year = models.IntegerField(verbose_name="Год окончания")
    slug = models.SlugField(unique=True, verbose_name="Slug (например, 1957-1959)")
    description = models.TextField(verbose_name="Описание", blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Архивный промежуток лет"
        verbose_name_plural = "Архивные промежутки лет"
        ordering = ['-end_year']

    def __str__(self):
        return f"{self.start_year} - {self.end_year}"

    def get_absolute_url(self):
        return reverse('archive_range', kwargs={'slug': self.slug})


class JournalIssue(models.Model):
    """Модель выпуска журнала"""
    year = models.IntegerField(verbose_name="Год")
    number = models.IntegerField(verbose_name="Номер")
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", blank=True)
    cover_image = models.ImageField(upload_to='covers/', verbose_name="Обложка", blank=True)
    is_current = models.BooleanField(default=False, verbose_name="Текущий выпуск")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # --- Связь с ArchiveYear ---
    archive_year = models.ForeignKey(
        ArchiveYear,
        on_delete=models.SET_NULL, # Или CASCADE
        related_name='issues', # Уникальное имя для обратной связи
        null=True, blank=True,
        verbose_name="Архивный промежуток"
    )
    # --- Конец связи ---

    class Meta:
        verbose_name = "Выпуск журнала"
        verbose_name_plural = "Выпуски журнала"
        ordering = ['-year', '-number']

    def __str__(self):
        return f"Выпуск {self.number}, {self.year}"


class Article(models.Model):
    """Модель статьи"""
    title = models.CharField(max_length=500, verbose_name="Название")
    abstract = models.TextField(verbose_name="Аннотация")
    authors = models.TextField(verbose_name="Авторы")
    keywords = models.TextField(verbose_name="Ключевые слова", blank=True)
    doi = models.CharField(max_length=100, verbose_name="DOI", blank=True)
    pdf_file = models.FileField(upload_to='articles/', verbose_name="PDF файл", blank=True)
    # --- Связь с JournalIssue ---
    issue = models.ForeignKey(JournalIssue, on_delete=models.CASCADE, related_name='articles', verbose_name="Выпуск")
    # --- Конец связи ---
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Убрана прямая связь с ArchiveYear (если она была)

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# --- Остальные модели без изменений ---
class EditorialBoard(models.Model):
    name = models.CharField(max_length=200, verbose_name="Имя")
    position = models.CharField(max_length=200, verbose_name="Должность")
    institution = models.CharField(max_length=300, verbose_name="Учреждение", blank=True)
    bio = models.TextField(verbose_name="Биография", blank=True)
    photo = models.ImageField(upload_to='editorial_board/', verbose_name="Фото", blank=True)
    order = models.IntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Член редакционной коллегии"
        verbose_name_plural = "Редакционная коллегия"
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} - {self.position}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False, verbose_name="Обработано")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ['-created_at']

    def __str__(self):
        return f"Сообщение от {self.name}"


class JournalInfo(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название журнала")
    description = models.TextField(verbose_name="Описание")
    issn_print = models.CharField(max_length=20, verbose_name="ISSN (печатная версия)")
    issn_online = models.CharField(max_length=20, verbose_name="ISSN (онлайн версия)")
    publisher = models.CharField(max_length=200, verbose_name="Издатель")
    logo = models.ImageField(upload_to='journal/', verbose_name="Логотип", blank=True)
    main_image = models.ImageField(upload_to='journal/', verbose_name="Главное изображение", blank=True)

    class Meta:
        verbose_name = "Информация о журнале"
        verbose_name_plural = "Информация о журнале"

    def __str__(self):
        return self.title