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
        "<uuid:pk>/",
        CommentDetailView.as_view(),
        name="comment_detail",
    ),
    path(
        "create_comment/<uuid:blog_pk>/",
        CreateCommentView.as_view(),
        name="create_comment",
    ),
    path(
        "reply/<uuid:blog_pk>/<uuid:comment_pk>/",
        CreateCommentView.as_view(),
        name="create_reply",
    ),
    path(
        "update_comment/<uuid:pk>/",
        UpdateCommentView.as_view(),
        name="update_comment",
    ),
    path(
        "delete_comment/<uuid:pk>/",
        DeleteCommentView.as_view(),
        name="delete_comment",
    ),
    path(
        "vote_comment/<uuid:pk>/",
        CommentVoteView.as_view(),
        name="vote_comment",
    ),
    path(
        "continue_thread/<uuid:pk>/",
        ContinueCommentThreadView.as_view(),
        name="continue_thread",
    ),
]
