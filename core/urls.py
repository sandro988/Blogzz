from django.urls import path
from .views import WelcomePageView, ContactFormView

urlpatterns = [
    path("", WelcomePageView.as_view(), name="welcome-page"),
    path("contact/", ContactFormView.as_view(), name="contact"),
]
