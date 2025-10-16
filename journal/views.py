from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.generic import ListView, DetailView
from .models import JournalIssue, Article, EditorialBoard, JournalInfo, ArchiveYear
from .forms import ContactForm

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


ARCHIVE_RANGES = {
    "1957-1959": {
        1959: ["Том 1", "Том 2", "Том 3", "Том 4", "Том 5", "Том 6"],
        1958: ["Том 1", "Том 2", "Том 3", "Том 4", "Том 5", "Том 6"],
        1957: ["Том 1", "Том 2", "Том 3", "Том 4", "Том 5", "Том 6"],
    },
    "1960-1969": {
        1969: ["Том 1", "Том 2"],
        1968: ["Том 1"],
        # и так далее
    },
    "2020-2025": {
        2025: ["Том 1"],
        2024: ["Том 1", "Том 2", "Том 3", "Том 4", "Том 5", "Том 6"],
        2023: ["Том 1", "Том 2", "Том 3", "Том 4", "Том 5", "Том 6"],
        # и так далее
    },
}

def archive_range_view(request, year_range):
    """
    Отображает архив для заданного промежутка лет (например, '1957-1959').
    """
    # Получаем данные для промежутка
    range_data = ARCHIVE_RANGES.get(year_range)

    if not range_data:
        # Если промежуток не найден, можно вернуть 404 или редирект
        from django.shortcuts import render
        from django.http import Http404
        raise Http404("Промежуток лет не найден в архиве.")

    # Сортируем годы по убыванию (новые первыми)
    sorted_years = sorted(range_data.keys(), reverse=True)

    context = {
        'year_range': year_range,
        'range_data': range_data,
        'sorted_years': sorted_years,
    }

    return render(request, 'journal/archive_range.html', context)

def sections(request):
    """Рубрики и периодичность"""
    return render(request, 'journal/sections.html')

def editorial_staff(request):
    """Редакционная коллегия"""
    return render(request, 'journal/editorial_staff.html')

def editorial_board(request):
    """Редакционная коллегия"""
    return render(request, 'journal/editorial_board.html')