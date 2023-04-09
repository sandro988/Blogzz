from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Blog, Category
from comments.models import Comment
from .forms import BlogForm
from comments.forms import CommentForm
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.conf import settings
from comments.utils import get_sorted_comments


class HomePageView(LoginRequiredMixin, ListView):
    """
    View created for listing out blogs on home page
    """

    model = Blog
    context_object_name = "blog_list"
    template_name = "blogs/list_blog.html"
    paginate_by = settings.PAGINATION_NUMBER
    login_url = "account_login"

    def get_template_names(self):
        """
        Determines the template to be used for rendering the view, if user scrolls down to a last
        element of a page, new set of blogs from next page is added to the current page, essentially it is a
        infinite scrolling feature, which is handled by htmx, so we check if it is the htmx request
        and return the appropriate template, but if it is not then we just return the 'home.html' template.
        """
        if self.request.htmx:
            return "blogs/partials/masonry_blog_list_element.html"
        return "blogs/list_blog.html"

    def get_queryset(self):
        """
        If user tries to search specific blogs, we get the search value and return blogs that contain
        the search value either in their title or category.

        If user tries to search something and clicks on one of the featured topics, we get the search
        value and lookup any blog with that category name.

        Alternatively If user just goes to home page, we output all of the blogs and paginate by specific number.

        Also we output only the blogs that have status of "published", so any blog that is moved to drafts won't be outputed.
        """

        searched_objects = self.request.GET.get("q")
        searched_objects_by_featured_category = self.request.GET.get("category")

        if searched_objects:
            return Blog.published_objects.filter(
                Q(blog_title__icontains=searched_objects)
                | Q(blog_category__icontains=searched_objects)
            )
        elif searched_objects_by_featured_category:
            return Blog.published_objects.filter(
                Q(blog_category__icontains=searched_objects_by_featured_category)
            )
        else:
            published_objects = Blog.published_objects
            return published_objects.get_queryset()

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context["categories"] = Category.objects.all()[:10]
        context["popular_blogs"] = Blog.get_popular_blogs()
        return context


class BlogsDetailView(LoginRequiredMixin, DetailView):
    """
    View created for outputing details of idividual blog posts.
    """

    model = Blog
    context_object_name = "blog"
    template_name = "blogs/blogs_detail.html"
    login_url = "account_login"

    def get_template_names(self):
        if self.request.htmx:
            return "comments/list_comments.html"
        return "blogs/blogs_detail.html"

    def get_context_data(self, **kwargs):
        context = super(BlogsDetailView, self).get_context_data(**kwargs)
        context["create_page_form"] = CommentForm()
        context["comments"] = get_sorted_comments(
            Comment.objects.filter(blog=self.object), self.request.GET.get("sort")
        )
        return context


class CreateBlogView(LoginRequiredMixin, CreateView):
    """
    A view for creating a new blog post.
    """

    model = Blog
    template_name = "blogs/create_blog.html"
    form_class = BlogForm
    login_url = "account_login"

    def form_valid(self, form):
        """
        Handles the input from the user and creates a new blog post.
        It takes the inputted topic name, checks if it exists in the category model,
        if it does not, it will add it to the category model. Then it sets the author
        of the blog to the currently logged-in user and sets the status of the blog
        to either "published" or "draft" depending on the user's choice.

        Args:
            form (BlogForm): An instance of the BlogForm containing the user's input.

        Returns:
            A redirect to the newly created blog post.
        """

        blog_category = form.cleaned_data["blog_category"].lower()
        category = Category.objects.get_or_create(category_name=blog_category.title())

        form.instance.blog_category_foreignkey = category[0]
        form.instance.author = self.request.user

        if "Create" in self.request.POST:
            form.instance.blog_status = "published"
        else:
            form.instance.blog_status = "draft"

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateBlogView, self).get_context_data(**kwargs)
        context["categories"] = Category.objects.all()[:10]
        context["popular_blogs"] = Blog.get_popular_blogs()
        return context


class UpdateBlogView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View for updating individual blog post
    """

    model = Blog
    template_name = "blogs/update_blog.html"
    form_class = BlogForm
    login_url = "account_login"

    def form_valid(self, form):
        """
        Handles the input from the user and updates the existing blog post.
        It takes the inputted topic name, checks if it exists in the category model,
        if it does not, it will add it to the category model. Then it sets the status of the blog
        to either "published" or "draft" depending on the user's choice.

        Args:
            form (BlogForm): An instance of the BlogForm containing the user's input.

        Returns:
            A redirect to the updated blog
        """

        blog_category = form.cleaned_data["blog_category"].lower()
        category = Category.objects.get_or_create(category_name=blog_category.title())
        form.instance.blog_category_foreignkey = category[0]

        if (
            "Move to drafts" in self.request.POST
            or "Save as draft" in self.request.POST
        ):
            form.instance.blog_status = "draft"
        elif "Publish" in self.request.POST:
            form.instance.blog_status = "published"

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UpdateBlogView, self).get_context_data(**kwargs)
        context["categories"] = Category.objects.all()[:10]
        context["popular_blogs"] = Blog.get_popular_blogs()
        return context

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class DeleteBlogView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View for deleteing individual blog post
    """

    model = Blog
    template_name = "blogs/delete_blog.html"
    success_url = reverse_lazy("home")
    login_url = "account_login"

    def get_context_data(self, **kwargs):
        context = super(DeleteBlogView, self).get_context_data(**kwargs)
        context["categories"] = Category.objects.all()[:10]
        context["popular_blogs"] = Blog.get_popular_blogs()
        return context

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class LikeBlogView(LoginRequiredMixin, View):
    """View created for handling liking and unliking of a blog"""

    login_url = "account_login"
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        """
        Handles the post request to like or unlike a blog.

        Args:
            request: The current request object
            kwargs: Additional keyword arguments, including the id of the blog

        Returns:
            JsonResponse: A JSON response containing the updated number of likes for the blog
        """

        blog = get_object_or_404(Blog, id=kwargs["pk"])
        user = request.user

        if user in blog.blog_likes.all():
            blog.blog_likes.remove(user)
            blog.blog_likes_count -= 1
        else:
            blog.blog_likes.add(user)
            blog.blog_likes_count += 1

        blog.save()
        return JsonResponse(blog.blog_likes_count, safe=False)
