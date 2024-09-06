from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    # Отображение всех публикаций.
    path('', views.PostListView.as_view(),
         name='index'),

    # Детальный просмотр публикации.
    path('posts/<int:post_id>/',
         views.PostDetailView.as_view(),
         name='post_detail'),

    # Создание публикации.
    path('posts/create/',
         views.PostCreateView.as_view(),
         name='create_post'),

    # Редактирование публикации.
    path('posts/<int:post_id>/edit/',
         views.PostUpdateView.as_view(),
         name='edit_post'),

    # Удаление публикации.
    path('posts/<int:post_id>/delete/',
         views.PostDeleteView.as_view(),
         name='delete_post'),

    # Добавление комментариев.
    path('posts/<int:post_id>/comments/',
         views.CommentCreateView.as_view(),
         name='add_comment'),
    # Редактирование комментария.
    path('posts/<int:post_id>/comments/<int:comment_id>/edit_comment/',
         views.CommentUpdateView.as_view(),
         name='edit_comment'),
    # Удаление комментария.
    path('posts/<int:post_id>/comment/<int:comment_id>/delete_comment/',
         views.CommentDeleteView.as_view(),
         name='delete_comment'),

    # Просмотр постов по публикации.
    path('category/<slug:category_slug>/',
         views.CategoryDetailView.as_view(),
         name='category_posts'),
    #  Просмотр профиля.
    path('profile/<str:username>/',
         views.ProfileDetailView.as_view(), name='profile'),

    # Редактирование профиля.
    path('profile/<str:username>/edit_profile/',
         views.ProfileUpdateView.as_view(),
         name='edit_profile')
]
