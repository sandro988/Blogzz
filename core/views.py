from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, FormView
from django.contrib import messages
from .forms import ContactForm


class WelcomePageView(TemplateView):
    """
    A view created for displaying the welcome page of the website.
    If the request has an 'htmx' attribute, it will display the contact form instead.
    """

    template_name = "core/welcome.html"

    def get_template_names(self):
        if self.request.htmx:
            return "core/contact_form.html"
        return "core/welcome.html"

    def get_context_data(self, **kwargs):
        context = super(WelcomePageView, self).get_context_data(**kwargs)
        context["form"] = ContactForm()
        return context


class ContactFormView(FormView):
    """
    View created for handling ContacForm submissions from users.
    """

    template_name = "core/contact_form.html"
    form_class = ContactForm
    success_url = reverse_lazy("welcome-page")

    def dispatch(self, request, *args, **kwargs):
        if request.method != "POST":
            return redirect(reverse("welcome-page"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error with your submission. Please try again.")
        return super().form_invalid(form)