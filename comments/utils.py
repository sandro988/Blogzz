from django.urls import reverse_lazy, resolve
from .models import Comment


def redirect_to_continue_thread_page(next_url: str, comment_to_delete: Comment):
    """
    Redirects to continue_thread page if there are more than one comments on the page, if there is only one comment with or without
    replies than we return None, this ensures that if user deletes the last comment on continue_thread page they get redirected to
    blog_detail page, but if there is more than one comment with or without replies and user deletes one of them, they will be redirected
    back to the continue_thread page.

    Parameters:
        next_url (str): A URL containing the 'blog_pk' and 'comment_pk' parameters for the comment to redirect to.
        comment_to_delete (Comment): The comment object that the user intends to delete.

    Returns:
        None if there is only comment on continue_thread page with or without replies.
        Redirect to the continue_thread page if there is more than one 1 comment with or without replies on page.
    """

    if next_url:
        next_url_info = resolve(next_url)
        blog_pk = next_url_info.kwargs.get("blog_pk")
        comment_pk = next_url_info.kwargs.get("comment_pk")
        comment = Comment.objects.get(id=comment_pk)
        # Number of replies on 'continue_thread' page.
        number_of_replies = comment.count_comments_and_replies()

        # If the user goes to continue_thread page and there is only one comment with replies and the user tries to
        # delete that comment, user should be redirected to blog_detail page, because after deleting that comment
        # all of its replies will also be deleted.
        if comment_to_delete.get_reply_count() >= 1 and comment.get_reply_count() == 1:
            return None
        elif number_of_replies > 1:
            return reverse_lazy(
                "continue_thread",
                kwargs={"blog_pk": blog_pk, "comment_pk": comment_pk},
            )

    return None


def get_comment_from_next_url(url: str):
    if url is None:
        return None
    next_url_info = resolve(url)
    comment_pk = next_url_info.kwargs.get("comment_pk")
    comment = Comment.objects.get(id=comment_pk)

    return comment
