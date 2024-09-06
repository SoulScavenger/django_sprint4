from django import forms

from blog.models import Comment, Post, User


class PostForm(forms.ModelForm):
    """Класс-Форма для модели Post."""

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateTimeInput(format=('%Y-%m-%d %H:%M'),
                                            attrs={'type': 'datetime-local'}),
            'text': forms.Textarea({'cols': '22', 'rows': '5'}),
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
        widgets = {
            'text': forms.Textarea({'cols': '22', 'rows': '5'}),
        }
