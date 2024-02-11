from django.contrib import admin
from django.utils.html import mark_safe
from blogapp.models import Post, User, Comments


# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'images')
    list_filter = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'images')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'images')
    ordering = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'images')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status', 'display_image')
    list_filter = ('status', 'created_at', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

    def display_image(self, obj):
        # Здесь вы можете создать HTML-код для отображения изображения
        if obj.images:
            return mark_safe(f'<img src="{obj.images.url}" width="50" height="50" />')
        else:
            return 'Нет изображения'

    display_image.short_description = 'Изображение'


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('username', 'post', 'email', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('username', 'body', 'email')