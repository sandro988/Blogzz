from django.urls import path
from .views import (
    CreateCommentView,
    CommentDetailView,
    UpdateCommentView,
    DeleteCommentView,
)

urlpatterns = [
    path(
        "comment/<uuid:pk>/",
        CommentDetailView.as_view(),
        name="comment_detail",
    ),
    path(
        "comment/create_comment/<uuid:pk>/",  # here pk is the primary key of a blog.
        CreateCommentView.as_view(),
        name="create_comment",
    ),
    path(
        "comment/update_comment/<uuid:blog_pk>/<uuid:comment_pk>/",
        UpdateCommentView.as_view(),
        name="update_comment",
    ),
    path(
        "comment/delete_comment/<uuid:blog_pk>/<uuid:comment_pk>/",
        DeleteCommentView.as_view(),
        name="delete_comment",
    ),
]
