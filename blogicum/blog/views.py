from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from blog.forms import CommentForm, PostForm, UserUpdateForm
from blog.mixins import (CommentCrudMixin, PostAccessEditMixin, PostCrudMixin,
                         PostViewMixin)
from blog.models import Category, Post, User


class CategoryDetailView(PostViewMixin):
    """View-класс для просмотра постов по категориям."""

    template_name = 'blog/category.html'
    category = None

    def set_category(self):
        self.category = get_object_or_404(Category,
                                          slug=self.kwargs['category_slug'],
                                          is_published=True)

    def get_queryset(self):
        self.set_category()
        qs = Post.filtered.filter(category=self.category)
        return self.get_comment_count(qs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class PostListView(PostViewMixin):
    """View-класс списка публикаций."""

    template_name = 'blog/index.html'

    def get_queryset(self):
        """Получить отфильтрованный QS из модели Post."""
        qs = Post.filtered.all()
        return self.get_comment_count(qs)


class PostDetailView(DetailView):
    """View-класс для просмотра публикации."""

    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/detail.html'

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        if obj.author != self.request.user:
            obj = get_object_or_404(Post.filtered.all(),
                                    id=self.kwargs['post_id']
                                    )
        return obj

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (self.object.comments.select_related('author'))

        return context


class PostCreateView(PostCrudMixin, CreateView):
    """View-класс создания публикации."""

    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(PostCrudMixin, PostAccessEditMixin, UpdateView):
    """View-класс для редактирования публикации."""

    form_class = PostForm


class PostDeleteView(PostCrudMixin, PostAccessEditMixin, DeleteView):
    """View-класс для удаления публикации."""


class CommentCreateView(CommentCrudMixin, CreateView):
    """View-класс для добавления комментария к публикации."""

    publication = None
    form_class = CommentForm

    def form_valid(self, form):
        self.publication = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.author = self.request.user
        form.instance.publication = self.publication
        return super().form_valid(form)


class CommentUpdateView(
    CommentCrudMixin, UserPassesTestMixin, UpdateView
):
    """View-класс для редактирования комментария к публикации."""

    form_class = CommentForm
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class CommentDeleteView(
    CommentCrudMixin, UserPassesTestMixin, DeleteView
):
    """View-класс для удаления комментария к публикации."""

    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'

    def test_func(self):
        object = self.get_object()
        return object.author_id == self.request.user.id

    def get_context_data(self, **kwargs: Any):
        return None


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """View-класс для редактирования профиля пользователя."""

    model = User
    form_class = UserUpdateForm
    template_name = 'blog/user.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.object.username})


class ProfileDetailView(PostViewMixin):
    """View-класс для просмотра профиля пользователя по категориям."""

    template_name = 'blog/profile.html'

    def get_queryset(self):
        author = get_object_or_404(User, username=self.kwargs['username'])
        qs = Post.filtered.filter(author=author)
        if author.username == self.request.user.username:
            qs = Post.objects.select_related(
                'author', 'category', 'location'
            ).filter(author=author)

        return self.get_comment_count(qs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(User, username=self.kwargs['username'])
        context['profile'] = profile
        return context
