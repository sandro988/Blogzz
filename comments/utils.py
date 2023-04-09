from django.urls import resolve
from .models import Comment
from typing import List


def get_comment_from_next_url(url: str):
    if url is None:
        return None
    next_url_info = resolve(url)
    comment_pk = next_url_info.kwargs.get("pk")
    comment = Comment.objects.get(id=comment_pk)

    return comment


def get_sorted_comments(comments: List[Comment], sort_param: str) -> List[Comment]:
    """
    Function used for sorting comments, this function will be used in blog_detail and continue_thread views.
    """

    if sort_param == "oldest":
        comments = comments.order_by("comment_created")
    elif sort_param == "newest":
        comments = comments.order_by("-comment_created")
    elif sort_param == "popular":
        comments = comments.order_by("-comment_upvotes_count")

    return comments


def get_sorted_replies(comment: Comment, sort_param: str) -> List[Comment]:
    """
    Function used for sorting the replies of a comment, this function will be used in comment_detail view
    where we have only one comment with its nested replies.
    """

    replies = comment.get_replies()
    if sort_param == "oldest":
        replies = comment.replies.order_by("comment_created")
    elif sort_param == "newest":
        replies = comment.replies.order_by("-comment_created")
    elif sort_param == "popular":
        replies = comment.replies.order_by("-comment_upvotes_count")

    return replies
