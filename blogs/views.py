from django.views.generic import ListView, DetailView, FormView
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

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context["form"] = ContactForm()
        return context


class BlogsDetailView(DetailView):
    """
    View created for outputing details of idividual blog posts.
    """

    model = Blog
    context_object_name = "blog"
    template_name = "blogs/blogs_detail.html"


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
