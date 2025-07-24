from django.test import TestCase

from django.core.exceptions import ValidationError

from accounts.validators import PhoneValidator



class PhoneValidatorTestCase(TestCase):
    def setUp(self):
        self.validator = PhoneValidator()

    def test_valid_phone_input_with_plus(self):
        tel_number = '+359974567812'
        self.validator(tel_number)

    def test_valid_phone_input_with_spaces(self):
        tel_number = '+359 9745 678 12'
        self.validator(tel_number)

    def test_valid_phone_input_without_spaces_and_without_plus(self):
        tel_number = '359974567812'
        self.validator(tel_number)

    def test_valid_phone_input_with_spaces_and_without_plus(self):
        tel_number = '359 9745 678 12'
        self.validator(tel_number)

    def test_invalid_phone_input_with_less_than_nine_symbols(self):
        tel_number = '+3599745'
        with self.assertRaises(ValidationError):
            self.validator(tel_number)

    def test_invalid_phone_input_with_more_than_fifteen_symbols(self):
        tel_number = '+3599759974545599745'
        with self.assertRaises(ValidationError):
            self.validator(tel_number)