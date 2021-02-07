from django.urls import path, include
from . import views

urlpatterns = [
    path("reference_books/", views.ReferenceBookListView.as_view()),
    path('reference_books_by_data/', views.ReferenceBookByDateListView.as_view()),
    path('articles_by_reference_book/', views.ArticlesByReferenceBookListView.as_view()),
    path('articles_by_version_reference_book/', views.ArticlesByVersionOfReferenceBookListView.as_view()),
]
