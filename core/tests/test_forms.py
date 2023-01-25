from django.core import mail
from django.test import SimpleTestCase
from django.urls import reverse


class ContactFormTests(SimpleTestCase):
    def setUp(self):
        self.subject = "Testing email"
        self.body = "This is going to be a test for my contact form that sends emails from users to me."
        self.email_from = "test_user_1@mail.com"
        self.email_to = "test_user_2@mail.com"
        self.reply_to = self.email_from

    def test_sending_email(self):
        mail.EmailMessage(
            self.subject,
            self.body,
            self.email_from,
            [self.email_to],
            reply_to=[self.email_to],
        ).send()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Testing email")
    
    def test_empty_form_submission(self):
        response = self.client.post(reverse("contact"))

        # Assert that the form is invalid
        self.assertEqual(response.status_code, 200)

        # Assert that the template used is "core/contact_form.html"
        self.assertTemplateUsed(response, "core/contact_form.html")
