from typing import Optional

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class ImageSizeValidator:
    def __init__(self, image_size_limit, message: Optional[str] = None):
        self.image_size_limit = image_size_limit
        self.message = message

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        if value is None:
            self.__message = f"Размерът на снимката трябва да е по малък от {self.image_size_limit}MB!"
        self.__message = value

    def __call__(self, value):
        if value.size > self.image_size_limit * 1024 * 1024:
            raise ValidationError(self.message)
