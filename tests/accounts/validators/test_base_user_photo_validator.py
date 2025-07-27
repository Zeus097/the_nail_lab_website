from django.test import TestCase

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError

from accounts.validators import ImageSizeValidator




class PhotoSizeValidatorTestCase(TestCase):
    def setUp(self):
        self.validator = ImageSizeValidator(5)


    def test_valid_photo_size_validator(self):
        photo = SimpleUploadedFile(
        name='small.jpg',
        content=b'\x00' * 1024 * 1024,
        content_type='image/jpeg'
    )
        self.validator(photo)

    def test_invalid_photo_size_validator(self):
        photo = SimpleUploadedFile(
            name='small.jpg',
            content=b'\x00' * 6 * 1024 * 1024,
            content_type='image/jpeg'
        )

        with self.assertRaises(ValidationError):
            self.validator(photo)
