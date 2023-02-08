from django import forms
from .models import Blog


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
