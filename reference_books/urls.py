from django.urls import path, include
from . import views

urlpatterns = [
    path("reference_books/", views.ReferenceBookListView.as_view({'get': 'list'})),
    path('reference_books_by_date/<date>/', views.ReferenceBookByDateListView.as_view({'get': 'list'})),
    path('articles_by_reference_book/<name>/', views.ArticlesByReferenceBookListView.as_view({'get': 'list'})),
    path('articles_by_version_reference_book/<name>/<version>/',
         views.ArticlesByVersionOfReferenceBookListView.as_view({'get': 'list'})),
]
