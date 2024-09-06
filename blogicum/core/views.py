from django.contrib.auth.views import LoginView
from django.urls import reverse


class CustomLoginView(LoginView):
    """Кастомный LoginView"""

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user})
