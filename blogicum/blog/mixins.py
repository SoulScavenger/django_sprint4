from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView

from blog.constants import POST_COUNT
from blog.models import Comment, Post


class PostViewMixin(ListView):
    model = Post
    paginate_by = POST_COUNT


class PostCrudMixin(LoginRequiredMixin):
    """Кастомный класс Миксин для CRUD операций для Post."""

    model = Post
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user})


class PostAccessEditMixin(UserPassesTestMixin):
    """Кастомный класс Миксин для проверки доступа к редактированию Post."""

    pk_url_kwarg = 'post_id'

    def handle_no_permission(self):
        return redirect('blog:post_detail', self.get_object().id)

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class CommentCrudMixin(LoginRequiredMixin):
    """Кастомный класс Миксин для CRUD операций для Comments."""

    model = Comment

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.object.publication_id})
