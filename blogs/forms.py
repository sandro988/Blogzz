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
        widgets = {
            'blog_title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'blog_category': forms.TextInput(attrs={'placeholder': "Category"}),
            'blog_thumbnail': forms.FileInput()
        }
