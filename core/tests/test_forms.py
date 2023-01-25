from django.core import mail
from django.test import SimpleTestCase
from django.urls import reverse
from core.forms import ContactForm
from django.conf import settings


class ContactFormTests(SimpleTestCase):
    def setUp(self):
        self.user_name = "Test_user"
        self.user_email = "Test_user@mail.com"
        self.user_message = "This is a test message"
        self.recipient_email = settings.EMAIL_HOST_USER
        self.subject = f"A message from contact form by: {self.user_name}"
        self.success_url = reverse("welcome-page")

    def test_contact_form_with_valid_data(self):
        form = ContactForm(
            data={
                "name": self.user_name,
                "email": self.user_email,
                "message": self.user_message,
            }
        )

        # Checking that the form is valid in the first place
        self.assertTrue(form.is_valid())

        response = self.client.post(reverse("contact"), data=form.cleaned_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.success_url, status_code=302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.recipient_email])

        # I am using lower() method on user_email because in the ContactForm when cleaning the form data
        # and i turn the email field to lowercase, so in this test when our form is submitted "Test_user@mail.com"
        # will turn into "test_user@mail.com"
        self.assertEqual(mail.outbox[0].reply_to, [self.user_email.lower()])
        self.assertEqual(mail.outbox[0].subject, self.subject)
        self.assertEqual(mail.outbox[0].body, self.user_message)

    def test_contact_form_with_invalid_data(self):
        form = ContactForm(
            data={
                "name": self.user_name,
                "email": "invalid_email",
                "message": self.user_message,
            }
        )

        # Checking that the form is valid in the first place
        self.assertFalse(form.is_valid())

        response = self.client.post(reverse("contact"), data=form.cleaned_data)

        # Assert that the form is invalid and that correct error message is returned to users
        # status code is 200 because we are not redirecting the users.
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "There was an error with sending your message. Please try again."
        )

        # Assert that the template used is "core/contact_form.html"
        self.assertTemplateUsed(response, "core/contact_form.html")

        # Checking that email was not sent
        self.assertEqual(len(mail.outbox), 0)

    def test_contact_form_with_incomplete_and_empty_data(self):
        form = ContactForm(
            data={
                "name": self.user_name,
                "email": "",
                "message": self.user_message,
            }
        )

        # Checking that the form is valid in the first place
        self.assertFalse(form.is_valid())

        response = self.client.post(reverse("contact"), data=form.cleaned_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "There was an error with sending your message. Please try again."
        )

        # Assert that the template used is "core/contact_form.html"
        self.assertTemplateUsed(response, "core/contact_form.html")

        # Checking that email was not sent
        self.assertEqual(len(mail.outbox), 0)

    def test_contact_form_with_empty_data(self):
        form = ContactForm(data={"name": "", "email": "", "message": ""})

        # Checking that the form is valid in the first place
        self.assertFalse(form.is_valid())

        response = self.client.post(reverse("contact"), data=form.cleaned_data)

        # Assert that the form is invalid and that correct error message is returned to users
        # status code is 200 because we are not redirecting the users.
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "There was an error with sending your message. Please try again."
        )

        # Assert that the template used is "core/contact_form.html"
        self.assertTemplateUsed(response, "core/contact_form.html")

        # Checking that email was not sent
        self.assertEqual(len(mail.outbox), 0)
