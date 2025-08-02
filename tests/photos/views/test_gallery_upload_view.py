from django.test import TestCase
from django.contrib.auth import get_user_model


User = get_user_model()


class TestGalleryUploadView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='ivan',
            email='ivan@test.com',
            password='asd123',
            telephone_number='0899123456',
            is_employee=True,
        )
        self.client.login(username='ivan', password='asd123')

    def test_get_request_returns_form(self):
        response = self.client.get('/photos/gallery/upload/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photos_gallery/gallery_upload.html')
        self.assertIn('form', response.context)
