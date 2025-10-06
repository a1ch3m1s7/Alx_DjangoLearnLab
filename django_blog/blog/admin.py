from django.contrib import admin
from .models import Post, Profile, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    search_fields = ('title', 'content')
    list_filter = ('published_date', 'author')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username', 'user__email', 'bio')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('short_content', 'author', 'post', 'created_at')
    search_fields = ('content', 'author__username', 'post__title')
    list_filter = ('created_at', 'author')

    def short_content(self, obj):
        return obj.content[:50]
    short_content.short_description = 'Content'