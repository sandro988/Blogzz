from django.urls import resolve
from .models import Comment


def get_comment_from_next_url(url: str):
    if url is None:
        return None
    next_url_info = resolve(url)
    comment_pk = next_url_info.kwargs.get("pk")
    comment = Comment.objects.get(id=comment_pk)

    return comment
