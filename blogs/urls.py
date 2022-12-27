from django.urls import path
from .views import HomePageView, BlogsDetailView, ContactFormView, ContactFormSuccessfullView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("blog/<uuid:pk>/", BlogsDetailView.as_view(), name="blog_detail"),

    # Contact form urls
    path("contact/", ContactFormView.as_view(), name="contact"),
    path("contact-successfull/", ContactFormSuccessfullView.as_view(), name="contact_successfull")
]
