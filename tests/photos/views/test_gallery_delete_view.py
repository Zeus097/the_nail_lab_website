from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from accounts.models import EmployeeBio

from photos.models import GalleryPhoto


User = get_user_model()


class TestGalleryDeleteView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='ivan',
            email='ivan@test.com',
            password='asd123',
            telephone_number='0899123456',
        )
        self.employee = EmployeeBio.objects.create(user=self.user)
        self.client.login(username='ivan', email='ivan@test.com', password='asd123')

        self.photo = GalleryPhoto.objects.create(
            name='Test Photo',
            uploader=self.employee,
            photo='gallery_photos'
        )

    def test_delete_confirmation_page(self):
        url = reverse('gallery_delete', args=[self.photo.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photos_gallery/gallery_delete_img.html')

    def test_redirect_after_deletion(self):
        url = reverse('gallery_delete', args=[self.photo.pk])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('gallery'))
        self.assertFalse(GalleryPhoto.objects.filter(pk=self.photo.pk).exists())
