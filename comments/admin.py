from django.contrib import admin
from .models import Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "blog",
        "comment_author",
        "short_comment_body",
        "comment_parent",
        "comment_created",
    ]

    def short_comment_body(self, obj):
        return (
            obj.comment_body[:75] + "..."
            if len(obj.comment_body) > 75
            else obj.comment_body
        )

    short_comment_body.short_description = "Comment Body"


admin.site.register(Comment, CommentAdmin)
