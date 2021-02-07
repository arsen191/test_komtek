from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ReferenceBook, Article
from .serializers import ReferenceBookSerializer, ArticleSerializer


class ReferenceBookListView(APIView):
    """получение списка справочников"""
    def get(self, request):
        serializer = ReferenceBookSerializer(ReferenceBook.objects.all(), many=True)
        return Response(serializer.data)


class ReferenceBookByDateListView(APIView):
    """получение списка справочников, актуальных на указанную дату"""
    def get(self, request):
        serializer = ReferenceBookSerializer(ReferenceBook.objects.filter(Q(begin_at__lte=self.request.data['data'])),
                                             many=True)
        return Response(serializer.data)


class ArticlesByReferenceBookListView(APIView):
    """получение элементов заданного справочника текущей версии"""
    def get(self, request):
        last_version_of_book = ReferenceBook.objects.filter(name=self.request.data['name']).order_by('version').last()
        queryset = Article.objects.filter(reference_book=last_version_of_book.pk)
        serializer = ArticleSerializer(queryset, many=True)
        return Response(serializer.data)


class ArticlesByVersionOfReferenceBookListView(APIView):
    """получение элементов заданного справочника указанной версии"""
    def get(self, request):
        books_filtered = ReferenceBook.objects.filter(name=self.request.data['name'],
                                                      version=self.request.data['version']).first()
        queryset = Article.objects.filter(reference_book=books_filtered.pk)
        serializer = ArticleSerializer(queryset, many=True)
        return Response(serializer.data)
