from django.urls import path
from .views import (
    HomePageView,
    BlogsDetailView,
    CreateBlogView,
    UpdateBlogView,
    DeleteBlogView,
    LikeBlogView,
)

urlpatterns = [
    path("home/", HomePageView.as_view(), name="home"),
    path("blog/<uuid:pk>/", BlogsDetailView.as_view(), name="blog_detail"),
    path("blog/create_blog/", CreateBlogView.as_view(), name="create_blog"),
    path("blog/update_blog/<uuid:pk>/", UpdateBlogView.as_view(), name="update_blog"),
    path("blog/delete_blog/<uuid:pk>/", DeleteBlogView.as_view(), name="delete_blog"),
    path("blog/like_blog/<uuid:pk>/", LikeBlogView.as_view(), name="like_blog"),
]
