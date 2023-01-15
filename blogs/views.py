from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Blog, Category
from .forms import ContactForm, BlogForm
from django.urls import reverse_lazy


class HomePageView(ListView):
    """
    View created for a home page, this view outputs blogs to users that are
    authenticated and the template that this view uses is: home_authenticated.html,
    but if the users are not authenticated the view will use home_not_authenticated.html
    as a template instead, which is kind of a welcome page template for users that are not yet
    authenticated.

    This view also takes in a ContactForm, that is outputed in a contact section at
    home_not_authenticated.html, this form can be used by users to send email messages
    to us.
    """

    model = Blog
    context_object_name = "blog_list"
    template_name = "home.html"

    def get_queryset(self):
        published_objects = Blog.published_objects
        return published_objects.get_queryset()

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context["form"] = ContactForm()
        return context


class BlogsDetailView(LoginRequiredMixin, DetailView):
    """
    View created for outputing details of idividual blog posts.
    """

    model = Blog
    context_object_name = "blog"
    template_name = "blogs/blogs_detail.html"
    login_url = "account_login"


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

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class ContactFormView(FormView):
    """
    View created for handling ContacForm submissions from users.
    """

    template_name = "blogs/contact_form.html"
    form_class = ContactForm
    success_url = "/contact/"

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)
