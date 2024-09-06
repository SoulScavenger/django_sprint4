from django.db import models
from django.utils import timezone


class FilteredPosts(models.Manager):
    """Кастомный менеджер для модели Post."""

    def get_queryset(self) -> models.QuerySet:
        """Получить отфильтрованный QuerySet."""
        return super().get_queryset().select_related(
            'author', 'location', 'category'
        ).filter(is_published=True,
                 pub_date__lte=timezone.now(),
                 category__is_published=True
                 )
