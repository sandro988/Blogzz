from django import forms
from .models import Blog
from django_editorjs_fields import EditorJsWidget


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        exclude = [
            "blog_status",
            "author",
            "blog_category_foreignkey",
            "blog_likes",
            "blog_likes_count",
        ]
        widgets = {
            "body_editorjs": EditorJsWidget(config={"minHeight": 100}),
            "body_editorjs_text": EditorJsWidget(
                plugins=["@editorjs/image", "@editorjs/header"]
            ),
        }
