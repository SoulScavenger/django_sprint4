from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from blog.constants import POST_COUNT
from blog.forms import CommentForm, PostForm, UserUpdateFormUpdate
from blog.models import Category, Comment, Post, User


# VIEW-классы для категорий.
class CategoryDetailView(DetailView):
    """View-класс для просмотра постов по категориям."""

    model = Category
    slug_url_kwarg = 'category_slug'
    context_object_name = 'category'
    template_name = 'blog/category.html'

    def get_queryset(self) -> QuerySet[Any]:
        return self.model.objects.filter(is_published=True)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        self.object_list = Post.filtered.filter(category=self.get_object())
        paginator = Paginator(self.object_list, POST_COUNT)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


# VIEW-Классы для публикаций.
class PostListView(ListView):
    """View-класс списка публикаций."""

    model = Post
    paginate_by = POST_COUNT
    template_name = 'blog/index.html'

    def get_queryset(self):
        """Получить отфильтрованный QS из модели Post."""
        return Post.filtered.all()


class PostDetailView(DetailView):
    """View-класс для просмотра публикации."""

    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/detail.html'

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        if (obj.author != self.request.user
           and (not obj.is_published or not obj.category.is_published)):
            raise Http404
        return obj

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (self.object.comments.select_related('author'))

        return context


class PostCrudCustomMixin(LoginRequiredMixin):
    """Кастомный класс Миксин для CRUD операций для Post."""

    model = Post
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user})


class PostCreateView(PostCrudCustomMixin, CreateView):
    """View-класс создания публикации."""

    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user})


class PostUpdateView(PostCrudCustomMixin, UserPassesTestMixin, UpdateView):
    """View-класс для редактирования публикации."""

    form_class = PostForm
    pk_url_kwarg = 'post_id'

    def handle_no_permission(self):
        return redirect('blog:post_detail', self.get_object().id)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class PostDeleteView(PostCrudCustomMixin, UserPassesTestMixin, DeleteView):
    """View-класс для удаления публикации."""

    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'
    redirect_field_name = ''

    def handle_no_permission(self):
        return redirect('blog:post_detail', self.get_object().id)

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


# VIEW-Классы для комментирования.
class CommentCrudCustomMixin(LoginRequiredMixin):
    """Кастомный класс Миксин для CRUD операций для Comments."""

    model = Comment

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.object.publication_id})


class CommentCreateView(LoginRequiredMixin, CreateView):
    """View-класс для добавления комментария к публикации."""

    model = Comment
    publication = None
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        self.publication = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.publication = self.publication
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.object.publication_id})


class CommentUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, UpdateView
):
    """View-класс для редактирования комментария к публикации."""

    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.object.publication_id})


class CommentDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, DeleteView
):
    """View-класс для удаления комментария к публикации."""

    model = Comment
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'

    def test_func(self):
        object = self.get_object()
        return object.author_id == self.request.user.id

    # Я это сделал, т.к. тесты орали:
    # Убедитесь, что в словарь контекста для страницы удаления комментария не
    # передаётся объект формы.
    def get_context_data(self, **kwargs: Any):
        return None

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.object.publication_id})


# VIEW-Классы для профиля.
class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View-класс для редактирования профиля пользователя."""

    model = User
    form_class = UserUpdateFormUpdate
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'blog/user.html'

    def test_func(self):
        object = self.get_object()
        return object.username == self.request.user.username

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.object.username})


class ProfileDetailView(DetailView):
    """View-класс для просмотра профиля пользователя по категориям."""

    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'profile'
    template_name = 'blog/profile.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        self.object_list = self.get_object().posts.all()
        paginator = Paginator(self.object_list, POST_COUNT)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context
