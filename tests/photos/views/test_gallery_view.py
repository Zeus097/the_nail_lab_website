from io import BytesIO

from PIL import Image

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from accounts.models import EmployeeBio
from photos.models import GalleryPhoto

User = get_user_model()

def create_test_image_file():
    # Image generator

    image = Image.new('RGB', (100, 100), color='red')
    image_io = BytesIO()
    image.save(image_io, format='JPEG')
    image_io.seek(0)
    return SimpleUploadedFile('test.jpg', image_io.read(), content_type='image/jpeg')



class TestGalleryView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='ivan', email='ivan@test.com', password='asd123')
        self.employee = EmployeeBio.objects.create(user=self.user)
        self.client.login(username='ivan', email='ivan@test.com', password='asd123')

        # Creating images for 'test_gallery__pagination'
        for i in range(10):
            GalleryPhoto.objects.create(
                name=f"Photo {i}",
                description=f"Description {i}",
                uploader=self.employee,
                photo=create_test_image_file()
            )

    def test_gallery_view_status_code(self):
        response = self.client.get(reverse('gallery'))
        self.assertEqual(response.status_code, 200)

    def test_gallery__pagination(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('gallery'))
        response.render()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['gallery_list']), 8)

    def test_gallery_view_uses_correct_template(self):
        response = self.client.get(reverse('gallery'))
        self.assertTemplateUsed(response, 'photos_gallery/gallery_main.html')

