from django.urls import path
from .views import CreateCommentView, CommentDetailView

urlpatterns = [
    path(
        "comment/<uuid:pk>/",
        CommentDetailView.as_view(),
        name="comment_detail",
    ),
    path(
        "comment/create_comment/<uuid:pk>/",
        CreateCommentView.as_view(),
        name="create_comment",
    ),
]
