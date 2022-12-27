from django import forms
from django.core.mail import EmailMessage, BadHeaderError
from django.http import HttpResponse
from django.conf import settings


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    message = forms.CharField(widget=forms.Textarea, max_length=500)

    def clean(self):
        """
        Cleaning form data, Capitalizing first letters
        of name and message fields and making email lowercase
        """

        name = self.cleaned_data["name"]
        email = self.cleaned_data["email"]
        message = self.cleaned_data["message"]

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
        
        if data['name'] and data['message'] and data['email']:
            try:
                email = EmailMessage(
                    f"A message from contact form by: {data['name']}", 
                    data["message"], 
                    data["email"], 
                    [settings.EMAIL_HOST_USER],
                    reply_to=[data["email"]],
                )
                email.send()
                print("it worked")
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
        

