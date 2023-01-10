from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Blog
from .forms import ContactForm
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
    View for creating new blog post
    """

    model = Blog
    template_name = "blogs/create_blog.html"
    fields = ["blog_title", "blog_category", "blog_body", "blog_thumbnail"]
    login_url = "account_login"

    def form_valid(self, form):
        """
        Check if the user has clicked on Create button, if they did than that means that they are intending
        to publish their blog, but if they click move to drafts button, the blog will not be published, but
        rather saved as a draft that won't be shown on a home page.

        Additionaly for all the new blogs, either draft or published the author of it will be set to request.user.
        """

        if "Create" in self.request.POST:
            form.instance.blog_status = "published"
        else:
            form.instance.blog_status = "draft"

        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateBlogView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View for updating individual blog post
    """

    model = Blog
    template_name = "blogs/update_blog.html"
    fields = ["blog_title", "blog_category", "blog_body", "blog_thumbnail"]
    login_url = "account_login"

    def form_valid(self, form):
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
