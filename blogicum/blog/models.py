from django.contrib.auth import get_user_model
from django.db import models

from blog.constants import TITLE_SLICE
from blog.managers import FilteredPosts
from core.models import PublishedModel

User = get_user_model()


class Category(PublishedModel):
    """Модель Тематической категории."""

    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок',
        help_text='Название категории, не более 256 символов.'
    )

    description = models.TextField(
        verbose_name='Описание',
        help_text='Описание категории.'
    )

    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; разрешены символы латиницы'
                   ', цифры, дефис и подчёркивание.')
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        """Именует объекты значением из поля title."""
        return self.title[:TITLE_SLICE]


class Location(PublishedModel):
    """Модель Географической метки."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название места',
        help_text='Название локации, не более 256 символов.'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        """Именует объекты значением из поля title."""
        return self.name[:TITLE_SLICE]


class Post(PublishedModel):
    """Модель Публикации."""

    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок',
        help_text='Уникальное название публикации, не более 256 символов.'
    )

    text = models.TextField(
        verbose_name='Текст',
        help_text='Текст публикации.'
    )

    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=('Если установить дату и время в будущем — можно делать '
                   'отложенные публикации.')
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        help_text='Выберете автора публикации.',
    )

    location = models.ForeignKey(
        Location,
        blank=True,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Местоположение',
        help_text='Выберете местоположение публикации.'
    )

    objects = models.Manager()
    filtered = FilteredPosts()

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        help_text='Выберете категорию публикации.'
    )

    image = models.ImageField(
        blank=True, verbose_name='Изображение', upload_to='posts_images'
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        default_related_name = 'posts'
        ordering = ('-pub_date', )

    def __str__(self):
        """Именует объекты значением из поля title."""
        return self.title[:TITLE_SLICE]

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog:post_detail', kwargs={'post_id': self.pk})


class Comment(models.Model):
    """Класс модели для Комментариев."""

    text = models.TextField(verbose_name='Текст комментария')
    publication = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Публикация'
    )
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата публикации')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор')

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at',)
        default_related_name = 'comments'

    def __str__(self):
        """Именует объекты значением из поля title."""
        return self.text[:TITLE_SLICE]
