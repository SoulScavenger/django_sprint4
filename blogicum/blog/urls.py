from django.urls import include, path

from blog import views

app_name = 'blog'

posts_urls = [
    path('<int:post_id>/',
         views.PostDetailView.as_view(),
         name='post_detail'),

    path('create/',
         views.PostCreateView.as_view(),
         name='create_post'),

    path('<int:post_id>/edit/',
         views.PostUpdateView.as_view(),
         name='edit_post'),

    path('<int:post_id>/delete/',
         views.PostDeleteView.as_view(),
         name='delete_post'),

    path('<int:post_id>/comments/',
         views.CommentCreateView.as_view(),
         name='add_comment'),

    path('<int:post_id>/comments/<int:comment_id>/edit_comment/',
         views.CommentUpdateView.as_view(),
         name='edit_comment'),

    path('<int:post_id>/comment/<int:comment_id>/delete_comment/',
         views.CommentDeleteView.as_view(),
         name='delete_comment'),
]


profiles_urls = [
    path('edit_profile/',
         views.ProfileUpdateView.as_view(),
         name='edit_profile'),

    path('<str:username>/',
         views.ProfileDetailView.as_view(), name='profile'),
]

urlpatterns = [
    path('', views.PostListView.as_view(),
         name='index'),
    path('posts/', include(posts_urls)),
    path('profile/', include(profiles_urls)),
    path('category/<slug:category_slug>/',
         views.CategoryDetailView.as_view(),
         name='category_posts'),
]
