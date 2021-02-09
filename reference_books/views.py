from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import ReferenceBook, Article
from .serializers import ReferenceBookSerializer, ArticleSerializer


class ReferenceBookListView(ReadOnlyModelViewSet):
    """получение списка справочников"""
    serializer_class = ReferenceBookSerializer

    def get_queryset(self):
        queryset = ReferenceBook.objects.all().order_by('name')
        return queryset


class ReferenceBookByDateListView(ReadOnlyModelViewSet):
    """получение списка справочников, актуальных на указанную дату"""
    serializer_class = ReferenceBookSerializer

    def get_queryset(self):
        # предполагаем, что актуальными являются справочники, выпущенные до указанной даты
        queryset = ReferenceBook.objects.filter(Q(begin_at__lte=self.kwargs['date']))
        return queryset


class ArticlesByReferenceBookListView(ReadOnlyModelViewSet):
    """получение элементов заданного справочника текущей версии"""
    serializer_class = ArticleSerializer

    def get_queryset(self):
        # предполагаем, что последняя версия является текущей
        last_version_of_book = ReferenceBook.objects.filter(name=self.kwargs['name']).order_by('version').last()
        queryset = Article.objects.filter(reference_book=last_version_of_book.pk)
        return queryset


class ValidArticleOfReferenceBook(APIView):
    """валидация элементов заданного справочника текущей версии"""
    def post(self, request):
        # предполагаем, что последняя версия является текущей
        try:
            last_version_of_book = ReferenceBook.objects.filter(name=self.request.data['name']).order_by('version').last()
            if Article.objects.filter(reference_book=last_version_of_book.pk,
                                      code__exact=self.request.data['code']).exists():
                return Response(f'этот элемент является элементом справочника {self.request.data["name"]} '
                                f'текущей версии', status=status.HTTP_200_OK)
            else:
                return Response(f'этот элемент не является элементом справочника {self.request.data["name"]} '
                                f'текущей версии', status=status.HTTP_204_NO_CONTENT)
        except KeyError:
            return Response('введите справочник и код элемента в формате {"name": наименование_справочника, '
                            '"code": код_элемента}')
        except AttributeError:
            return Response("введите корректные данные!")


class ArticlesByVersionOfReferenceBookListView(ReadOnlyModelViewSet):
    """получение элементов заданного справочника указанной версии"""
    serializer_class = ArticleSerializer

    def get_queryset(self):
        queryset = Article.objects.filter(reference_book__name=self.kwargs['name'],
                                          reference_book__version=self.kwargs['version'])
        return queryset


class ValidArticleByVersionOfReferenceBook(APIView):
    """валидация элемента заданного справочника по указанной версии"""
    def post(self, request):
        try:
            if Article.objects.filter(reference_book__name=self.request.data['name'],
                                      reference_book__version=self.request.data['version'],
                                      code__exact=self.request.data['code']).exists():
                return Response(
                    f'этот элемент является элементом справочника {self.request.data["name"]} '
                    f'версии {self.request.data["version"]}', status=status.HTTP_200_OK)
            else:
                return Response(
                    f'этот элемент не является элементом справочника {self.request.data["name"]} '
                    f'версии {self.request.data["version"]}', status=status.HTTP_204_NO_CONTENT)
        except KeyError:
            return Response('введите справочник, версию и код элемента в формате {"name": наименование_справочника, '
                            '"version": версия_справочника, "code": код_элемента}')
        except AttributeError:
            return Response("введите корректные данные!")
