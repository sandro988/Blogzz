from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = [
            "blog",
            "comment_author",
            "comment_parent",
        ]
