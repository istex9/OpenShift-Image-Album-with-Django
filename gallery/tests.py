from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class GalleryTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='tesztuser', password='tesztjelszo')

    def test_login_required_for_upload(self):
        response = self.client.get(reverse('upload_photo'))
        self.assertRedirects(response, f'/accounts/login/?next={reverse("upload_photo")}')

    def test_homepage_accessible(self):
        self.client.login(username='tesztuser', password='tesztjelszo')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fényképek listája")
