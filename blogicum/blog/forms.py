from django import forms

from .models import Comment, Post, User


class PostForm(forms.ModelForm):
    """Класс-Форма для модели Post."""

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'})
        }


class UserUpdateFormUpdate(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class CommentForm(forms.ModelForm):
    """Класс-Форма для модели Comments."""

    class Meta:
        model = Comment
        fields = ('text',)
