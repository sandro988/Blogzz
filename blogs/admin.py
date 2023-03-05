from django.contrib import admin
from .models import Blog, Category
from comments.admin import CommentInline


class BlogAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]


admin.site.register(Blog, BlogAdmin)
admin.site.register(Category)
