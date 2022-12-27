from django.views.generic import ListView, DetailView, FormView, TemplateView
from .models import Blog
from .forms import ContactForm
from django.urls import reverse_lazy


class HomePageView(ListView):
    model = Blog
    context_object_name = "blog_list"
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context =  super(HomePageView, self).get_context_data(**kwargs)
        context['form'] = ContactForm()
        return context


class BlogsDetailView(DetailView):
    model = Blog
    context_object_name = "blog"
    template_name = "blogs/blogs_detail.html"

class ContactFormView(FormView):
    template_name = 'blogs/home.html'
    form_class = ContactForm
    success_url = reverse_lazy("contact_successfull")

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


class ContactFormSuccessfullView(TemplateView):
    template_name = "blogs/contact_email_sent_successfull.html"
