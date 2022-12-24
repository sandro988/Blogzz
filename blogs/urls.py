from django.urls import path
from .views import HomePageView, BlogsDetailView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("<uuid:pk>/", BlogsDetailView.as_view(), "book_detail"),
]
