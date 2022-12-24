from django.views.generic import ListView, DetailView
from .models import Blog


class HomePageView(ListView):
    model = Blog
    context_object_name = "blog_list"
    template_name = "blogs/blogs_list.html"


class BlogsDetailView(DetailView):
    model = Blog
    context_object_name = "blog"
    template_name = "blogs/blogs_detail.html"
