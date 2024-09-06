from django.contrib import admin

from .models import Category, Location, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'is_published',
        'created_at'
    )

    list_editable = (
        'is_published',
    )

    list_filter = (
        'is_published',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
        'created_at',
    )

    list_editable = (
        'is_published',
    )

    list_filter = (
        'is_published',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',
        'created_at'
    )

    list_editable = (
        'author',
        'is_published',
        'location',
        'category'
    )

    search_fields = ('title',
                     'author__username',
                     'location__name',
                     'category__title')

    list_filter = ('author',
                   'location',
                   'category',
                   'is_published')

    list_display_links = ('title', )


admin.site.empty_value_display = 'Не задано'
