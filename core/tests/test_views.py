from django.test import SimpleTestCase
from django.urls import reverse


class WelcomePageViewTests(SimpleTestCase):
    def test_welcome_page_view(self):
        response = self.client.get(reverse("welcome-page"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/welcome.html")
        self.assertContains(response, "Stay curious and enjoy writing")


class ContactPageViewTests(SimpleTestCase):
    def test_contact_page_view(self):
        # on GET request client should be redirected to welcome page

        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 302)

        # setting follow to True, so that we can check if the page
        # that is loaded after redirect is correct.

        response = self.client.get(reverse("contact"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/welcome.html")
        self.assertContains(response, "Stay curious and enjoy writing")
