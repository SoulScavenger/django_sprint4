from django.db import models


class PublishedModel(models.Model):
    """Абстрактная модель."""

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
        help_text='Дата добавления.'
    )

    class Meta:
        abstract = True
