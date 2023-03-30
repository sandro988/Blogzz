from django.urls import path
from .views import (
    CreateCommentView,
    CommentDetailView,
    UpdateCommentView,
    DeleteCommentView,
    CommentVoteView,
    ContinueCommentThreadView,
)

urlpatterns = [
    path(
        "comment/<uuid:pk>/",
        CommentDetailView.as_view(),
        name="comment_detail",
    ),
    path(
        "comment/create_comment/<uuid:blog_pk>/",
        CreateCommentView.as_view(),
        name="create_comment",
    ),
    path(
        "comment/reply/<uuid:blog_pk>/<uuid:comment_pk>/",
        CreateCommentView.as_view(),
        name="create_reply",
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
    path(
        "comment/vote_comment/<uuid:blog_pk>/<uuid:comment_pk>/",
        CommentVoteView.as_view(),
        name="vote_comment",
    ),
    path(
        "comment/continue_thread/<uuid:blog_pk>/<uuid:comment_pk>/",
        ContinueCommentThreadView.as_view(),
        name="continue_thread",
    ),
]
