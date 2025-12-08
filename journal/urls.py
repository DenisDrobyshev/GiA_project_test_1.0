from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('contact/', views.contact, name='contact'),

    path('issues/', views.IssueListView.as_view(), name='issues'),
    path('issues/<int:pk>/', views.IssueDetailView.as_view(), name='issue_detail'),

    path('articles/', views.ArticleListView.as_view(), name='articles'),
    path('articles/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),

    # Используем article_id, так как во views.py функции ожидают именно этот аргумент
    path('articles/<int:article_id>/download/', views.download_article_pdf, name='download_article_pdf'),
    path('articles/<int:article_id>/read/', views.read_article_pdf, name='read_article_pdf'),

    path('archive/', views.archive, name='archive'),
    # URL для конкретного промежутка лет, например: /archive/1957-1959/
    path('archive/<str:year_range>/', views.archive_range_view, name='archive_range'),

    # === Редакция ===
    path('editorial-board/', views.editorial_board, name='editorial_board'),
    path('editorial-staff/', views.editorial_staff, name='editorial_staff'),

    path('history/', views.history, name='history'),
    path('journal-info/', views.journal_info, name='journal_info'),
    path('sections/', views.sections, name='sections'),

    # === Политики и руководства ===
    path('focus-and-scope/', views.focus_and_scope, name='focus_and_scope'),
    path('peer-reviewing/', views.peer_reviewing, name='peer_reviewing'),
    path('ethics/', views.ethics, name='ethics'),
    path('copyright/', views.copyright, name='copyright'),
    path('conflict-of-interests/', views.conflict_of_interests, name='conflict_of_interests'),
    path('open-access/', views.open_access, name='open_access'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('fees/', views.fees, name='fees'),
    path('guidelines/', views.guidelines, name='guidelines'),
    path('text-design/', views.text_design, name='text_design'),
    path('references/', views.references, name='references'),
]

