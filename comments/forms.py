from django import forms
from .models import Comment


class CommentCreationForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = [
            "blog",
            "comment_author",
            "comment_parent",
            "comment_upvotes",
            "comment_upvotes_count",
        ]


class CommentUpdateForm(CommentCreationForm):
    class Meta:
        model = Comment
        exclude = [
            "blog",
            "comment_author",
            "comment_parent",
            "comment_upvotes",
            "comment_upvotes_count",
        ]
