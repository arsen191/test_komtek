from datetime import date

from django.db import models
from django.db.models import UniqueConstraint


class ReferenceBook(models.Model):
    """Справочник"""
    name = models.CharField(max_length=128, verbose_name="наименование")
    short_name = models.CharField(max_length=50, blank=True, verbose_name="короткое наименование")
    description = models.TextField(blank=True, verbose_name="описание")
    version = models.CharField(max_length=15, verbose_name="Версия справочника")
    begin_at = models.DateField(default=date.today(), verbose_name="Дата начала действия справочника этой версии")

    def __str__(self):
        return f'{self.name} ver.{self.version}'

    class Meta:
        verbose_name = "Справочник"
        verbose_name_plural = "Справочники"
        constraints = [
            UniqueConstraint(fields=['name', 'version'], name='unique_version_of_book')
        ]


class Article(models.Model):
    """Элемент справочника"""
    reference_book = models.ForeignKey(ReferenceBook, on_delete=models.CASCADE, verbose_name="справочник")
    code = models.CharField(max_length=30, verbose_name="код элемента")
    value = models.CharField(max_length=255, verbose_name="значение элемента")

    def __str__(self):
        return f'{self.reference_book.name} - {self.code}'

    class Meta:
        verbose_name = "Элемент справочника"
        verbose_name_plural = "Элементы справочника"
