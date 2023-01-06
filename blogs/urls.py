from django.urls import path
from .views import (
    HomePageView,
    BlogsDetailView,
    CreateBlogView,
    UpdateBlogView,
    DeleteBlogView,
    ContactFormView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("blog/<uuid:pk>/", BlogsDetailView.as_view(), name="blog_detail"),
    path("blog/create_blog/", CreateBlogView.as_view(), name="create_blog"),
    path("blog/update_blog/<uuid:pk>/", UpdateBlogView.as_view(), name="update_blog"),
    path("blog/delete_blob/<uuid:pk>/", DeleteBlogView.as_view(), name="delete_blog"),
    # Contact form url
    path("contact/", ContactFormView.as_view(), name="contact"),
]
