from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, FileResponse, Http404 
from django.contrib import messages
from django.views.generic import ListView, DetailView
from .models import JournalIssue, Article, JournalInfo, ArchiveYear
from .forms import ContactForm
from itertools import groupby


def home_view(request):
    return render(request, 'journal/index.html')

def home(request):
    """Главная страница"""
    journal_info = JournalInfo.objects.first()
    current_issue = JournalIssue.objects.filter(is_current=True).first()
    recent_articles = Article.objects.filter(is_published=True)[:5]
    
    context = {
        'journal_info': journal_info,
        'current_issue': current_issue,
        'recent_articles': recent_articles,
    }
    return render(request, 'journal/home.html', context)


def contact(request):
    """Страница контактов и форма обратной связи"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваше сообщение успешно отправлено!')
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ContactForm()
    
    return render(request, 'journal/contact.html', {'form': form})


class IssueListView(ListView):
    """Список выпусков журнала"""
    model = JournalIssue
    template_name = 'journal/issues.html'
    context_object_name = 'issues'
    paginate_by = 10


class IssueDetailView(DetailView):
    """Детальная страница выпуска"""
    model = JournalIssue
    template_name = 'journal/issue_detail.html'
    context_object_name = 'issue'


class ArticleListView(ListView):
    """Список статей"""
    model = Article
    template_name = 'journal/articles.html'
    context_object_name = 'articles'
    paginate_by = 10
    
    def get_queryset(self):
        return Article.objects.filter(is_published=True)


class ArticleDetailView(DetailView):
    """Детальная страница статьи"""
    model = Article
    template_name = 'journal/article_detail.html'
    context_object_name = 'article'


def download_article_pdf(request, article_id):
    """Скачиваем пдф файла статьи (как вложение)"""
    article = get_object_or_404(Article, pk=article_id)

    # поле в модели article называется pdf_file если оно называется иначе изменить!

    if not article.pdf_file:
        raise Http404("Файл PDF для этой статьи отсутствует.")

    try:
        file_handle = article.pdf_file.open('rb')
        response = FileResponse(file_handle, as_attachment=True)
        # формируем имя файла для пользователя (безопасное)
        filename = f"Article_{article_id}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    except FileNotFoundError:
        raise Http404("Файл не найден на сервере.")


def read_article_pdf(request, article_id):
    """Просмотр PDF файла статьи в браузере (inline)"""
    article = get_object_or_404(Article, pk=article_id)
    
    if not article.pdf_file:
        raise Http404("PDF файл для этой статьи отсутствует.")
        
    try:
        file_handle = article.pdf_file.open('rb')
        # as_attachment=False открывает файл во вкладке браузера
        return FileResponse(file_handle, as_attachment=False)
    except FileNotFoundError:
        raise Http404("Файл не найден на сервере.")


def editorial_board(request):
    """Редакционная коллегия"""
    board_members = EditorialBoard.objects.all()
    return render(request, 'journal/editorial_board.html', {'board_members': board_members})


def archive(request):
    """Архив журнала"""
    archive_years = ArchiveYear.objects.filter(is_active=True)
    return render(request, 'journal/archive.html', {'archive_years': archive_years})

def history(request):
    """История журнала"""
    return render(request, 'journal/history.html')

def journal_info(request):
    """Информация о журнале"""
    journal_info = JournalInfo.objects.first()
    return render(request, 'journal/journal_info.html', {'journal_info': journal_info})


def focus_and_scope(request):
    """Цели и задачи журнала"""
    return render(request, 'journal/focus_and_scope.html')


def peer_reviewing(request):
    """Рецензирование"""
    return render(request, 'journal/peer_reviewing.html')


def ethics(request):
    """Публикационная этика"""
    return render(request, 'journal/ethics.html')


def copyright(request):
    """Авторское право"""
    return render(request, 'journal/copyright.html')


def conflict_of_interests(request):
    """Конфликт интересов"""
    return render(request, 'journal/conflict_of_interests.html')


def open_access(request):
    """Открытый доступ"""
    return render(request, 'journal/open_access.html')


def privacy_policy(request):
    """Политика конфиденциальности"""
    return render(request, 'journal/privacy_policy.html')


def fees(request):
    """Плата за публикацию"""
    return render(request, 'journal/fees.html')


def guidelines(request):
    """Руководство для авторов"""
    return render(request, 'journal/guidelines.html')


def text_design(request):
    """Оформление статьи"""
    return render(request, 'journal/text_design.html')


def references(request):
    """Библиография"""
    return render(request, 'journal/references.html')


def archive_range_view(request, year_range):
    """
    Отображает страницу архива для диапазона (например, '2020-2025').
    """
    try:
        # Разбиваем строку "2020-2025" на начало и конец
        start_year, end_year = map(int, year_range.split('-'))
    except ValueError:
        raise Http404("Некорректный формат диапазона лет")

    # 1. Достаем выпуски из БД, попадающие в этот диапазон
    # order_by('-year') важен для группировки
    issues = JournalIssue.objects.filter(
        year__gte=start_year, 
        year__lte=end_year
    ).order_by('-year', '-number')

    # 2. Группируем выпуски по годам для удобного вывода в шаблоне
    # structure: [(2025, [issue1, issue2]), (2024, [issue3...])]
    issues_by_year = []
    for year, group in groupby(issues, key=lambda x: x.year):
        issues_by_year.append((year, list(group)))
    
    # 3. Генерируем список лет для кнопок (от конца к началу)
    years_list = list(range(end_year, start_year - 1, -1))

    context = {
        'year_range': year_range,
        'issues_by_year': issues_by_year, # Данные для сетки
        'years_list': years_list,          # Данные для кнопок
    }

    return render(request, 'journal/archive_range.html', context)

def sections(request):
    """Рубрики и периодичность"""
    return render(request, 'journal/sections.html')

def editorial_staff(request):
    """Редакционная коллегия"""
    return render(request, 'journal/editorial_staff.html')
