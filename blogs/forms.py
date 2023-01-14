from django import forms
from django.core.mail import EmailMessage, BadHeaderError
from django.http import HttpResponse
from django.conf import settings
from .models import Blog
from django_editorjs_fields import EditorJsWidget


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
            }
        ),
    )
    email = forms.EmailField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
            }
        ),
    )
    message = forms.CharField(
        max_length=500,
        widget=forms.Textarea(
            attrs={
                "autocomplete": "off",
            }
        ),
    )

    # Removing cols and rows attributes from textarea field so that i can specify
    # a more specific size to it in the css.
    message.widget.attrs.pop("cols", None)
    message.widget.attrs.pop("rows", None)

    def clean(self):
        """
        Cleaning form data, Capitalizing first letters
        of name and message fields and making email lowercase
        """

        name = self.cleaned_data.get("name", "")
        email = self.cleaned_data.get("email", "")
        message = self.cleaned_data.get("message", "")

        if name and email and message:
            name = name[0].upper() + name[1:].lower()
            message = message[0].upper() + message[1:].lower()
            email = email.lower()

        return {"name": name, "email": email, "message": message}

    def send_email(self):
        """
        Function used for sending emails from
        users that have subbmitted contact form
        """

        data = self.clean()

        if data["name"] and data["message"] and data["email"]:
            try:
                email = EmailMessage(
                    f"A message from contact form by: {data['name']}",
                    data["message"],
                    data["email"],
                    [settings.EMAIL_HOST_USER],
                    reply_to=[data["email"]],
                )
                email.send()
            except BadHeaderError:
                return HttpResponse("Invalid header found.")


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        exclude = ["blog_status", "author"]
        widgets = {
            "body_editorjs": EditorJsWidget(config={"minHeight": 100}),
            "body_editorjs_text": EditorJsWidget(
                plugins=["@editorjs/image", "@editorjs/header"]
            ),
        }
