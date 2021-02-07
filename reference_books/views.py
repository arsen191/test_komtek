from django.db.models import Q
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import ReferenceBook, Article
from .serializers import ReferenceBookSerializer, ArticleSerializer


class ReferenceBookListView(ReadOnlyModelViewSet):
    """получение списка справочников"""
    serializer_class = ReferenceBookSerializer

    def get_queryset(self):
        queryset = ReferenceBook.objects.all()
        return queryset


class ReferenceBookByDateListView(ReadOnlyModelViewSet):
    """получение списка справочников, актуальных на указанную дату"""
    serializer_class = ReferenceBookSerializer

    def get_queryset(self):
        queryset = ReferenceBook.objects.filter(Q(begin_at__lte=self.kwargs['data']))
        return queryset


class ArticlesByReferenceBookListView(ReadOnlyModelViewSet):
    """получение элементов заданного справочника текущей версии"""
    serializer_class = ArticleSerializer

    def get_queryset(self):
        last_version_of_book = ReferenceBook.objects.filter(name=self.kwargs['name']).order_by('version').last()
        queryset = Article.objects.filter(reference_book=last_version_of_book.pk)
        return queryset


class ArticlesByVersionOfReferenceBookListView(ReadOnlyModelViewSet):
    """получение элементов заданного справочника указанной версии"""
    serializer_class = ArticleSerializer

    def get_queryset(self):
        books_filtered = ReferenceBook.objects.filter(name=self.kwargs['name'],
                                                      version=self.kwargs['version']).first()
        queryset = Article.objects.filter(reference_book=books_filtered.pk)
        return queryset
